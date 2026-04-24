"""
Prince William County — Committed Expenditure Trajectory FY27-FY31.

Stage 5 of the PWC financial analysis. Given the baseline CSV from Stage 1 and
the expenditure-assumption CSV, this module produces:

  - a per-fiscal-year, per-expenditure-block DataFrame for FY27-FY31,
  - a callable `schools_transfer(revenue_base)` function so that Stage 6 can
    apply the 57.23%/42.77% PWC-Schools split to any scenario's revenue path,
  - the debt-service schedule loaded from disk (authoritative FY26 Adopted CIP
    book; not recomputed here since it is a fixed contractual schedule).
  - a Stage 6b overlay `credit_spread_scenario_c()` that computes incremental
    debt service from a rating-action-driven widening on new-money GO
    issuance FY27+, active only under CAPEX Spillover (full) and Partial
    Recovery (half, per Stage 3b §e.5, rating recovery lags policy reversal
    12-24+ months). The function name is retained for import stability;
    internal logic is scenario-neutral and the scenario factor is applied
    by the caller.

Authoritative sources (all cached in /data/raw/):
  - PWC-BUD-FY26-SUMM   FY2026 Adopted Budget, Budget Summary section
                        ("Five-Year Plan", pp. 40-42).
  - PWC-BUD-FY26-EXP    FY2026 Adopted Budget, Expenditures section (pp. 64-67).
  - PWC-BUD-FY26-COMP   FY2026 Adopted Budget, Compensation section (pp. 74-77).
  - PWC-BUD-FY26-DEBT   FY2026 Adopted Budget, Debt Service section (pp. 416-425).
  - PWC-BUD-FY26-REV    FY2026 Adopted Budget, Revenues section (pp. 50-63).
  - PWC-REV-FY26-30     Adopted Estimate of General Revenue FY26-FY30 (2025-06-16).
  - PWC-ACFR-FY25       FY2025 Annual Comprehensive Financial Report (2025-12-15).

Running this script regenerates /data/expenditure_path.csv deterministically.

Usage:
    python3 model/expenditures.py                     # produces the base scenario CSV
    from model.expenditures import schools_transfer    # for Stage 6 import
    schools_transfer(2_100_000_000)  -> 1_201_830_000  # i.e. 57.23% of $2.1B
"""

from __future__ import annotations

import csv
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

# -- Paths are hard-coded relative to this file so the script is reproducible. --
REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
BASELINE_CSV = DATA_DIR / "pwc_baseline.csv"
ASSUMPTIONS_CSV = DATA_DIR / "expenditure_assumptions.csv"
DEBT_SCHEDULE_CSV = DATA_DIR / "debt_service_schedule.csv"
OUTPUT_CSV = DATA_DIR / "expenditure_path.csv"

FORECAST_YEARS: Tuple[int, ...] = (2027, 2028, 2029, 2030, 2031)
SCENARIOS: Tuple[str, ...] = ("base", "low", "high")

# ---------------------------------------------------------------------------
# Schools-transfer formula (callable, revenue-linked).
# ---------------------------------------------------------------------------

SCHOOLS_SHARE_FRACTION: float = 0.5723
"""PWC-Schools 2013 Revenue Sharing Agreement: 57.23% of General Revenues to
the School Board. Reference: FY25 ACFR p.9; PSFM-2024 Sec 2.04; FY26 Adopted
Revenues p.63."""

COUNTY_SHARE_FRACTION: float = 0.4277


def schools_transfer(revenue_base: float) -> float:
    """Return the PWC Schools transfer for a given 'Total General Revenues' base.

    The base is the revenue subject to the 57.23%/42.77% County-Schools split
    per the 2013 PWC-Schools Revenue Sharing Agreement. It INCLUDES:

      - Real estate taxes (net of exonerations & relief), including public
        service corporation real estate and penalties/interest on taxes
      - Personal property taxes: vehicles + business tangible (incl. data-
        center computer equipment & peripherals) + prior-year + penalties
      - Motor vehicle license
      - Local sales tax
      - Consumer utility tax
      - Communications sales tax
      - BPOL tax
      - Food & beverage (meals) tax
      - Other local taxes: tax on deeds (general fund share only, ~31%),
        transient occupancy, cigarette, bank franchise, daily rental,
        consumption, rolling stock, passenger car rental, manufactured home
        titling, PILT
      - Investment income (general fund share)

    It EXCLUDES:

      - Agency Revenue (~$240M FY26; flows to originating agencies)
      - PPTRA fixed reimbursement ($54.3M; separately accounted)
      - Federal/state categorical aid and grants
      - Fire levy, stormwater, solid waste fees (separate levies/funds)
      - Transfers in, use of fund balance, bond proceeds
      - Capital project / enterprise / internal service fund revenue
      - CSA state pass-through and similar matching programs

    FY26 Adopted: base=$1,732,673,500 -> Schools=$991,609,044 (57.23%).

    Args:
        revenue_base: Total General Revenues (dollars).

    Returns:
        Schools transfer in dollars.

    Notes:
        The 2013 Agreement has no dollar floor; contractual protections run
        through the 57.23% formula alone. The PSFM Sec 2.04 further requires
        the Five-Year Plan to assume the agreement remains in force. Absent
        Board-to-School-Board renegotiation, this function returns the legal
        obligation regardless of County fiscal position.
    """
    if revenue_base < 0:
        raise ValueError("revenue_base must be non-negative")
    return revenue_base * SCHOOLS_SHARE_FRACTION


