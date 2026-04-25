"""
C&P Cure Scenario — fourth scenario layered on CAPEX Spillover.

Question:
  If the Board, faced with the CAPEX Spillover deficit, attempts to plug it
  entirely by raising the data-center Computer & Peripherals (C&P) tax rate
  above the FY27 adopted $4.50/$100, what rate is required year-by-year and
  does the resulting behavioral response collapse the C&P assessed-value base?

Inputs:
  - data/scenario_results.csv          CAPEX Spillover annual deficit
  - data/scenario_revenue_detail.csv   data_center_tax_revenue line
  - data/depreciation_schedule.csv     PWC Schedule C (50/35/20/10/5)
  - data/va_county_tax_stack.csv       Peer-county C&P rates

Behavioral parameters synthesized from:
  - research/location_elasticity_notes.md  (new-build elasticity per +$1/$100
    differential vs Loudoun; refresh-cycle slowdown over time)
  - research/va_tax_competitive_notes.md   (tip-out thresholds: +$1 tolerated,
    +$2 inflection, +$5 leave-VA)
  - research/depreciation_regime_notes.md  (operator GAAP lives 5-6 yrs vs.
    PWC 4-yr-to-floor schedule)

Outputs land under data/cp_cure_*.csv.
"""
from __future__ import annotations

import csv
from pathlib import Path
from dataclasses import dataclass

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "data"
OUT_DIR = DATA
OUT_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# Constants — all sourced; see research/*.md for citations
# ---------------------------------------------------------------------------
FISCAL_YEARS = (2027, 2028, 2029, 2030, 2031)
CLIFF_YEARS = (2032, 2033, 2034, 2035, 2036)

# PWC Schedule C: % of original capitalized cost by age
# Source: PWC 2025 BTPP Return Form, Schedule C
SCHEDULE_C = [0.50, 0.35, 0.20, 0.10] + [0.05] * 30  # year 0, 1, 2, 3, 4+

# Loudoun reference rate (TY2026)
LOUDOUN_CP_RATE = 4.15  # $/$100 of AV
PWC_FY27_CP_RATE = 4.50  # $/$100, FY27 adopted
PWC_FY26_CP_RATE = 4.15  # FY26 prior

# Elasticity parameters (from research/location_elasticity_notes.md §6)
NEW_BUILD_ELASTICITY_PER_DOLLAR = 0.0125  # -1.25% per +$1 over Loudoun
REFRESH_SLOWDOWN_BY_YEAR = {  # cumulative slowdown of in-place refresh
    1: 0.003,   # year 1 of differential: -0.3% pa
    2: 0.005,   # year 2: -0.5%
    3: 0.005,
    4: 0.010,   # year 4+: -1.0%
    5: 0.010,
}
# Tip-out thresholds ($ above Loudoun)
TIP_OUT_TOLERATED = 1.00   # +$1 absorbed
TIP_OUT_INFLECTION = 2.00  # +$2 starts redirecting
TIP_OUT_LEAVE_VA = 5.00    # +$5 likely triggers out-of-state

# Sales-tax exemption probability of repeal/conditioning by FY28
# Source: research/va_tax_competitive_notes.md §1
P_EXEMPTION_REPEAL = 0.50  # bundled probability of any material tightening
EXEMPTION_LOSS_CAPEX_DRAG = 0.06  # 5-7% cost-stack increase reduces new builds proportionally

# TY2024 anchors (from PWC-DCR-TY24)
TY24_GROSS_BOOK = 15.68e9   # $15.68B reported gross capitalized C&P cost
TY24_DEPRECIATED_AV = 3.97e9  # $3.97B depreciated AV
TY24_CP_REVENUE = 123.9e6     # $123.9M at $3.70 rate

# CAPEX Spillover baseline annual NEW C&P CAPEX (gross capitalized $) —
# calibrated so AV trajectory matches CAPEX Spillover DC revenue ($486M FY27 →
# $578M FY31 at 55% C&P share at $4.50 → C&P AV ~$5.9B → ~$7.1B). Backsolved:
# steady-state new-CAPEX ≈ AV / sum(SCHEDULE_C) ≈ AV / 1.20 ≈ $5B/yr.
BASELINE_NEW_CP_CAPEX = {  # dollars per year, before elasticity
    2026: 4.5e9,
    2027: 4.7e9,
    2028: 4.9e9,
    2029: 5.1e9,
    2030: 5.3e9,
    2031: 5.5e9,
    2032: 5.5e9,
    2033: 5.5e9,
    2034: 5.5e9,
    2035: 5.5e9,
    2036: 5.5e9,
}

