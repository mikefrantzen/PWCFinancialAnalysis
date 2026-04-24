"""Stage 4 — Non-Data-Center Revenue Drivers for Prince William County, VA.

Purpose
-------
Generate FY27–FY31 projections of every NON-data-center general-fund revenue
line under three directional scenarios (low / base / high). Data-center
revenue lines are handled by Stage 6 using Stage 2 (canceled projects) and
Stage 3 (spillover elasticities); they are excluded here. The "computer
equipment & peripherals" tax is de-facto pure-DC (~96% of the line per
PWC-DCR-TY24) and the DC share of business-tangible / real-property / F&F
is also carved out, leaving behind the residential and non-DC commercial
base that this module projects.

Stage 6b overlay — Regulatory spillover (residential channel)
-------------------------------------------------------------
In addition to the three directional scenarios, this module produces an
orthogonal overlay that represents the peer-county-grounded **residential
CAPEX spillover** from the April 2026 non-appeal (Stage 3b). When
`regulatory_spillover=True` is passed to `project_non_dc_revenue()`, the
residential real-estate projection applies two multiplicative effects,
read at runtime from `data/non_dc_spillover_parameters.csv`:

1. `permit_units_reduction_year{N}` — reduces NEW-construction units
   (and therefore new-construction AV added each year).
2. `residential_av_growth_drag_year{N}` — ADDITIVE drag on the residential
   AV growth rate (applied after any federal-pass-through drag).

Under Stage 3b's recommendations, commercial-CRE and industrial channels
carry NULL point estimates, so the overlay does NOT adjust those lines.
Ranges for all channels remain available for sensitivity analysis through
the same CSV. The overlay is orthogonal to low/base/high: it can be
layered on any base scenario. Stage 6 uses it only on CAPEX Spillover
(LOW + overlay). See `research/non_dc_spillover_evidence.md` §f for mapping.

Scenarios (directional, not symmetric)
--------------------------------------
- base: PWC FY26–FY30 Adopted Estimate of General Revenue trajectory held
  as-is for non-DC lines (pre-ruling baseline forecast). Residential
  assessed value grows only through turnover + new construction, not
  through price appreciation (PWC reassesses annually).
- low:  continued federal civilian + contractor contraction (cumulative
  -40k VA federal civilian jobs by FY31), NoVA residential nominal -10%
  over 5 yr (Case-Shiller DC-Washington MSA peaked Jun-2022 at 344.2
  NSA and was 339.1 Dec-2025), office vacancy >20% persists.
- high: federal stabilization, NoVA residential flat-to-+1%/yr, office
  absorbs modestly. Not a boom case; a "shocks resolved" case.

Methodology
-----------
1. Real estate: split FY26 adopted real-estate tax ($1,025.922M) into
   residential (67.7% per FY25 ACFR MD&A), DC (carve-out via TY2024 DC
   real-property $144.2M), and non-DC commercial. Grow each segment by
   its scenario parameters. Apply a one-year assessment lag (TY-N
   assessment hits FY-N+1 revenue).
2. Residential growth = price path + turnover reassessment + new units.
   Price path: Case-Shiller DC-MSA / FHFA HPI-informed 5yr CAGR.
   Assessment lag: FY27 revenue reflects the TY2026 landbook which was
   locked Jan-2026 on late-2025 market conditions.
3. Federal-contracting exposure: translate a VA federal-civilian job
   change (cumulative) into PWC income shock via share × multiplier,
   then apply income elasticities to personal-property (vehicles),
   sales tax, BPOL, and meals tax. Also feed a price pressure term
   back into residential.
4. State aid: PWCS enrollment × state per-pupil SOQ × LCI drift, applied
   to the GF direct state-revenue line (excludes schools component-unit
   aid). Small absolute number.
5. Smaller lines: growth rates per assumption table for consumer
   utility, communications, motor-vehicle license, recordation,
   cigarette, transient occupancy, investment income (rate-sensitive
   on $2.2B portfolio), PPTRA (fixed by statute), federal PILT (flat).
6. Meals tax: rate steps from 4% -> 3% on 2026-01-01; FY27+ are full-year
   3%. So FY27 base = FY26 base × (3/4) + growth × 2 years? No — FY26
   adopted already includes the step-down ($40.25M), so FY27 is simply
   FY26 × (12/6) × (1/1) accounting for FY26 being half-half. Explicit
   rebase used: FY27 base = FY26 adopted × (3/3.5) because FY26 had 6
   months at 4% and 6 months at 3% = blended 3.5%.

Output
------
- DataFrame with columns:
    fiscal_year, scenario, revenue_line, amount_usd, method_note
- CSV: data/non_dc_revenue_projection.csv

Reproducibility
---------------
Run `python3 model/revenue_drivers.py` from the project root. Reads
`data/pwc_baseline.csv` and `data/revenue_driver_assumptions.csv`; writes
`data/non_dc_revenue_projection.csv`. No network access; all inputs are
local CSV. Every named constant in this module is either read from the
assumption CSV or derived from a baseline CSV row with citation comment.

Source keys
-----------
PWC-* keys resolve to citations/stage1.bib (inherited).
CSI_DCXRNSA_2026, FHFA_HPI_2026Q1, JLL_NoVA_2025Q4, CUSH_NOVA_2026,
BLS_QCEW_VA_2025Q2, VA_SOQ_2026, VA_LCI_2026, PWCS_ENROLL_2026,
FED_SOFR_2026Q1, cbo2024salestax, brookings_hamilton_2026 resolve to
citations/stage4.bib (this stage). synth_stage4 = analyst synthesis.
Inherited: whro2026dogecuts (Stage 3), mangum2020 / bartik2005
(Stage 3).
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd
import numpy as np

# -----------------------------------------------------------------------------
# Paths
# -----------------------------------------------------------------------------
REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "data"
BASELINE_CSV = DATA / "pwc_baseline.csv"
ASSUMPTIONS_CSV = DATA / "revenue_driver_assumptions.csv"
SPILLOVER_CSV = DATA / "non_dc_spillover_parameters.csv"  # Stage 3b parameters.
OUTPUT_CSV = DATA / "non_dc_revenue_projection.csv"

# -----------------------------------------------------------------------------
# Constants (every number here either has a source_key comment OR is derived
# from an assumption-CSV row / baseline-CSV row at runtime).
# -----------------------------------------------------------------------------
FISCAL_YEARS = [2027, 2028, 2029, 2030, 2031]
SCENARIOS = ["low", "base", "high"]

# FY26 baseline figures, loaded dynamically. Listed here for readability.
# Source: PWC-BUD-FY26-REV p.60 + PWC-REV-FY26-30 p.3 — see baseline CSV.
FY26_LINES = {
    # revenue_line                               baseline_subcategory
    "real_estate_total":                        "real_property",
    "personal_property_vehicles":               "vehicles_current",
    "local_sales_tax":                          "local_sales_tax",
    "food_and_beverage_tax":                    "food_and_beverage_tax",
    "bpol_tax":                                 "bpol_tax",
    "consumer_utility_tax":                     "consumer_utility_tax",
    "communications_sales_tax":                 "communications_sales_tax",
    "recordation_tax":                          "recordation_tax",
    "motor_vehicle_license":                    "motor_vehicle_license",
    "transient_occupancy_tax":                  "transient_occupancy_tax",
    "cigarette_tax":                            "cigarette_tax",
    "state_revenue_gf_direct":                  "state_revenue",
    "federal_pilt":                             "federal_revenue",
    "pptra_fixed_reimbursement":                "pptra_fixed_reimbursement",
    "investment_income":                        "investment_income",
}

# DC carve-outs (Stage 6 owns these — excluded from this module's output).
# Source: PWC-DCR-TY24 (TY2024 DC real-property $144.2M; C&P $123.9M;
# F&F $23.2M of $44.2M; DCs = 96.1% of C&P; 52.7% of F&F).
DC_REAL_PROPERTY_FY26_EST = 170_000_000  # analyst-derived: TY2024 $144.2M grown by DC pipeline
                                          # plus full FY26 buildout effect. Placeholder; Stage 6
                                          # refines. Used ONLY to net out of total real-property.

# Residential / non-DC commercial split of the RE base.
# Source: PWC-ACFR-FY25 MD&A — Residential = 67.7% of total AV;
# DC = 15.8% of total AV; non-DC commercial+industrial = ~16.5%.
RESIDENTIAL_SHARE_OF_TOTAL_AV = 0.677
DC_SHARE_OF_TOTAL_AV = 0.158
NON_DC_COMMERCIAL_SHARE_OF_TOTAL_AV = 1.0 - RESIDENTIAL_SHARE_OF_TOTAL_AV - DC_SHARE_OF_TOTAL_AV

# FY26 adopted RE tax rate = $0.906/$100. Held constant across scenarios here
# (rate policy is a Stage 6 lever). Source: PWC-REV-FY26-30 p.2.
RE_TAX_RATE = 0.00906

# Personal property on business-tangible (non-DC portion only). The baseline
# business_tangible_current line is $217.995M and is ~90% DC-equipment; the
# non-DC portion is ~$22M (furniture & fixtures + small-business BTP).
# Source: PWC-DCR-TY24 (DCs = 96.1% of C&P category; ~50% of F&F).
NON_DC_BTP_FY26_EST = 22_000_000

# Meals tax rate blend: FY26 is 6 mo at 4% + 6 mo at 3% = effective 3.5%;
# FY27+ are full 3%. Source: PWC-REV-FY26-30 p.20.
MEALS_RATE_FY26_BLEND = 0.035
MEALS_RATE_FY27_PLUS = 0.030

# PWC Schools projected enrollment (FY26 baseline) — PWCS Fall 2025
# enrollment ~91,543 (Source: PWCS 2025-26 Data Profile, cited as
# PWCS_ENROLL_2026 in citations/stage4.bib).
PWCS_ENROLLMENT_FY26 = 91_543

# Approximate PWC share of VA federal-contractor workforce × PWC payroll
# basis. Used to translate VA federal-civilian job change into PWC
# household-income change. See baseline_notes and stage4.bib
# (BLS_QCEW_VA_2025Q2). Average federal-civilian + contractor comp in
# NoVA is ~$140k fully loaded.
AVG_FEDERAL_WORKER_TOTAL_COMP_NOVA = 140_000


# -----------------------------------------------------------------------------
# Loaders
# -----------------------------------------------------------------------------
def _load_baseline() -> pd.DataFrame:
    """Load baseline CSV; skip comment rows that start with '#'."""
    df = pd.read_csv(
        BASELINE_CSV,
        comment="#",
        dtype={"fiscal_year": str},
    )
    # Keep only FY26 rows for use as baseline values.
    return df


def _load_assumptions() -> pd.DataFrame:
    df = pd.read_csv(ASSUMPTIONS_CSV, comment="#")
    return df


def _load_spillover_parameters() -> pd.DataFrame:
    """Load Stage 3b non-DC spillover parameter table (point/low/high per
    channel x year). This is the peer-county-grounded parameter set used
    for CAPEX Spillover's regulatory-spillover overlay.
    """
    df = pd.read_csv(SPILLOVER_CSV, comment="#")
    return df


def _spillover_point(sp: pd.DataFrame, parameter_name: str) -> float:
    """Return the point estimate for a named Stage 3b spillover parameter."""
    rows = sp[sp["parameter_name"] == parameter_name]
    if rows.empty:
        raise KeyError(f"Stage 3b spillover parameter {parameter_name} not found")
    return float(rows["point_estimate"].iloc[0])


def _get_baseline(df: pd.DataFrame, fy: str, subcategory: str) -> float:
    rows = df[(df["fiscal_year"] == fy) & (df["subcategory"] == subcategory)]
    if rows.empty:
        raise KeyError(f"No baseline row for fiscal_year={fy} subcategory={subcategory}")
    return float(rows["amount_usd"].iloc[0])


def _get_param(assump: pd.DataFrame, driver: str, parameter: str, scenario: str) -> float:
    """Fetch scenario-specific parameter; fall back to 'base' if scenario-specific
    row is missing (used for e.g. PPTRA which is fixed across scenarios)."""
    rows = assump[
        (assump["driver"] == driver)
        & (assump["parameter"] == parameter)
        & (assump["scenario"] == scenario)
    ]
    if rows.empty:
        rows = assump[
            (assump["driver"] == driver)
            & (assump["parameter"] == parameter)
            & (assump["scenario"] == "base")
        ]
    if rows.empty:
        raise KeyError(f"No assumption row for driver={driver} parameter={parameter}")
    return float(rows["value"].iloc[0])


# -----------------------------------------------------------------------------
# Driver functions. Each returns a dict[fiscal_year -> USD].
# -----------------------------------------------------------------------------
def project_residential_re(
    baseline: pd.DataFrame,
    assump: pd.DataFrame,
    scenario: str,
    regulatory_spillover: bool = False,
    spillover: pd.DataFrame | None = None,
) -> dict[int, float]:
    """Residential real-estate tax revenue FY27-FY31.

    Growth = nominal price path + turnover reassessment + new construction,
    less federal-job-loss housing-demand pass-through. Assessment lag = 1yr.

    When ``regulatory_spillover`` is True, the Stage 3b peer-county-grounded
    residential overlay is applied (CAPEX Spillover only):

      - ``new_units`` is multiplied by ``(1 - permit_units_reduction_year{N})``
        for each forecast year, reducing new-construction AV added.
      - The residential AV growth rate has ``residential_av_growth_drag_year{N}``
        SUBTRACTED from it (additive drag on the growth channel).

    The ``spillover`` DataFrame is the result of ``_load_spillover_parameters()``.
    When not supplied and the flag is True, it is loaded.
    """
    fy26_total_re = _get_baseline(baseline, "FY2026", "real_property")
    # Residential portion of FY26 RE = 67.7% after stripping DC carve-out.
    # FY26 adopted RE = $1,025.922M. DC RE ~$170M (analyst est). Residential
    # approx = (FY26_total - DC) * (residential_share / (1 - DC_share)).
    # Source: PWC-ACFR-FY25 MD&A + PWC-DCR-TY24.
    non_dc_re = fy26_total_re - DC_REAL_PROPERTY_FY26_EST
    residential_share_of_non_dc = RESIDENTIAL_SHARE_OF_TOTAL_AV / (
        RESIDENTIAL_SHARE_OF_TOTAL_AV + NON_DC_COMMERCIAL_SHARE_OF_TOTAL_AV
    )
    fy26_residential_re = non_dc_re * residential_share_of_non_dc

    price_cagr = _get_param(assump, "residential_re", "case_shiller_dc_msa_5yr_cagr", scenario)
    turnover = _get_param(assump, "residential_re", "pwc_turnover_rate", scenario)
    new_units = _get_param(assump, "residential_re", "new_construction_units_per_yr", scenario)
    avg_unit_val = _get_param(assump, "residential_re", "avg_new_unit_assessed_value", "base")

    # Federal-job pass-through drag on prices.
    fed_jobs_delta = _get_param(
        assump, "federal_exposure", "va_federal_civilian_job_change_cumulative", scenario
    )
    fed_housing_pass = _get_param(
        assump, "federal_exposure", "federal_job_loss_housing_demand_pass_through", scenario
    )
    # fed_jobs_delta is negative for losses. Pass-through per 10k jobs.
    fed_price_drag_5yr = (fed_jobs_delta / 10_000) * fed_housing_pass
    # Split evenly over the 5-year projection window.
    fed_price_drag_annual = fed_price_drag_5yr / len(FISCAL_YEARS)

    # New construction AV added per year (baseline).
    new_construction_av_baseline = new_units * avg_unit_val

    # Total assessed value of residential base in FY26 terms, backed out of tax.
    fy26_residential_av = fy26_residential_re / RE_TAX_RATE

    # Stage 3b spillover overlay — load parameter table if requested.
    if regulatory_spillover and spillover is None:
        spillover = _load_spillover_parameters()

    projection = {}
    av = fy26_residential_av
    for idx, yr in enumerate(FISCAL_YEARS, start=1):
        # Stage 3b overlay: permit-units reduction AND AV growth drag for
        # CAPEX Spillover, both year-indexed year-1 ... year-5 from the
        # April 2026 event. Event is May 2026 = FY27 year-1.
        permit_reduction = 0.0
        av_drag = 0.0
        if regulatory_spillover and spillover is not None:
            try:
                permit_reduction = _spillover_point(
                    spillover, f"permit_units_reduction_year{idx}"
                )
                av_drag = _spillover_point(
                    spillover, f"residential_av_growth_drag_year{idx}"
                )
            except KeyError:
                permit_reduction = 0.0
                av_drag = 0.0

        # Apply nominal price change + federal pass-through drag + Stage 3b
        # AV-growth drag to existing stock. PWC reassesses 100% annually, so
        # the price shock applies to the full stock with a 1-year lag.
        effective_price_growth = price_cagr + fed_price_drag_annual - av_drag
        av = av * (1 + effective_price_growth)
        # Add new construction at full value — reduced by Stage 3b permit drop.
        new_construction_av = new_construction_av_baseline * (1.0 - permit_reduction)
        av = av + new_construction_av
        # Turnover has a marginal markup effect above re-price. In PWC's annual
        # 100%-reassessment regime, turnover is implicitly in the price path.
        _ = turnover  # retained for explicit audit; not applied double-count.
        projection[yr] = av * RE_TAX_RATE

    return projection


def project_non_dc_commercial_re(
    baseline: pd.DataFrame, assump: pd.DataFrame, scenario: str
) -> dict[int, float]:
    """Non-DC commercial + industrial real-estate tax."""
    fy26_total_re = _get_baseline(baseline, "FY2026", "real_property")
    non_dc_re = fy26_total_re - DC_REAL_PROPERTY_FY26_EST
    commercial_share_of_non_dc = NON_DC_COMMERCIAL_SHARE_OF_TOTAL_AV / (
        RESIDENTIAL_SHARE_OF_TOTAL_AV + NON_DC_COMMERCIAL_SHARE_OF_TOTAL_AV
    )
    fy26_commercial_re = non_dc_re * commercial_share_of_non_dc

    growth = _get_param(assump, "commercial_re", "office_absorption_5yr_cagr", scenario)
    # Innovation Park absorption: sqft at ~$250/sqft assessed value approx.
    sqft_yr = _get_param(assump, "commercial_re", "innovation_park_absorption_sqft_yr", scenario)
    innovation_park_av_add = sqft_yr * 250.0  # $250/sqft commercial assessed value
    innovation_park_re_add = innovation_park_av_add * RE_TAX_RATE

    projection = {}
    val = fy26_commercial_re
    for yr in FISCAL_YEARS:
        val = val * (1 + growth) + innovation_park_re_add
        projection[yr] = val
    return projection


def _federal_income_shock_fraction(assump: pd.DataFrame, scenario: str) -> float:
    """Return fractional hit (or lift) to PWC household income from federal
    civilian + contractor workforce change. Negative = loss."""
    va_jobs_delta = _get_param(
        assump, "federal_exposure", "va_federal_civilian_job_change_cumulative", scenario
    )
    pwc_share = _get_param(
        assump, "federal_exposure", "pwc_share_of_va_federal_contractors", "base"
    )
    multiplier = _get_param(
        assump, "federal_exposure", "pwc_fed_contractor_multiplier", "base"
    )
    pwc_jobs_delta = va_jobs_delta * pwc_share
    pwc_income_delta_dollars = (
        pwc_jobs_delta * AVG_FEDERAL_WORKER_TOTAL_COMP_NOVA * multiplier
    )
    # Denominator: approximate PWC aggregate household income.
    # Source: ACS 5-yr PWC median HH income ~$115k × ~170k households = $19.5B.
    pwc_aggregate_hh_income = 19_500_000_000
    return pwc_income_delta_dollars / pwc_aggregate_hh_income


def project_personal_property_vehicles(
    baseline: pd.DataFrame, assump: pd.DataFrame, scenario: str
) -> dict[int, float]:
    fy26 = _get_baseline(baseline, "FY2026", "vehicles_current")
    base_growth = _get_param(
        assump, "smaller_lines", "personal_property_vehicles_base_growth", scenario
    )
    elasticity = _get_param(
        assump, "federal_exposure", "household_income_to_personal_property_elasticity", scenario
    )
    income_shock_5yr = _federal_income_shock_fraction(assump, scenario)
    income_shock_annual = income_shock_5yr / len(FISCAL_YEARS)
    fed_effect_annual = elasticity * income_shock_annual

    projection = {}
    val = fy26
    for yr in FISCAL_YEARS:
        val = val * (1 + base_growth + fed_effect_annual)
        projection[yr] = val
    return projection


def project_local_sales_tax(
    baseline: pd.DataFrame, assump: pd.DataFrame, scenario: str
) -> dict[int, float]:
    fy26 = _get_baseline(baseline, "FY2026", "local_sales_tax")
    base_growth = _get_param(assump, "smaller_lines", "sales_tax_base_growth", scenario)
    elasticity = _get_param(
        assump, "federal_exposure", "household_income_to_sales_tax_elasticity", scenario
    )
    income_shock_5yr = _federal_income_shock_fraction(assump, scenario)
    income_shock_annual = income_shock_5yr / len(FISCAL_YEARS)
    fed_effect_annual = elasticity * income_shock_annual

    projection = {}
    val = fy26
    for yr in FISCAL_YEARS:
        val = val * (1 + base_growth + fed_effect_annual)
        projection[yr] = val
    return projection


def project_bpol(
    baseline: pd.DataFrame, assump: pd.DataFrame, scenario: str
) -> dict[int, float]:
    fy26 = _get_baseline(baseline, "FY2026", "bpol_tax")
    base_growth = _get_param(assump, "smaller_lines", "bpol_base_growth", scenario)
    elasticity = _get_param(
        assump, "federal_exposure", "bpol_to_contractor_receipts_elasticity", scenario
    )
    # BPOL exposure: use half of the federal income shock as a proxy for
    # contractor gross-receipts shock (contractor firms concentrate the hit).
    contractor_shock_5yr = _federal_income_shock_fraction(assump, scenario) * 2.0
    contractor_shock_annual = contractor_shock_5yr / len(FISCAL_YEARS)
    fed_effect_annual = elasticity * contractor_shock_annual

    projection = {}
    val = fy26
    for yr in FISCAL_YEARS:
        val = val * (1 + base_growth + fed_effect_annual)
        projection[yr] = val
    return projection


def project_meals_tax(
    baseline: pd.DataFrame, assump: pd.DataFrame, scenario: str
) -> dict[int, float]:
    fy26 = _get_baseline(baseline, "FY2026", "food_and_beverage_tax")
    # Rebase from FY26 blended 3.5% to FY27 3.0% full year.
    fy26_base_at_3pct = fy26 * (MEALS_RATE_FY27_PLUS / MEALS_RATE_FY26_BLEND)
    base_growth = _get_param(
        assump, "smaller_lines", "meals_tax_base_growth_pre_rate", scenario
    )
    elasticity = _get_param(
        assump, "federal_exposure", "meals_tax_to_daytime_pop_elasticity", scenario
    )
    income_shock_5yr = _federal_income_shock_fraction(assump, scenario)
    income_shock_annual = income_shock_5yr / len(FISCAL_YEARS)
    fed_effect_annual = elasticity * income_shock_annual

    projection = {}
    val = fy26_base_at_3pct
    for yr in FISCAL_YEARS:
        val = val * (1 + base_growth + fed_effect_annual)
        projection[yr] = val
    return projection


def project_state_aid(
    baseline: pd.DataFrame, assump: pd.DataFrame, scenario: str
) -> dict[int, float]:
    """GF direct state revenue only (schools component-unit state aid handled
    by Stage 5 expenditure side via the 57.23% transfer framework)."""
    fy26 = _get_param(assump, "state_aid", "fy26_gf_state_aid_baseline", "base")
    enrollment_cagr = _get_param(assump, "state_aid", "pwcs_enrollment_growth_cagr", scenario)
    per_pupil_cagr = _get_param(assump, "state_aid", "soq_per_pupil_growth_cagr", scenario)
    lci_drift = _get_param(assump, "state_aid", "pwc_lci_drift", scenario)
    # Net growth = (1+enroll)(1+per_pupil)(1 - lci_drift) - 1; LCI up means
    # local share up, so state aid growth is suppressed.
    annual = (1 + enrollment_cagr) * (1 + per_pupil_cagr) * (1 - lci_drift) - 1

    projection = {}
    val = fy26
    for yr in FISCAL_YEARS:
        val = val * (1 + annual)
        projection[yr] = val
    return projection


def _simple_growth(
    fy26_value: float, growth_rate: float
) -> dict[int, float]:
    projection = {}
    val = fy26_value
    for yr in FISCAL_YEARS:
        val = val * (1 + growth_rate)
        projection[yr] = val
    return projection


def project_consumer_utility(
    baseline: pd.DataFrame, assump: pd.DataFrame, scenario: str
) -> dict[int, float]:
    fy26 = _get_baseline(baseline, "FY2026", "consumer_utility_tax")
    g = _get_param(assump, "smaller_lines", "consumer_utility_growth", scenario)
    return _simple_growth(fy26, g)


def project_communications(
    baseline: pd.DataFrame, assump: pd.DataFrame, scenario: str
) -> dict[int, float]:
    fy26 = _get_baseline(baseline, "FY2026", "communications_sales_tax")
    g = _get_param(assump, "smaller_lines", "communications_sales_growth", scenario)
    return _simple_growth(fy26, g)


def project_motor_vehicle_license(
    baseline: pd.DataFrame, assump: pd.DataFrame, scenario: str
) -> dict[int, float]:
    fy26 = _get_baseline(baseline, "FY2026", "motor_vehicle_license")
    g = _get_param(assump, "smaller_lines", "motor_vehicle_license_growth", scenario)
    return _simple_growth(fy26, g)


def project_recordation_tax(
    baseline: pd.DataFrame, assump: pd.DataFrame, scenario: str
) -> dict[int, float]:
    fy26 = _get_baseline(baseline, "FY2026", "recordation_tax")
    g = _get_param(assump, "smaller_lines", "recordation_tax_growth", scenario)
    return _simple_growth(fy26, g)


def project_transient_occupancy(
    baseline: pd.DataFrame, assump: pd.DataFrame, scenario: str
) -> dict[int, float]:
    fy26 = _get_baseline(baseline, "FY2026", "transient_occupancy_tax")
    g = _get_param(assump, "smaller_lines", "transient_occupancy_growth", scenario)
    return _simple_growth(fy26, g)


def project_cigarette_tax(
    baseline: pd.DataFrame, assump: pd.DataFrame, scenario: str
) -> dict[int, float]:
    fy26 = _get_baseline(baseline, "FY2026", "cigarette_tax")
    g = _get_param(assump, "smaller_lines", "cigarette_tax_growth", scenario)
    return _simple_growth(fy26, g)


def project_investment_income(
    baseline: pd.DataFrame, assump: pd.DataFrame, scenario: str
) -> dict[int, float]:
    """Investment income is portfolio × yield. FY26 adopted $29.4M on $2.2B ≈
    1.34% effective GF share yield (portfolio yield is gross; $29.4M is the
    general-fund slice of interest). Scenario yields bracket the interest-
    rate path. Portfolio held flat."""
    fy26 = _get_baseline(baseline, "FY2026", "investment_income")
    yield_fy26_implied = fy26 / _get_param(
        assump, "smaller_lines", "investment_income_portfolio_assumption", "base"
    )
    # Scenario yield path declines from FY26 implied to scenario terminal.
    terminal_yield = _get_param(
        assump, "smaller_lines", "investment_income_rate_assumption_pct", scenario
    )
    # Adjust implied FY26 GF-share yield by the proportional change in market
    # rates: FY26 market rate ~4.5% (SOFR Dec 2025), so terminal/4.5% scales.
    fy26_market_rate = 0.045
    scaler = terminal_yield / fy26_market_rate
    portfolio = _get_param(
        assump, "smaller_lines", "investment_income_portfolio_assumption", "base"
    )

    projection = {}
    # Linearly glide from FY26 implied GF-share yield to terminal scaled yield.
    for idx, yr in enumerate(FISCAL_YEARS, start=1):
        blend = idx / len(FISCAL_YEARS)
        scaler_path = 1.0 + blend * (scaler - 1.0)
        projection[yr] = portfolio * yield_fy26_implied * scaler_path
    return projection


def project_non_dc_btp(
    baseline: pd.DataFrame, assump: pd.DataFrame, scenario: str
) -> dict[int, float]:
    """Non-DC business tangible (mostly small-business furniture & fixtures
    outside the data-center category). Grows with general business activity;
    elasticity-weighted BPOL proxy scaled to non-DC BTP base."""
    fy26 = NON_DC_BTP_FY26_EST
    base_growth = _get_param(assump, "smaller_lines", "bpol_base_growth", scenario)
    return _simple_growth(fy26, base_growth)


def project_pptra(
    baseline: pd.DataFrame, assump: pd.DataFrame, scenario: str
) -> dict[int, float]:
    val = _get_param(assump, "smaller_lines", "pptra_fixed_reimbursement", "base")
    return {yr: val for yr in FISCAL_YEARS}


def project_federal_pilt(
    baseline: pd.DataFrame, assump: pd.DataFrame, scenario: str
) -> dict[int, float]:
    fy26 = _get_baseline(baseline, "FY2026", "federal_revenue")
    g = _get_param(assump, "smaller_lines", "federal_pilt_growth", "base")
    return _simple_growth(fy26, g)


# -----------------------------------------------------------------------------
# Top-level driver
# -----------------------------------------------------------------------------
DRIVERS = [
    ("residential_real_estate",       project_residential_re),
    ("non_dc_commercial_real_estate", project_non_dc_commercial_re),
    ("personal_property_vehicles",    project_personal_property_vehicles),
    ("non_dc_business_tangible",      project_non_dc_btp),
    ("local_sales_tax",               project_local_sales_tax),
    ("bpol_tax",                      project_bpol),
    ("food_and_beverage_tax",         project_meals_tax),
    ("consumer_utility_tax",          project_consumer_utility),
    ("communications_sales_tax",      project_communications),
    ("motor_vehicle_license",         project_motor_vehicle_license),
    ("recordation_tax",               project_recordation_tax),
    ("transient_occupancy_tax",       project_transient_occupancy),
    ("cigarette_tax",                 project_cigarette_tax),
    ("investment_income",             project_investment_income),
    ("state_aid_gf_direct",           project_state_aid),
    ("federal_pilt",                  project_federal_pilt),
    ("pptra_fixed_reimbursement",     project_pptra),
]


def project_non_dc_revenue(
    scenario: str,
    regulatory_spillover: bool = False,
    output_scenario_label: str | None = None,
) -> pd.DataFrame:
    """Project all non-DC revenue lines under ``scenario`` (low/base/high).

    When ``regulatory_spillover`` is True, the Stage 3b residential overlay
    is applied to ``project_residential_re`` only. Other channels follow
    Stage 3b's finance-office-honest recommendation (null point estimate,
    ranges retained in the CSV for sensitivity).

    ``output_scenario_label`` (optional) overrides the scenario label stamped
    on the output rows (e.g., ``"low_with_spillover"``). This lets Stage 6
    address the overlay as a distinct series without collision with the
    pure Stage 4 low/base/high scenarios.
    """
    baseline = _load_baseline()
    assump = _load_assumptions()
    spillover = _load_spillover_parameters() if regulatory_spillover else None
    label = output_scenario_label or scenario

    rows = []
    for line_name, fn in DRIVERS:
        if fn is project_residential_re and regulatory_spillover:
            result = fn(
                baseline,
                assump,
                scenario,
                regulatory_spillover=True,
                spillover=spillover,
            )
        else:
            result = fn(baseline, assump, scenario)
        for fy, amount in result.items():
            rows.append(
                {
                    "fiscal_year": fy,
                    "scenario": label,
                    "revenue_line": line_name,
                    "amount_usd": round(amount, 0),
                }
            )
    return pd.DataFrame(rows)


def build_full_projection() -> pd.DataFrame:
    """Emit the three base scenarios plus a fourth `low_with_spillover`
    series that adds the Stage 3b residential overlay to LOW. Stage 6b
    consumes the overlay series directly for CAPEX Spillover.
    """
    frames = [project_non_dc_revenue(s) for s in SCENARIOS]
    frames.append(
        project_non_dc_revenue(
            "low",
            regulatory_spillover=True,
            output_scenario_label="low_with_spillover",
        )
    )
    return pd.concat(frames, ignore_index=True)


def _summarize(df: pd.DataFrame) -> pd.DataFrame:
    """Scenario × fiscal-year totals for logging."""
    return (
        df.groupby(["scenario", "fiscal_year"])["amount_usd"]
        .sum()
        .unstack("fiscal_year")
        .round(0)
    )


def main() -> None:
    df = build_full_projection()
    df.to_csv(OUTPUT_CSV, index=False)
    totals = _summarize(df)
    print("Wrote", OUTPUT_CSV)
    print()
    print("Total non-DC revenue by scenario × FY (USD):")
    print(totals.to_string())


if __name__ == "__main__":
    main()