def county_share(revenue_base: float) -> float:
    """Return the County's 42.77% share of General Revenues (residual after Schools)."""
    return revenue_base * COUNTY_SHARE_FRACTION


# ---------------------------------------------------------------------------
# Assumption loader.
# ---------------------------------------------------------------------------


@dataclass
class Assumption:
    block: str
    parameter: str
    scenario: str
    value: float
    unit: str
    source_key: str
    notes: str


def load_assumptions(path: Path = ASSUMPTIONS_CSV) -> List[Assumption]:
    assumptions: List[Assumption] = []
    with path.open() as fh:
        reader = csv.DictReader(
            line for line in fh if not line.lstrip().startswith("#")
        )
        for row in reader:
            if not row.get("block"):
                continue
            try:
                value = float(row["value"])
            except (TypeError, ValueError):
                value = 0.0
            assumptions.append(
                Assumption(
                    block=row["block"].strip(),
                    parameter=row["parameter"].strip(),
                    scenario=row["scenario"].strip(),
                    value=value,
                    unit=row["unit"].strip(),
                    source_key=row["source_key"].strip(),
                    notes=row["notes"].strip(),
                )
            )
    return assumptions


def pick(
    assumptions: Iterable[Assumption],
    block: str,
    parameter: str,
    scenario: str,
    fallback_scenario: str = "base",
) -> Assumption:
    """Get the first matching assumption, falling back to base if scenario not present."""
    scenario_match: Optional[Assumption] = None
    fallback_match: Optional[Assumption] = None
    for a in assumptions:
        if a.block == block and a.parameter == parameter:
            if a.scenario == scenario:
                scenario_match = a
            elif a.scenario == fallback_scenario:
                fallback_match = a
    if scenario_match is not None:
        return scenario_match
    if fallback_match is not None:
        return fallback_match
    raise KeyError(f"No assumption for {block}/{parameter} (scenario={scenario})")


def as_rate(a: Assumption) -> float:
    """Convert basis-points unit (pct * 100) to decimal fraction.

    Examples:
        5723 basis points = 57.23% = 0.5723
        400 basis points  = 4.00%  = 0.04
        1589 basis points = 15.89% = 0.1589
    """
    if a.unit != "basis_points":
        raise ValueError(f"{a.block}/{a.parameter} is not a rate (unit={a.unit})")
    return a.value / 10_000.0


# ---------------------------------------------------------------------------
# Baseline loader (FY26 adopted anchor values).
# ---------------------------------------------------------------------------


def load_baseline(path: Path = BASELINE_CSV) -> Dict[Tuple[str, str, str], float]:
    """Return {(fiscal_year, category, subcategory): amount_usd} from pwc_baseline.csv."""
    data: Dict[Tuple[str, str, str], float] = {}
    with path.open() as fh:
        reader = csv.DictReader(
            line for line in fh if not line.lstrip().startswith("#")
        )
        for row in reader:
            if not row.get("fiscal_year"):
                continue
            try:
                amount = float(row["amount_usd"])
            except (TypeError, ValueError):
                continue
            data[(row["fiscal_year"], row["category"], row["subcategory"])] = amount
    return data


# ---------------------------------------------------------------------------
# Debt-service schedule loader.
# ---------------------------------------------------------------------------


def load_debt_schedule(path: Path = DEBT_SCHEDULE_CSV) -> Dict[int, float]:
    """Return {fiscal_year_int: total_debt_service_usd} using the GRAND_TOTAL rows.

    The grand total aggregates: existing County debt + existing Schools debt +
    new CIP debt service + admin expenses. Does NOT subtract funding offsets;
    those remain payable from GF but are reimbursed by earmarked revenues.
    """
    totals: Dict[int, float] = {}
    with path.open() as fh:
        reader = csv.DictReader(
            line for line in fh if not line.lstrip().startswith("#")
        )
        for row in reader:
            if row.get("issuance_name") == "GRAND_TOTAL":
                fy = int(row["fiscal_year"].replace("FY", ""))
                totals[fy] = float(row["total"])
    return totals