# Historical pre-2026 adds, calibrated so cumulative gross book ≈ $15.68B in
# TY24 (reported actual). Backsolved with ~10% YoY growth.
HISTORICAL_ADDS = {
    2020: 2.50e9,
    2021: 2.80e9,
    2022: 3.10e9,
    2023: 3.40e9,
    2024: 3.70e9,
    2025: 4.10e9,  # FY26 (TY25) — fills the gap to FY27 model start
}
# Sanity: 2.5+2.8+3.1+3.4+3.7 = 15.5B at TY24 (matches reported $15.68B within calibration)


# ---------------------------------------------------------------------------
# Core depreciation engine
# ---------------------------------------------------------------------------
@dataclass
class CohortBook:
    """Track gross capitalized cost by vintage year. Depreciated AV is computed
    on demand by applying SCHEDULE_C to (current_year - vintage)."""
    # vintage_year -> gross capitalized cost in dollars
    cohorts: dict[int, float]

    def total_av(self, current_year: int) -> float:
        total = 0.0
        for vintage, gross in self.cohorts.items():
            age = current_year - vintage
            if age < 0:
                continue
            factor = SCHEDULE_C[min(age, len(SCHEDULE_C) - 1)]
            total += gross * factor
        return total

    def add(self, vintage_year: int, gross: float):
        self.cohorts[vintage_year] = self.cohorts.get(vintage_year, 0.0) + gross


def initial_book() -> CohortBook:
    book = CohortBook(cohorts={})
    for v, g in HISTORICAL_ADDS.items():
        book.add(v, g)
    return book


# ---------------------------------------------------------------------------
# Elasticity model: how much new CAPEX is deterred at a given hike rate?
# ---------------------------------------------------------------------------
def new_capex_factor(rate_hike: float, year_of_hike: int = 1) -> float:
    """Multiplicative factor on new C&P CAPEX given a rate hike above Loudoun.

    Piecewise model based on observed regional thresholds (research/
    location_elasticity_notes.md and va_tax_competitive_notes.md):
      - 0 to $1 differential: 0% reduction (within tolerance band)
      - $1 to $2: linear 0% → 5% (Bisnow/operator commentary; tolerated)
      - $2 to $5: linear 5% → 30% (inflection; net-new redirected)
      - $5 to $10: linear 30% → 70% (leave-VA threshold crossed)
      - $10+: capped at 80% (existing fiber/peering lock-in keeps some CAPEX)
    Year-1 response is partial; year 2+ allows full redirection.
    """
    d = max(0.0, rate_hike)
    if d <= TIP_OUT_TOLERATED:                 # ≤ $1
        long_run = 0.0
    elif d <= TIP_OUT_INFLECTION:              # $1 - $2
        long_run = 0.05 * (d - 1.0)
    elif d <= TIP_OUT_LEAVE_VA:                # $2 - $5
        long_run = 0.05 + (0.25) * (d - 2.0) / 3.0  # 5% to 30%
    elif d <= 10.0:                            # $5 - $10
        long_run = 0.30 + (0.40) * (d - 5.0) / 5.0  # 30% to 70%
    else:
        long_run = min(0.80, 0.70 + (d - 10.0) * 0.02)
    # Year-1 hike: only partial response (planning lag)
    year_factor = min(1.0, year_of_hike / 2.0)
    reduction = long_run * (0.5 + 0.5 * year_factor)
    return max(0.20, 1.0 - reduction)


def refresh_slowdown_factor(year_of_hike: int) -> float:
    """Multiplicative factor on the in-place refresh portion of new CAPEX
    (separate from net-new buildouts that are more redirectable)."""
    slow = REFRESH_SLOWDOWN_BY_YEAR.get(min(year_of_hike, 5), 0.010)
    return 1.0 - slow * year_of_hike  # cumulative