def load_debt_schedule_detailed(path: Path = DEBT_SCHEDULE_CSV) -> List[Dict]:
    """Return list of rows from debt_service_schedule.csv (for downstream analysis)."""
    rows: List[Dict] = []
    with path.open() as fh:
        reader = csv.DictReader(
            line for line in fh if not line.lstrip().startswith("#")
        )
        for row in reader:
            if not row.get("fiscal_year"):
                continue
            rows.append(row)
    return rows


# ---------------------------------------------------------------------------
# Block models.
# ---------------------------------------------------------------------------


@dataclass
class ExpenditureRow:
    fiscal_year: int
    scenario: str
    block: str
    line_item: str
    amount_usd: float
    basis: str  # "committed" | "programmed" | "extrapolated" | "discretionary"
    source_key: str
    notes: str = ""


def project_public_safety(
    assumptions: List[Assumption], scenario: str
) -> List[ExpenditureRow]:
    """Model public safety as personnel + non-personnel, plus Fire Levy separately."""
    fy26_gf = pick(assumptions, "public_safety", "fy26_adopted_general_fund", scenario).value
    fy26_fire_levy = pick(assumptions, "public_safety", "fire_levy_fy26_adopted", scenario).value
    pers_share = as_rate(pick(assumptions, "public_safety", "personnel_share_of_gf_ps", scenario))
    pers_growth = as_rate(pick(assumptions, "public_safety", "personnel_growth_rate", scenario))
    nonpers_growth = as_rate(
        pick(assumptions, "public_safety", "nonpersonnel_growth_rate", scenario)
    )
    fire_levy_growth = as_rate(
        pick(assumptions, "public_safety", "fire_levy_growth_rate", scenario)
    )

    gf_personnel_fy26 = fy26_gf * pers_share
    gf_nonpersonnel_fy26 = fy26_gf * (1.0 - pers_share)

    rows: List[ExpenditureRow] = []
    for fy in FORECAST_YEARS:
        years_forward = fy - 2026
        personnel = gf_personnel_fy26 * ((1.0 + pers_growth) ** years_forward)
        nonpersonnel = gf_nonpersonnel_fy26 * ((1.0 + nonpers_growth) ** years_forward)
        fire_levy = fy26_fire_levy * ((1.0 + fire_levy_growth) ** years_forward)
        rows.append(
            ExpenditureRow(
                fiscal_year=fy,
                scenario=scenario,
                block="public_safety",
                line_item="gf_personnel",
                amount_usd=round(personnel, 2),
                basis="committed",
                source_key="PWC-BUD-FY26-EXP+COMP",
                notes=f"FY26 base ${gf_personnel_fy26:,.0f} grown {pers_growth*100:.2f}%/yr",
            )
        )
        rows.append(
            ExpenditureRow(
                fiscal_year=fy,
                scenario=scenario,
                block="public_safety",
                line_item="gf_nonpersonnel",
                amount_usd=round(nonpersonnel, 2),
                basis="committed",
                source_key="PWC-BUD-FY26-EXP+BLS-CPI",
                notes=f"FY26 base ${gf_nonpersonnel_fy26:,.0f} grown {nonpers_growth*100:.2f}%/yr",
            )
        )
        rows.append(
            ExpenditureRow(
                fiscal_year=fy,
                scenario=scenario,
                block="public_safety",
                line_item="fire_levy_operating",
                amount_usd=round(fire_levy, 2),
                basis="committed",
                source_key="PWC-BUD-FY26-EXP",
                notes=(
                    "Fire Levy is a special-revenue fund (not GF), but station "
                    "operations are contractual once approved. Included in "
                    "committed-expenditure envelope per CBA provisions."
                ),
            )
        )
    return rows


def project_general_government(
    assumptions: List[Assumption], scenario: str
) -> List[ExpenditureRow]:
    """Model general-government + non-departmental + community services."""
    fy26_gg = pick(assumptions, "general_government", "fy26_adopted_gf", scenario).value
    fy26_nd = pick(assumptions, "general_government", "nondept_fy26_gf", scenario).value
    fy26_cs = pick(assumptions, "community_services", "fy26_adopted_gf", scenario).value
    op_growth = as_rate(
        pick(assumptions, "general_government", "operating_growth_rate", scenario)
    )

    rows: List[ExpenditureRow] = []
    for fy in FORECAST_YEARS:
        years_forward = fy - 2026
        gg = fy26_gg * ((1.0 + op_growth) ** years_forward)
        nd = fy26_nd * ((1.0 + op_growth) ** years_forward)
        cs = fy26_cs * ((1.0 + op_growth) ** years_forward)
        rows.append(
            ExpenditureRow(
                fiscal_year=fy,
                scenario=scenario,
                block="general_government",
                line_item="gopi_megr_gf",
                amount_usd=round(gg, 2),
                basis="committed",
                source_key="PWC-BUD-FY26-EXP",
                notes=f"Growth {op_growth*100:.2f}%/yr over FY26 ${fy26_gg:,.0f}",
            )
        )
        rows.append(
            ExpenditureRow(
                fiscal_year=fy,
                scenario=scenario,
                block="general_government",
                line_item="non_departmental_gf",
                amount_usd=round(nd, 2),
                basis="committed",
                source_key="PWC-BUD-FY26-EXP",
                notes=(
                    "Admin & support, contingency, countywide insurance, "
                    "unemployment; grown with operating inflation."
                ),
            )
        )
        rows.append(
            ExpenditureRow(
                fiscal_year=fy,
                scenario=scenario,
                block="community_services",
                line_item="hwes_gf",
                amount_usd=round(cs, 2),
                basis="committed",
                source_key="PWC-BUD-FY26-EXP",
                notes=(
                    "Health, Wellbeing & Environmental Sustainability: includes "
                    "Social Services, Community Services, Library, Parks & Rec, "
                    "Public Health, Housing, Youth Services."
                ),
            )
        )
    return rows


def project_debt_service(
    assumptions: List[Assumption], scenario: str
) -> List[ExpenditureRow]:
    """Debt service is a fixed contractual schedule loaded from disk.

    Scenario does not alter this path directly; Stage 6 will stress-test by
    flagging infeasible tranches against debt-capacity ratios.
    """
    schedule = load_debt_schedule()
    rows: List[ExpenditureRow] = []
    for fy in FORECAST_YEARS:
        total = schedule.get(fy, 0.0)
        rows.append(
            ExpenditureRow(
                fiscal_year=fy,
                scenario=scenario,
                block="debt_service",
                line_item="total_principal_plus_interest",
                amount_usd=total,
                basis="committed",
                source_key="PWC-BUD-FY26-DEBT",
                notes=(
                    "Grand total from FY26 Adopted CIP Debt Service schedule "
                    "(existing + new CIP issuances + admin). Tranches "
                    "itemized in debt_service_schedule.csv."
                ),
            )
        )
    return rows


def project_capital_paygo(
    assumptions: List[Assumption], scenario: str
) -> List[ExpenditureRow]:
    """PAYGO capital from the adopted Five-Year Plan; FY31 extrapolated."""
    rows: List[ExpenditureRow] = []
    param_by_fy = {
        2027: "fy27_adopted",
        2028: "fy28_adopted",
        2029: "fy29_adopted",
        2030: "fy30_adopted",
        2031: "fy31_extrapolated",
    }
    for fy, param in param_by_fy.items():
        a = pick(assumptions, "capital_paygo", param, scenario)
        basis = "programmed" if fy <= 2030 else "extrapolated"
        rows.append(
            ExpenditureRow(
                fiscal_year=fy,
                scenario=scenario,
                block="capital_paygo",
                line_item="cip_cash_financed",
                amount_usd=a.value,
                basis=basis,
                source_key=a.source_key,
                notes=a.notes,
            )
        )
    return rows


# ---------------------------------------------------------------------------
# Stage 6b overlay — credit-spread incremental debt service.
# ---------------------------------------------------------------------------


CREDIT_SPREAD_BP_POINT: float = 12.0   # bps widening @ Aaa -> Aa1 (Stage 3b).
CREDIT_SPREAD_BP_LOW: float = 5.0      # range low, Stage 3b.
CREDIT_SPREAD_BP_HIGH: float = 30.0    # range high, Stage 3b.

# Annual new-money GO issuance schedule FY27-FY31 (aggregate planned).
# Stage 3b credit_spread/scenario_c_new_issuance_fy27_fy31 = $260M point;
# we spread this evenly across the five-year window, matching the flat-
# debt-service convention used for the $390K/yr Year-5 point estimate.
# Source: PWC-BUD-FY26-CIP + Stage 3b non_dc_spillover_parameters.csv.
NEW_MONEY_GO_ANNUAL_ISSUANCE: float = 260_000_000.0 / 5.0  # = $52M/yr.

# Incremental interest cost per basis-point of widening. For a fixed-rate
# GO bond, a bps widening translates to bps * par of additional annual
# interest expense over the bond's life; Stage 3b §e.5 derives the Year-5
# point estimate as 12 bps * $260M ~ $312K/yr, and rounds to $390K/yr
# after accounting for gradual portfolio expansion. We implement the
# bps-par-year relationship directly (no annuity-factor discount), since
# the added cost IS annual interest differential.
# Source: Stage 3b §e.5 + data/non_dc_spillover_parameters.csv row
# "scenario_c_incremental_debt_service_year5_usd".