# ---------------------------------------------------------------------------
# Scenario simulator
# ---------------------------------------------------------------------------
def simulate_scenario(
    cp_rate_path: dict[int, float],
    new_capex_path: dict[int, float] | None = None,
    apply_elasticity: bool = True,
    apply_exemption_loss: bool = False,
) -> dict[int, dict[str, float]]:
    """Simulate C&P AV and revenue under a given rate path.

    Args:
        cp_rate_path: {year: rate $/$100}.
        new_capex_path: optional override for baseline new CAPEX (used for
            cliff scenarios where refresh halts).
        apply_elasticity: if True, behavioral response reduces new CAPEX.
        apply_exemption_loss: if True, additional VA-exemption-loss drag.

    Returns:
        {year: {"cp_av": ..., "cp_revenue": ..., "new_capex": ...}}
    """
    book = initial_book()
    base_capex = new_capex_path or BASELINE_NEW_CP_CAPEX
    results: dict[int, dict[str, float]] = {}
    hike_year_counter = 0

    for year in sorted(cp_rate_path.keys()):
        rate = cp_rate_path[year]
        rate_hike = rate - LOUDOUN_CP_RATE  # $ above Loudoun
        if rate_hike > TIP_OUT_TOLERATED and apply_elasticity:
            hike_year_counter += 1

        # New CAPEX this year
        new_capex = base_capex.get(year, base_capex[max(base_capex.keys())])
        if apply_elasticity:
            new_capex *= new_capex_factor(rate_hike, hike_year_counter)
            new_capex *= refresh_slowdown_factor(hike_year_counter)
        if apply_exemption_loss:
            new_capex *= (1.0 - EXEMPTION_LOSS_CAPEX_DRAG)

        book.add(year, new_capex)

        # Compute AV and revenue at this year's rate
        cp_av = book.total_av(year)
        cp_revenue = cp_av * rate / 100.0

        results[year] = {
            "cp_rate": rate,
            "rate_hike_above_loudoun": rate_hike,
            "new_capex_this_year": new_capex,
            "new_capex_factor_applied": new_capex / base_capex.get(year, base_capex[max(base_capex.keys())]),
            "cp_av": cp_av,
            "cp_revenue": cp_revenue,
        }

    return results


# ---------------------------------------------------------------------------
# Solver: find rate path that closes CAPEX Spillover deficit each year
# ---------------------------------------------------------------------------
def load_capex_spillover_deficit() -> dict[int, float]:
    """Read CAPEX Spillover annual deficit from public scenario_results.csv.
    READ-ONLY access to the public submodule."""
    path = DATA / "scenario_results.csv"
    out = {}
    with path.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["scenario"] != "CAPEX Spillover":
                continue
            if row["metric"] != "surplus_or_deficit":
                continue
            fy = int(row["fiscal_year"])
            if fy in FISCAL_YEARS:
                out[fy] = -float(row["value"])  # invert to positive deficit
    return out