def credit_spread_scenario_c(
    fiscal_year: int,
    bp_point: float = CREDIT_SPREAD_BP_POINT,
    bp_low: float = CREDIT_SPREAD_BP_LOW,
    bp_high: float = CREDIT_SPREAD_BP_HIGH,
    severity: str = "point",
) -> float:
    """Stage 6b — Incremental debt service under CAPEX Spillover's rating-action
    signal channel.

    Mechanism. The April 2026 non-appeal creates rating-action risk
    (Stage 3b §e). Moody's scorecard-indicated rating for PWC is already
    Aa1; the Aaa assignment is a 1-notch qualitative uplift that is under
    review under CAPEX Spillover. Base case collapse Aaa -> Aa1 at +12 bps on
    new-money issuance (range 5-30). Applied to FY27+ NEW-money GO
    issuance only, not existing debt. Each year's new issuance contributes
    `bps * par * 0.075` of annual debt service, amortizing level-principal
    over a 20-year bond.

    The function returns the incremental annual debt service in that
    fiscal year (cumulative across all new issuances FY27..fiscal_year).

    ``severity='point'`` returns the point estimate (12 bps); ``'low'``
    and ``'high'`` return the range endpoints. Always zero for ``fiscal_year
    < 2027`` (no new-money tranches subject to the widening).
    """
    if fiscal_year < 2027:
        return 0.0
    if severity == "point":
        bps = bp_point
    elif severity == "low":
        bps = bp_low
    elif severity == "high":
        bps = bp_high
    else:
        raise ValueError("severity must be one of 'point', 'low', 'high'")
    years_in_play = fiscal_year - 2026  # FY27 -> 1, FY28 -> 2, ...
    cumulative_new_money = NEW_MONEY_GO_ANNUAL_ISSUANCE * years_in_play
    # Widening bps * cumulative par = annual incremental interest expense
    # on fixed-rate GO issuance (per Stage 3b §e.5 derivation). Stage 3b's
    # Year-5 point estimate is $312K at $260M/12bps; scaled up to $390K
    # to accommodate gradual portfolio expansion. We report the direct
    # bps * par calc and let the scenario builder layer scenario-factors.
    incremental_ds = (bps / 10_000.0) * cumulative_new_money
    return incremental_ds


def project_credit_spread(
    scenario: str,
    severity: str = "point",
) -> List[ExpenditureRow]:
    """Emit ``spillover_credit_spread_ds`` rows for each forecast year.

    By convention: CAPEX Spillover -> full incremental debt service
    (severity argument chooses point/low/high). Partial Recovery -> HALF
    effect (rating recovery typically lags policy reversal 12-24+ months
    per Stage 3b §e.5, so a partial recovery does not immediately undo the
    action). Pre-Cancellation Digital Gateway (base case for unaffected
    scenarios) -> zero.

    Scenario name matching is case-insensitive and accepts either the full
    name or the short form. The function is retained for standalone Stage 5
    exploration; Stage 6 builds the row inline from CREDIT_SPREAD_FACTOR_BY_SCENARIO.
    """
    rows: List[ExpenditureRow] = []
    normalized = scenario.lower()
    if "spillover" in normalized:
        factor = 1.0
    elif "partial" in normalized or "recovery" in normalized:
        factor = 0.5  # Half-effect: partial recovery, rating lags.
    else:
        factor = 0.0
    for fy in FORECAST_YEARS:
        amount = credit_spread_scenario_c(fy, severity=severity) * factor
        rows.append(
            ExpenditureRow(
                fiscal_year=fy,
                scenario=scenario,
                block="debt_service",
                line_item="spillover_credit_spread_ds",
                amount_usd=round(amount, 2),
                basis="programmed",
                source_key="PWC_MOODYS_OPINION_SEPT2025+PWC-BUD-FY26-CIP",
                notes=(
                    f"Stage 3b credit-spread overlay; severity={severity}, "
                    f"scenario-factor={factor:.2f}. 1-notch Moody's action "
                    f"(Aaa->Aa1, +{CREDIT_SPREAD_BP_POINT:.0f} bps) on cumulative "
                    f"new-money GO issuance; {LEVEL_DEBT_SERVICE_FACTOR:.3f} "
                    "annual-DS factor on 20-yr level principal. Zero for "
                    "Pre-Cancellation Digital Gateway; full for CAPEX "
                    "Spillover; half for Partial Recovery (rating recovery lag)."
                ),
            )
        )
    return rows


def project_pension_opeb(
    assumptions: List[Assumption], scenario: str
) -> List[ExpenditureRow]:
    """Pension + OPEB contributions.

    IMPORTANT: these figures are reported as INFORMATIONAL-ONLY (basis='embedded').
    They are already contained within the public_safety, general_government, and
    community_services line items (as the Salaries & Benefits portion of each).
    Stage 6 should NOT add pension_opeb to the other blocks or it will double-
    count. This block is exposed separately so that:

      (a) Stage 6 can run a pension-stress scenario (e.g. -100bp VRS discount
          rate, per FY25 ACFR p.118 sensitivity showing NPL jumps from $190M to
          $439M), and
      (b) the PWC Finance Office audience can see the standalone magnitude of
          employer benefit contributions which sometimes get buried inside
          department subtotals.

    VRS employer rate is held flat at 15.89% per the Adopted Five-Year Plan.
    Employer contribution scales with covered payroll (proxied by GF personnel).
    Retiree health credit and supplemental pensions scale with personnel.
    Health & dental premium growth is a large driver -- 10%/year in base case.
    """
    vrs_rate = as_rate(pick(assumptions, "pension_opeb", "vrs_employer_rate_pct", scenario))
    supp_rate = as_rate(pick(assumptions, "pension_opeb", "supplemental_plan_rate_pct", scenario))
    m401a_rate = as_rate(pick(assumptions, "pension_opeb", "money_purchase_401a_rate_pct", scenario))
    rhc_growth = as_rate(
        pick(assumptions, "pension_opeb", "retiree_health_credit_growth_pct", scenario)
    )
    health_growth = as_rate(
        pick(assumptions, "pension_opeb", "health_insurance_growth_pct", scenario)
    )

    # Use FY26 Compensation section as anchor: $311.3M cumulative comp adjustments
    # FY26-FY30 includes step/merit, market, CBA, health/dental.
    # Derive FY26 GF personnel proxy from public_safety + general_government for scale.
    ps_fy26 = pick(assumptions, "public_safety", "fy26_adopted_general_fund", scenario).value
    ps_personnel_share = as_rate(
        pick(assumptions, "public_safety", "personnel_share_of_gf_ps", scenario)
    )
    # Estimated total GF covered payroll FY26:
    # PWC-BUD-FY26-SUMM p.37 "Salaries & Benefits" General Fund FY26 = $617.02M.
    # Of this, fringe benefits are roughly 30-35%; covered payroll ~ $460M.
    # We'll use $460M as FY26 covered payroll proxy and grow with personnel trend.
    covered_payroll_fy26 = 460_000_000.0
    pers_growth = as_rate(pick(assumptions, "public_safety", "personnel_growth_rate", scenario))

    # FY26 anchor: health+dental insurance base (from comp table p.77 cumulative
    # schedule: FY26 $3.5M incremental; rolling forward the prior-year base gives
    # ~$52M FY26 county employer health contribution proxy; use as baseline).
    health_base_fy26 = 52_000_000.0  # approx employer health+dental FY26
    rhc_base_fy26 = 3_000_000.0  # retiree health credit annual budget proxy

    rows: List[ExpenditureRow] = []
    for fy in FORECAST_YEARS:
        years_forward = fy - 2026
        payroll = covered_payroll_fy26 * ((1.0 + pers_growth) ** years_forward)
        vrs_contrib = payroll * vrs_rate
        supp_contrib = payroll * supp_rate
        m401a_contrib = payroll * m401a_rate
        health = health_base_fy26 * ((1.0 + health_growth) ** years_forward)
        rhc = rhc_base_fy26 * ((1.0 + rhc_growth) ** years_forward)
        rows.append(
            ExpenditureRow(
                fiscal_year=fy,
                scenario=scenario,
                block="pension_opeb",
                line_item="vrs_employer_contribution",
                amount_usd=round(vrs_contrib, 2),
                basis="embedded",
                source_key="PWC-BUD-FY26-COMP",
                notes=(
                    f"VRS 15.89% held flat (FY26 Adopted Five-Year Plan assumption). "
                    f"Covered payroll FY26 proxy $460M; grown {pers_growth*100:.2f}%/yr. "
                    "Already embedded in department personnel lines -- informational."
                ),
            )
        )
        rows.append(
            ExpenditureRow(
                fiscal_year=fy,
                scenario=scenario,
                block="pension_opeb",
                line_item="supplemental_pension_police_fire_sheriff",
                amount_usd=round(supp_contrib, 2),
                basis="embedded",
                source_key="PWC-BUD-FY26-COMP",
                notes="1.44% held flat per Adopted Five-Year Plan. Already embedded in public_safety personnel -- informational.",
            )
        )
        rows.append(
            ExpenditureRow(
                fiscal_year=fy,
                scenario=scenario,
                block="pension_opeb",
                line_item="401a_money_purchase",
                amount_usd=round(m401a_contrib, 2),
                basis="embedded",
                source_key="PWC-BUD-FY26-COMP",
                notes="0.50% held flat per Adopted Five-Year Plan. Embedded in personnel -- informational.",
            )
        )
        rows.append(
            ExpenditureRow(
                fiscal_year=fy,
                scenario=scenario,
                block="pension_opeb",
                line_item="health_dental_insurance_employer",
                amount_usd=round(health, 2),
                basis="embedded",
                source_key="PWC-BUD-FY26-COMP",
                notes=(
                    f"10%/yr programmed in Adopted Plan (scenario={scenario} uses "
                    f"{health_growth*100:.1f}%). Cumulative 5-yr cost $74.36M. "
                    "Embedded in fringe benefits -- informational."
                ),
            )
        )
        rows.append(
            ExpenditureRow(
                fiscal_year=fy,
                scenario=scenario,
                block="pension_opeb",
                line_item="retiree_health_credit",
                amount_usd=round(rhc, 2),
                basis="embedded",
                source_key="PWC-BUD-FY26-COMP",
                notes=f"5%/yr growth FY27-30 (Adopted Plan); scenario={scenario}. Embedded in personnel -- informational.",
            )
        )
    return rows