def solve_required_rate(
    deficit_by_year: dict[int, float],
    schools_carve_out: bool = True,
    apply_elasticity: bool = True,
    apply_exemption_loss: bool = False,
    rate_cap: float = 25.0,
) -> dict[int, dict[str, float]]:
    """For each year, find the C&P rate at which the resulting C&P revenue
    (above the FY27 adopted baseline of $4.50) closes that year's deficit.

    Two treatments of Schools share:
      schools_carve_out=True: every $1 of incremental C&P revenue closes $1
        of deficit (extends Item 7-C precedent).
      schools_carve_out=False: only $0.4277 of each $1 closes deficit
        (Schools 57.23% claims the rest).
    """
    deficit_offset_factor = 1.0 if schools_carve_out else 0.4277

    results: dict[int, dict[str, float]] = {}
    book = initial_book()
    hike_year = 0

    # Baseline revenue at $4.50 (no hike) for reference
    baseline_run = simulate_scenario(
        {y: PWC_FY27_CP_RATE for y in FISCAL_YEARS},
        apply_elasticity=False,
    )

    # Iterate year by year, advancing book state
    for year in FISCAL_YEARS:
        target_deficit = deficit_by_year[year]
        baseline_rev = baseline_run[year]["cp_revenue"]
        baseline_av = baseline_run[year]["cp_av"]

        # Binary-search the rate
        lo, hi = PWC_FY27_CP_RATE, rate_cap
        best = None
        for _ in range(60):
            mid = (lo + hi) / 2
            # Build a one-shot simulate just for this year's stand-alone snapshot
            # (full path-dependent solve would compound rate-year-counter — we
            # use the cumulative hike year as years above tolerated band)
            rate_hike = mid - LOUDOUN_CP_RATE
            local_hike_year = max(1, year - 2026) if rate_hike > TIP_OUT_TOLERATED else 0

            # Effective AV under this rate, factoring elasticity
            new_capex_baseline = BASELINE_NEW_CP_CAPEX[year]
            if apply_elasticity:
                ncf = new_capex_factor(rate_hike, local_hike_year)
                rsf = refresh_slowdown_factor(local_hike_year)
                effective_capex = new_capex_baseline * ncf * rsf
            else:
                effective_capex = new_capex_baseline
            if apply_exemption_loss:
                effective_capex *= (1.0 - EXEMPTION_LOSS_CAPEX_DRAG)

            # AV: existing book at this year (depreciating) + new capex year-0
            existing_av = initial_book().total_av(year)
            # Plus prior years' new capex (baseline minus elasticity, stylized)
            # For simplicity, assume prior years also took elasticity hits at
            # this rate level (steady-state approximation)
            for v in range(2026, year):
                pv_capex = BASELINE_NEW_CP_CAPEX[v]
                if apply_elasticity:
                    pv_capex *= ncf * rsf
                if apply_exemption_loss:
                    pv_capex *= (1.0 - EXEMPTION_LOSS_CAPEX_DRAG)
                age = year - v
                existing_av += pv_capex * SCHEDULE_C[min(age, len(SCHEDULE_C) - 1)]
            total_av = existing_av + effective_capex * SCHEDULE_C[0]

            cp_revenue = total_av * mid / 100.0
            incremental_revenue = cp_revenue - baseline_rev
            deficit_closed = incremental_revenue * deficit_offset_factor

            if deficit_closed >= target_deficit:
                hi = mid
                best = (mid, total_av, cp_revenue, incremental_revenue, deficit_closed, ncf, rsf, effective_capex)
            else:
                lo = mid

        if best is None or hi >= rate_cap - 0.01:
            # Could not close the gap below the rate cap
            results[year] = {
                "required_rate": float("nan"),
                "feasible": False,
                "baseline_av_no_hike": baseline_av,
                "baseline_revenue_no_hike": baseline_rev,
                "target_deficit_M": target_deficit / 1e6,
                "note": f"INFEASIBLE: no rate <= ${rate_cap}/$100 closes the gap given elasticity",
            }
        else:
            mid, total_av, cp_revenue, incr, closed, ncf, rsf, effective_capex = best
            results[year] = {
                "required_rate": mid,
                "rate_hike_above_loudoun": mid - LOUDOUN_CP_RATE,
                "rate_hike_above_pwc_fy27": mid - PWC_FY27_CP_RATE,
                "feasible": True,
                "cp_av": total_av,
                "cp_revenue": cp_revenue,
                "baseline_av_no_hike": baseline_av,
                "baseline_revenue_no_hike": baseline_rev,
                "incremental_revenue_M": incr / 1e6,
                "deficit_closed_M": closed / 1e6,
                "target_deficit_M": target_deficit / 1e6,
                "new_capex_factor": ncf,
                "refresh_factor": rsf,
                "effective_new_capex_B": effective_capex / 1e9,
            }

    return results


# ---------------------------------------------------------------------------
# Cliff analysis: what happens FY32-FY36 if refresh halts at high rate?
# ---------------------------------------------------------------------------
def run_cliff_analysis(
    rate_after_fy31: float,
    refresh_halt_pct: float,
) -> dict[int, dict[str, float]]:
    """Project AV and revenue FY32-FY36 assuming new C&P CAPEX is suppressed.

    Args:
        rate_after_fy31: held-flat C&P rate from FY32 onward.
        refresh_halt_pct: 0.0 = full baseline new CAPEX continues; 0.5 = half;
            1.0 = full halt (worst case).
    """
    book = initial_book()
    # Run through FY26-FY31 at baseline (no hike) so we start FY32 with realistic AV
    for v in range(2026, 2032):
        book.add(v, BASELINE_NEW_CP_CAPEX[v])

    results = {}
    for year in CLIFF_YEARS:
        new_capex = BASELINE_NEW_CP_CAPEX[year] * (1.0 - refresh_halt_pct)
        book.add(year, new_capex)
        cp_av = book.total_av(year)
        cp_revenue = cp_av * rate_after_fy31 / 100.0
        results[year] = {
            "cp_av": cp_av,
            "cp_revenue": cp_revenue,
            "new_capex_this_year": new_capex,
            "rate": rate_after_fy31,
        }
    return results


# ---------------------------------------------------------------------------
# Output writers
# ---------------------------------------------------------------------------
def write_results_csv(results: dict, name: str, fieldnames: list[str]):
    path = OUT_DIR / name
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["fiscal_year"] + fieldnames)
        writer.writeheader()
        for year, row in sorted(results.items()):
            r = {"fiscal_year": year}
            for k in fieldnames:
                v = row.get(k)
                if isinstance(v, float):
                    r[k] = f"{v:.6f}"
                else:
                    r[k] = v if v is not None else ""
            writer.writerow(r)
    print(f"Wrote {path}")