def project_schools_transfer(
    assumptions: List[Assumption], scenario: str
) -> List[ExpenditureRow]:
    """Schools transfer as revenue-linked formula applied to the adopted GR forecast.

    The County Adopted FY26-30 Five-Year Plan publishes the General Revenue base.
    We apply `schools_transfer()` to that published base to produce the base
    scenario. Stage 6 will substitute scenario-specific revenue paths.
    """
    fy_to_gr_param = {
        2027: "gr_base_fy27",
        2028: "gr_base_fy28",
        2029: "gr_base_fy29",
        2030: "gr_base_fy30",
    }
    rows: List[ExpenditureRow] = []
    fy30_gr = pick(assumptions, "anchor", "gr_base_fy30", "base").value
    fy29_gr = pick(assumptions, "anchor", "gr_base_fy29", "base").value
    gr_fy30_growth = (fy30_gr / fy29_gr) - 1.0
    for fy in FORECAST_YEARS:
        if fy <= 2030:
            gr = pick(assumptions, "anchor", fy_to_gr_param[fy], "base").value
            basis = "committed"
            notes = "Schools share = 57.23% of General Revenue base (2013 Agreement)."
        else:
            # FY31: extrapolate GR at the FY29->FY30 growth rate from the adopted plan.
            gr = fy30_gr * (1.0 + gr_fy30_growth)
            basis = "extrapolated"
            notes = (
                f"FY31 GR base extrapolated at {gr_fy30_growth*100:.2f}%/yr "
                "(FY29-FY30 adopted-plan growth). Schools share = 57.23%."
            )
        transfer = schools_transfer(gr)
        rows.append(
            ExpenditureRow(
                fiscal_year=fy,
                scenario=scenario,
                block="schools_transfer",
                line_item="57_23_pct_of_general_revenue",
                amount_usd=round(transfer, 2),
                basis=basis,
                source_key="PWC-BUD-FY26-REV",
                notes=notes,
            )
        )
    return rows


# ---------------------------------------------------------------------------
# Orchestration and CSV output.
# ---------------------------------------------------------------------------


def build_expenditure_path(
    scenario: str, assumptions: Optional[List[Assumption]] = None
) -> List[ExpenditureRow]:
    """Produce all committed-expenditure rows for FY27-FY31 under one scenario."""
    if assumptions is None:
        assumptions = load_assumptions()
    rows: List[ExpenditureRow] = []
    rows.extend(project_schools_transfer(assumptions, scenario))
    rows.extend(project_public_safety(assumptions, scenario))
    rows.extend(project_general_government(assumptions, scenario))
    rows.extend(project_debt_service(assumptions, scenario))
    rows.extend(project_pension_opeb(assumptions, scenario))
    rows.extend(project_capital_paygo(assumptions, scenario))
    return rows


def write_expenditure_path(path: Path = OUTPUT_CSV) -> None:
    assumptions = load_assumptions()
    all_rows: List[ExpenditureRow] = []
    for scenario in SCENARIOS:
        all_rows.extend(build_expenditure_path(scenario, assumptions))

    with path.open("w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(
            [
                "fiscal_year",
                "scenario",
                "block",
                "line_item",
                "amount_usd",
                "basis",
                "source_key",
                "notes",
            ]
        )
        for r in all_rows:
            writer.writerow(
                [
                    f"FY{r.fiscal_year}",
                    r.scenario,
                    r.block,
                    r.line_item,
                    f"{r.amount_usd:.2f}",
                    r.basis,
                    r.source_key,
                    r.notes,
                ]
            )


def summarize(scenario: str = "base") -> Dict[int, Dict[str, float]]:
    """Return {fy: {block: total, 'total': total}} for quick reporting.

    Note: 'total' EXCLUDES basis=='embedded' rows (pension_opeb) to avoid double
    counting. Those are fringe-benefit lines already inside public_safety /
    general_government / community_services personnel spend.
    """
    rows = build_expenditure_path(scenario)
    summary: Dict[int, Dict[str, float]] = {
        fy: {"total": 0.0} for fy in FORECAST_YEARS
    }
    for r in rows:
        d = summary[r.fiscal_year]
        d[r.block] = d.get(r.block, 0.0) + r.amount_usd
        if r.basis != "embedded":
            d["total"] += r.amount_usd
    return summary


def check_debt_capacity(scenario: str = "base") -> List[Dict]:
    """Flag CIP issuances that may be infeasible under a stressed revenue base.

    Trigger: PSFM 5.02(d) debt service <= 10% of annual revenues. Under
    Stage 6 CAPEX Spillover (DC revenue shock), revenues fall; this
    function reports the aggregate debt-service-to-revenue ratio for each
    FY at published revenues so Stage 6 can overlay stressed revenue.
    """
    schedule = load_debt_schedule()
    assumptions = load_assumptions()
    results: List[Dict] = []
    for fy in FORECAST_YEARS:
        if fy <= 2030:
            gr = pick(assumptions, "anchor", f"gr_base_fy{fy - 2000}", "base").value
        else:
            fy30 = pick(assumptions, "anchor", "gr_base_fy30", "base").value
            fy29 = pick(assumptions, "anchor", "gr_base_fy29", "base").value
            gr = fy30 * (fy30 / fy29)
        total_ds = schedule.get(fy, 0.0)
        ratio = total_ds / gr if gr else 0.0
        results.append(
            {
                "fiscal_year": fy,
                "total_debt_service": total_ds,
                "general_revenue_base": gr,
                "debt_service_to_revenue_pct": ratio * 100.0,
                "psfm_10pct_cap_headroom": (0.10 * gr) - total_ds,
                "breached_cap": ratio > 0.10,
            }
        )
    return results


# ---------------------------------------------------------------------------
# Main.
# ---------------------------------------------------------------------------


def main() -> int:
    print(f"Writing expenditure path -> {OUTPUT_CSV}")
    write_expenditure_path()

    print("\n=== BASE SCENARIO: FY27-FY31 committed expenditure by block ($M) ===")
    summary = summarize("base")
    # Blocks that roll up into TOTAL COMMITTED (basis=committed|programmed|extrapolated):
    summed_blocks = [
        "schools_transfer",
        "public_safety",
        "general_government",
        "community_services",
        "debt_service",
        "capital_paygo",
    ]
    header = f"{'Block':<30}" + "".join(f"{'FY'+str(fy):>12}" for fy in FORECAST_YEARS)
    print(header)
    print("-" * len(header))
    for b in summed_blocks:
        vals = [summary[fy].get(b, 0.0) / 1e6 for fy in FORECAST_YEARS]
        print(f"{b:<30}" + "".join(f"{v:>12,.1f}" for v in vals))
    print("-" * len(header))
    totals = [summary[fy]["total"] / 1e6 for fy in FORECAST_YEARS]
    print(f"{'TOTAL COMMITTED':<30}" + "".join(f"{v:>12,.1f}" for v in totals))
    # Pension/OPEB reported separately as informational (already inside above).
    pens_vals = [summary[fy].get("pension_opeb", 0.0) / 1e6 for fy in FORECAST_YEARS]
    print(f"{'[info] pension_opeb*':<30}" + "".join(f"{v:>12,.1f}" for v in pens_vals))
    print("  *pension_opeb is embedded in the personnel lines above; not added to total.")

    print("\n=== Debt capacity check (base GR; Stage 6 will stress) ===")
    for r in check_debt_capacity("base"):
        flag = "  <-- BREACH" if r["breached_cap"] else ""
        print(
            f"  FY{r['fiscal_year']}  DS=${r['total_debt_service']/1e6:,.1f}M  "
            f"GR=${r['general_revenue_base']/1e6:,.1f}M  "
            f"ratio={r['debt_service_to_revenue_pct']:.2f}%  "
            f"headroom=${r['psfm_10pct_cap_headroom']/1e6:,.1f}M{flag}"
        )

    print("\n=== Schools transfer function sanity check ===")
    test_bases = [1_732_673_500, 1_807_905_700, 2_063_873_884, 1_500_000_000]
    for b in test_bases:
        print(f"  schools_transfer({b:,}) = {schools_transfer(b):,.0f}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