def main():
    deficit = load_capex_spillover_deficit()
    print("=== CAPEX Spillover deficit to fill (annual, $M) ===")
    for y, d in sorted(deficit.items()):
        print(f"  FY{y}: ${d/1e6:>9,.1f}M")
    print(f"  Cumulative: ${sum(deficit.values())/1e6:,.0f}M")
    print()

    # ----- Solve A: carve-out, elasticity ON, no exemption loss -----
    print("=== Required C&P rate path (Schools carve-out, with elasticity) ===")
    res_a = solve_required_rate(
        deficit, schools_carve_out=True, apply_elasticity=True
    )
    for y, r in res_a.items():
        if r["feasible"]:
            print(f"  FY{y}: rate ${r['required_rate']:.2f}  (+${r['rate_hike_above_loudoun']:.2f} vs Loudoun, +${r['rate_hike_above_pwc_fy27']:.2f} vs FY27 adopted)")
            print(f"         elasticity factor: new-build {r['new_capex_factor']:.2%}, refresh {r['refresh_factor']:.2%}, effective new CAPEX ${r['effective_new_capex_B']:.2f}B")
        else:
            print(f"  FY{y}: {r['note']}")
    print()

    # ----- Solve B: Schools-shared, elasticity ON -----
    print("=== Required C&P rate path (Schools-shared 57.23%, with elasticity) ===")
    res_b = solve_required_rate(
        deficit, schools_carve_out=False, apply_elasticity=True
    )
    for y, r in res_b.items():
        if r["feasible"]:
            print(f"  FY{y}: rate ${r['required_rate']:.2f}  (+${r['rate_hike_above_loudoun']:.2f} vs Loudoun)")
        else:
            print(f"  FY{y}: {r['note']}")
    print()

    # ----- Solve C: carve-out + VA exemption loss -----
    print("=== Required C&P rate path (carve-out + 50%-prob VA exemption loss layered) ===")
    res_c = solve_required_rate(
        deficit, schools_carve_out=True, apply_elasticity=True, apply_exemption_loss=True
    )
    for y, r in res_c.items():
        if r["feasible"]:
            print(f"  FY{y}: rate ${r['required_rate']:.2f}")
        else:
            print(f"  FY{y}: {r['note']}")
    print()

    # ----- Cliff: held at $7 with 50% refresh halt -----
    print("=== Cliff scenario: $7.00 rate held FY32-FY36, 50% refresh halt ===")
    cliff_50 = run_cliff_analysis(rate_after_fy31=7.00, refresh_halt_pct=0.50)
    for y, r in cliff_50.items():
        print(f"  FY{y}: AV ${r['cp_av']/1e9:.2f}B, revenue ${r['cp_revenue']/1e6:>6,.1f}M")
    print()

    print("=== Cliff scenario: $7.00 rate held, FULL refresh halt ===")
    cliff_full = run_cliff_analysis(rate_after_fy31=7.00, refresh_halt_pct=1.00)
    for y, r in cliff_full.items():
        print(f"  FY{y}: AV ${r['cp_av']/1e9:.2f}B, revenue ${r['cp_revenue']/1e6:>6,.1f}M")
    print()

    # ----- Cliff at $10 -----
    print("=== Cliff scenario: $10.00 rate held FY32-FY36, FULL refresh halt ===")
    cliff_10 = run_cliff_analysis(rate_after_fy31=10.00, refresh_halt_pct=1.00)
    for y, r in cliff_10.items():
        print(f"  FY{y}: AV ${r['cp_av']/1e9:.2f}B, revenue ${r['cp_revenue']/1e6:>6,.1f}M")
    print()

    # Write all results to CSVs
    fields = [
        "required_rate", "rate_hike_above_loudoun", "rate_hike_above_pwc_fy27",
        "feasible", "cp_av", "cp_revenue", "incremental_revenue_M",
        "deficit_closed_M", "target_deficit_M", "new_capex_factor",
        "refresh_factor", "effective_new_capex_B", "note",
    ]
    write_results_csv(res_a, "cp_cure_carveout_with_elasticity.csv", fields)
    write_results_csv(res_b, "cp_cure_schools_shared_with_elasticity.csv", fields)
    write_results_csv(res_c, "cp_cure_carveout_with_exemption_loss.csv", fields)

    cliff_fields = ["cp_av", "cp_revenue", "new_capex_this_year", "rate"]
    write_results_csv(cliff_50, "cp_cure_cliff_rate7_halfrefresh.csv", cliff_fields)
    write_results_csv(cliff_full, "cp_cure_cliff_rate7_fullhalt.csv", cliff_fields)
    write_results_csv(cliff_10, "cp_cure_cliff_rate10_fullhalt.csv", cliff_fields)


if __name__ == "__main__":
    main()
