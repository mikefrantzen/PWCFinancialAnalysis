"""
Figure generator for the PWC Financial Analysis.

All figures are produced from committed artifacts under /data and /model and
labeled with source notes. Regenerate with:

    python3 figures/make_figures.py

Outputs:
    figures/fig_revenue_mix_fy26.png
    figures/fig_scenario_deficit.png
    figures/fig_required_tax_rate.png
    figures/fig_reserve_trajectory.png
    figures/fig_debt_service_ratio.png
    figures/fig_canceled_capex.png
    figures/fig_peer_county_permits.png     (Stage 3b)
    figures/fig_spillover_channels.png      (Stage 6b)
    figures/fig_revenue_hole.png            (shortfall + dept-level layoff panel)
    figures/fig_options_menu.png            (nine-option menu figure)

Assumptions, documented here and echoed in figure captions:
    TEACHER_COST_PER_YEAR = $90,000 fully loaded.
      Basis: PWC Public Schools published 2024-2025 average teacher base
      salary ~$75,000 (PWCS Board budget documents, teacher salary scale)
      plus ~20% benefits load (VRS 15.89% employer rate + retiree health
      credit + supplemental). $75K x 1.20 = $90K. Rounded low on purpose
      so the "teacher-equivalent" counts are defensible (a lower teacher
      cost produces a more arresting headcount number only if the cost is
      understated; here we chose the lower-bound defensible cost to keep
      the count honest rather than inflated). If the Finance Office
      substitutes the Adopted FY26 PWCS fully-loaded average of ~$100K,
      the teacher-equivalent counts fall ~10%, which does not change the
      order of magnitude of any comparison below.
    COUNTY_FTE_FULLY_LOADED = $115,000
      Basis: Stage 5 operating-reduction FTE math. $460M covered payroll
      / fringe-loaded $617M FY26 GF Salaries & Benefits (PWC-BUD-FY26-SUMM
      p.37) divided across ~5,400 GF FTE implied headcount.
    PWC_POLICE_BUDGET_FY26 = $160.67M  (PWC-BUD-FY26-EXP p.65)
    PWC_PUBLIC_SAFETY_FY26 = $420.40M  (PWC-BUD-FY26-EXP p.65-66 "Safe & Secure Community")
    PWC_SCHOOLS_TRANSFER_FY26 = $991.61M  (PWC-REV-FY26-30 p.2)
    PWC_MEDIAN_HOME_FY26 = $570,600  (PWC 2025 Real Estate Assessments Annual Report)
    PWC_MEDIAN_HOME_TAX_FY26 = $570,600 * 0.00906 = $5,170/yr
"""
from __future__ import annotations

import csv
import os
import textwrap
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "data"
OUT = REPO / "figures"
OUT.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "figure.dpi": 150,
    "savefig.dpi": 180,
    "font.size": 9,
    "axes.titlesize": 11,
    "axes.labelsize": 9,
    "axes.edgecolor": "#444",
    "axes.linewidth": 0.8,
    "axes.grid": True,
    "grid.linewidth": 0.4,
    "grid.color": "#cccccc",
    "legend.frameon": False,
})

DOLLAR = lambda x, _=None: f"${x:,.0f}"


# ---------- helpers ----------
def load_scenario_results():
    """Load /data/scenario_results.csv into dict[scenario][fy][metric] = value."""
    out: dict[str, dict[int, dict[str, float]]] = defaultdict(lambda: defaultdict(dict))
    with open(DATA / "scenario_results.csv") as f:
        rdr = csv.DictReader(f)
        for row in rdr:
            scen = row["scenario"]
            fy = int(row["fiscal_year"])
            met = row["metric"]
            try:
                val = float(row["value"])
            except ValueError:
                continue
            out[scen][fy][met] = val
    return out


SCENARIO_PRE_DG = "Pre-Cancellation Digital Gateway"
SCENARIO_SPILLOVER = "CAPEX Spillover"
SCENARIO_PARTIAL = "Partial Recovery"
SCENARIOS = [SCENARIO_PRE_DG, SCENARIO_SPILLOVER, SCENARIO_PARTIAL]

# Short forms used in charts where space is tight.
SCENARIO_LABEL = {
    SCENARIO_PRE_DG: "Pre-Cancel DG",
    SCENARIO_SPILLOVER: "CAPEX Spillover",
    SCENARIO_PARTIAL: "Partial Recovery",
}
SCENARIO_COLOR = {
    SCENARIO_PRE_DG: "#1f77b4",
    SCENARIO_SPILLOVER: "#d62728",
    SCENARIO_PARTIAL: "#2ca02c",
}


# ---------- fig 1: FY26 revenue mix, DC share highlighted ----------
def fig_revenue_mix_fy26():
    # From /research/baseline_notes.md §2 and Stage 1 table; DC share ~20% of the
    # split base via computer equipment + DC real property + DC BTFF; non-DC
    # remainder back-solves to the Stage 1 table.
    # We split the $1.733B split base into:
    #   - Real Estate (non-DC)  $855.9M  (residential + non-DC commercial)
    #   - Real Estate (DC)      $170.0M  (Stage 4 carve, TY2024 $144.2M -> $170M FY26)
    #   - Personal Property: vehicles $214.9M, DC CE&P ~$180M, non-DC BTFF ~$41.3M
    #   - Sales tax $102.5M
    #   - Meals $40.25M
    #   - BPOL $37.2M (some DC)
    #   - Investment income $29.4M
    #   - Other $62.2M (motor vehicle license, consumer utility, comms, all other)
    # Data-center components highlighted below via a darker bar-segment color.
    categories = [
        ("Real Estate, non-DC", 855.9, False),
        ("Real Estate, DC", 170.0, True),
        ("DC Computer Equip & Peripherals", 180.0, True),
        ("Personal Prop. vehicles", 214.9, False),
        ("Non-DC Business Tangible", 41.3, False),
        ("Local Sales Tax", 102.5, False),
        ("Meals (Food & Bev)", 40.25, False),
        ("BPOL", 37.17, False),
        ("Investment Income", 29.4, False),
        ("Other Local Taxes", 62.2, False),
    ]
    total = sum(v for _, v, _ in categories)
    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    x = list(range(len(categories)))
    colors = ["#b8860b" if dc else "#4e79a7" for _, _, dc in categories]
    ax.bar(x, [v for _, v, _ in categories], color=colors, edgecolor="#222", linewidth=0.6)
    for i, (_, v, _) in enumerate(categories):
        pct = v / total * 100
        ax.text(i, v + 12, f"${v:,.0f}M\n({pct:.1f}%)", ha="center", va="bottom", fontsize=7)
    ax.set_xticks(x)
    ax.set_xticklabels([c for c, _, _ in categories], rotation=35, ha="right", fontsize=7.5)
    ax.set_ylabel("USD, millions")
    ax.set_title(
        "FY26 Adopted General Revenue subject to 57.23% Schools split: $1,732.7M\n"
        "Data-center components (gold): ≈$350M ≈ 20% of the split base"
    )
    ax.set_ylim(0, max(v for _, v, _ in categories) * 1.18)
    import matplotlib.patches as mpatches
    legend = [
        mpatches.Patch(color="#4e79a7", label="Non-DC revenue"),
        mpatches.Patch(color="#b8860b", label="Data-center revenue"),
    ]
    ax.legend(handles=legend, loc="upper right", fontsize=8)
    ax.text(
        0.0,
        -0.26,
        "Source: PWC Adopted Budget FY26 (PWC-BUD-FY26-REV p.63); Estimate of General Revenue FY2026-2030 p.2; "
        "TY2024 PWC Data Center Revenue Report pp.22-24; Stage 1 baseline_notes.md §2.",
        transform=ax.transAxes,
        fontsize=6.8,
        ha="left",
        color="#444",
    )
    fig.tight_layout()
    fig.savefig(OUT / "fig_revenue_mix_fy26.png", bbox_inches="tight")
    plt.close(fig)


# ---------- fig 2: scenario deficit bars ----------
def fig_scenario_deficit(data):
    fys = [2027, 2028, 2029, 2030, 2031]
    width = 0.26
    x = [i for i in range(len(fys))]
    fig, ax = plt.subplots(figsize=(7.2, 4.1))
    for i, scen in enumerate(SCENARIOS):
        vals = [data[scen][fy]["surplus_or_deficit"] / 1e6 for fy in fys]
        offsets = [xi + (i - 1) * width for xi in x]
        ax.bar(
            offsets,
            vals,
            width=width,
            color=SCENARIO_COLOR[scen],
            label=SCENARIO_LABEL[scen],
            edgecolor="#222",
            linewidth=0.5,
        )
        for xi, v in zip(offsets, vals):
            ax.text(xi, v - 8, f"{v:.0f}", ha="center", va="top", fontsize=7, color="white" if v < -40 else "#222")
    ax.axhline(0, color="#222", linewidth=0.7)
    ax.set_xticks(x)
    ax.set_xticklabels([f"FY{fy-2000}" for fy in fys])
    ax.set_ylabel("Surplus / (Deficit), USD millions")
    ax.set_title("Five-Year General Fund Surplus / (Deficit) by Scenario")
    ax.legend(loc="lower left", fontsize=8)

    # cumulative callouts
    for i, scen in enumerate(SCENARIOS):
        cum = sum(data[scen][fy]["surplus_or_deficit"] for fy in fys) / 1e6
        ax.text(
            0.99,
            0.95 - 0.07 * i,
            f"{SCENARIO_LABEL[scen]}  cumulative: ${cum:,.0f}M",
            transform=ax.transAxes,
            ha="right",
            va="top",
            color=SCENARIO_COLOR[scen],
            fontsize=8.5,
        )
    ax.text(
        0.0,
        -0.2,
        "Source: /data/scenario_results.csv (Stage 6 integrated model); surplus/deficit metric by scenario and fiscal year.",
        transform=ax.transAxes,
        fontsize=6.8,
        ha="left",
        color="#444",
    )
    fig.tight_layout()
    fig.savefig(OUT / "fig_scenario_deficit.png", bbox_inches="tight")
    plt.close(fig)


# ---------- fig 2b: FY27 adopted Five-Year Plan vs. scenarios ----------
def fig_fy27_adopted_vs_scenarios(data):
    """Compare PWC's own adopted FY27-FY31 Five-Year Plan general revenue to the
    three scenarios in this model. The plan is the county's forward revenue
    baseline as of 2026-04-21 adoption (Item 7-J)."""
    fys = [2027, 2028, 2029, 2030, 2031]
    adopted_plan = {
        2027: 1_955_227_500,
        2028: 2_044_099_938,
        2029: 2_120_820_936,
        2030: 2_206_491_134,
        2031: 2_295_304_188,
    }
    fig, ax = plt.subplots(figsize=(7.4, 4.3))
    # Scenario lines
    for scen in SCENARIOS:
        vals = [data[scen][fy]["total_revenue"] / 1e9 for fy in fys]
        ax.plot(
            fys, vals, marker="o",
            color=SCENARIO_COLOR[scen], label=SCENARIO_LABEL[scen], linewidth=1.8,
        )
    # FY27 adopted plan overlay
    adopted_vals = [adopted_plan[fy] / 1e9 for fy in fys]
    ax.plot(
        fys, adopted_vals, marker="s", color="#b8860b", linewidth=2.2,
        linestyle="--", label="FY27 Adopted Five-Year Plan (Item 7-J)",
    )
    for fy, v in zip(fys, adopted_vals):
        ax.annotate(f"${v:.2f}B", (fy, v), textcoords="offset points",
                    xytext=(0, 8), ha="center", fontsize=7, color="#8B6508")
    ax.set_xticks(fys)
    ax.set_xticklabels([f"FY{fy-2000}" for fy in fys])
    ax.set_ylabel("Total General Fund Revenue, USD billions")
    ax.set_title("PWC Adopted FY27-FY31 Five-Year Plan vs. Three Scenarios")
    ax.legend(loc="upper left", fontsize=8)
    ax.text(
        0.0,
        -0.22,
        "Sources: Adopted plan from /data/fy27_adopted_five_year_plan.csv (Item 7-J, adopted 2026-04-21); "
        "scenario totals from /data/scenario_results.csv metric total_revenue. "
        "Adopted plan figures are proposed-budget values; adopted post-markup general revenue is ~$32.6M lower "
        "(Adoption memo p.2). Non-Pageland DC CAPEX is not discounted in the adopted plan.",
        transform=ax.transAxes,
        fontsize=6.5,
        ha="left",
        color="#444",
    )
    fig.tight_layout()
    fig.savefig(OUT / "fig_fy27_adopted_vs_scenarios.png", bbox_inches="tight")
    plt.close(fig)


# ---------- fig 3: required nominal tax rate ----------
def fig_required_tax_rate(data):
    fys = [2027, 2028, 2029, 2030, 2031]
    fig, ax = plt.subplots(figsize=(7.2, 4.1))
    fy27_rate = 0.850
    fy26_rate = 0.906
    ax.axhline(fy27_rate, color="#1f7a1f", linestyle="-", linewidth=1.2, label="FY27 adopted nominal rate $0.850")
    ax.axhline(fy26_rate, color="#888", linestyle="--", linewidth=0.8, label="FY26 adopted nominal rate $0.906")
    ax.axhline(1.000, color="#888", linestyle=":", linewidth=0.8)
    ax.text(fys[0] - 0.05, 1.003, "$1.00 threshold", fontsize=7, color="#666")

    for scen in SCENARIOS:
        vals = [data[scen][fy]["required_re_tax_rate_nominal_per_100"] for fy in fys]
        ax.plot(fys, vals, marker="o", color=SCENARIO_COLOR[scen], label=SCENARIO_LABEL[scen], linewidth=1.8)
        for fy, v in zip(fys, vals):
            ax.annotate(f"{v:.3f}", (fy, v), textcoords="offset points", xytext=(0, 7), ha="center", fontsize=7, color=SCENARIO_COLOR[scen])

    ax.set_xticks(fys)
    ax.set_xticklabels([f"FY{fy-2000}" for fy in fys])
    ax.set_ylabel("Nominal real-estate tax rate, $ per $100 AV")
    ax.set_ylim(0.80, 1.10)
    ax.set_title("Required Nominal RE Tax Rate to Close the Gap, by Scenario")
    ax.legend(loc="upper left", fontsize=8)
    ax.text(
        0.0,
        -0.2,
        "Source: /data/scenario_results.csv metric required_re_tax_rate_nominal_per_100. Nominal rate converted from the modeled "
        "effective rate using the FY26 $0.906/$0.746 = 1.214 ratio (PWC-BUD-FY26-REV p.63; model/pwc_5yr.py §NOMINAL_TO_EFFECTIVE_RATIO). "
        "FY27 adopted rate $0.850 (Item 7-A) shown as the current-policy reference; FY26 $0.906 shown for historical comparison.",
        transform=ax.transAxes,
        fontsize=6.5,
        ha="left",
        color="#444",
    )
    fig.tight_layout()
    fig.savefig(OUT / "fig_required_tax_rate.png", bbox_inches="tight")
    plt.close(fig)


# ---------- fig 4: reserve trajectory ----------
def fig_reserve_trajectory(data):
    fys = [2027, 2028, 2029, 2030, 2031]
    fig, ax = plt.subplots(figsize=(7.2, 4.3))
    floor_vals = [data[SCENARIO_PRE_DG][fy]["unassigned_gf_balance_policy_floor_7_5pct"] / 1e6 for fy in fys]
    ax.plot(fys, floor_vals, color="#222", linestyle="--", linewidth=1.2, label="7.5% policy floor (PSFM 1.02)")
    for scen in SCENARIOS:
        vals = [data[scen][fy]["unassigned_gf_balance_eoy"] / 1e6 for fy in fys]
        ax.plot(fys, vals, marker="o", color=SCENARIO_COLOR[scen], label=SCENARIO_LABEL[scen], linewidth=1.8)
    ax.axhline(0, color="#666", linewidth=0.8)
    ax.set_xticks(fys)
    ax.set_xticklabels([f"FY{fy-2000}" for fy in fys])
    ax.set_ylabel("Unassigned GF Balance, USD millions (EOY)")
    ax.set_title("Unassigned General Fund Balance vs. 7.5% PSFM Floor\n(Negative values = balance exhausted)")
    ax.legend(loc="lower left", fontsize=8)
    ax.text(
        0.0,
        -0.22,
        "Source: /data/scenario_results.csv; starting balance FY25 audited $134.7M (PWC-ACFR-FY25 p.35 Exhibit 4); "
        "floor = 7.5% × total GF revenue per PWC Principles of Sound Financial Management §1.02 (PWC-PSFM-24).",
        transform=ax.transAxes,
        fontsize=6.5,
        ha="left",
        color="#444",
    )
    fig.tight_layout()
    fig.savefig(OUT / "fig_reserve_trajectory.png", bbox_inches="tight")
    plt.close(fig)


# ---------- fig 5: debt-service ratio ----------
def fig_debt_service_ratio(data):
    fys = [2027, 2028, 2029, 2030, 2031]
    fig, ax = plt.subplots(figsize=(7.2, 4.1))
    ax.axhline(10, color="#222", linestyle="--", linewidth=1.0, label="10% PSFM cap (§5.02d)")
    for scen in SCENARIOS:
        vals = [data[scen][fy]["debt_service_to_revenue_ratio"] * 100 for fy in fys]
        ax.plot(fys, vals, marker="o", color=SCENARIO_COLOR[scen], label=SCENARIO_LABEL[scen], linewidth=1.8)
    ax.set_xticks(fys)
    ax.set_xticklabels([f"FY{fy-2000}" for fy in fys])
    ax.set_ylabel("Debt service as % of total revenue")
    ax.set_title("Debt-Service-to-Revenue Ratio vs. 10% PSFM Cap")
    ax.set_ylim(5.5, 10.5)
    ax.legend(loc="center left", fontsize=8)
    ax.text(
        0.0,
        -0.2,
        "Source: /data/scenario_results.csv metrics debt_service_to_revenue_ratio; cap from PWC-PSFM-24 Policy 5.02(d). "
        "Denominator is total revenue including Agency Revenue and Fire Levy.",
        transform=ax.transAxes,
        fontsize=6.5,
        ha="left",
        color="#444",
    )
    fig.tight_layout()
    fig.savefig(OUT / "fig_debt_service_ratio.png", bbox_inches="tight")
    plt.close(fig)


# ---------- fig 6: canceled / contingent / proceeding MW by project ----------
def fig_canceled_capex():
    # Rows from /data/canceled_projects.csv (MW integer extraction)
    projects = [
        ("Digital Gateway North (Ord. 23-57 / QTS)", 700, "invalidated"),
        ("Digital Gateway South (Ord. 23-58 / QTS)", 500, "invalidated"),
        ("Compass PWC Campus 1 (Ord. 23-59)", 1700, "invalidated"),
        ("PW Digital Gateway residual (379 ac)", 200, "contingent"),
        ("Dulles South Innovation Center (est.)", 1800, "contingent"),
        ("John Marshall Commons / CTP-II", 80, "contingent"),
        ("Devlin Tech Park (AWS)", 900, "proceeding"),
        ("Hornbaker Road (Mortenson)", 100, "proceeding"),
        ("Amazon Wellington/Devlin 44 ac", 100, "proceeding"),
    ]
    colors = {
        "invalidated": "#d62728",
        "contingent": "#ff7f0e",
        "proceeding": "#2ca02c",
    }
    fig, ax = plt.subplots(figsize=(7.5, 4.6))
    names = [p[0] for p in projects]
    mw = [p[1] for p in projects]
    cats = [p[2] for p in projects]
    y = list(range(len(projects)))[::-1]
    bars = ax.barh(
        y,
        mw,
        color=[colors[c] for c in cats],
        edgecolor="#222",
        linewidth=0.5,
    )
    for yi, m in zip(y, mw):
        ax.text(m + 25, yi, f"{m:,} MW", va="center", fontsize=7.5)
    ax.set_yticks(y)
    ax.set_yticklabels(names, fontsize=7.5)
    ax.set_xlabel("IT load (MW) at planned stabilization")
    ax.set_title(
        "Pageland / Digital Gateway Cancellation and Contingent / Proceeding Overlay Sites"
    )
    import matplotlib.patches as mpatches
    legend = [
        mpatches.Patch(color=colors["invalidated"], label="Invalidated (Oak Valley ruling)"),
        mpatches.Patch(color=colors["contingent"], label="Contingent on overlay reliability"),
        mpatches.Patch(color=colors["proceeding"], label="Proceeding"),
    ]
    ax.legend(handles=legend, loc="lower right", fontsize=7.5)
    totals = defaultdict(int)
    for _, m, c in projects:
        totals[c] += m
    ax.text(
        0.0,
        -0.18,
        f"Totals: invalidated {totals['invalidated']:,} MW (23M sqft); contingent {totals['contingent']:,} MW; "
        f"proceeding: {totals['proceeding']:,} MW. Source: /data/canceled_projects.csv; Stage 2 canceled_projects.md §2 and §3.",
        transform=ax.transAxes,
        fontsize=6.8,
        ha="left",
        color="#444",
    )
    ax.set_xlim(0, max(mw) * 1.22)
    fig.tight_layout()
    fig.savefig(OUT / "fig_canceled_capex.png", bbox_inches="tight")
    plt.close(fig)


# ---------- fig 7 (NEW Stage 3b): Loudoun vs peer-county residential permits ----------
def fig_peer_county_permits():
    """Loudoun vs. peer-county residential permit time series, highlighting
    the -53% YoY 2024->2025 differential post by-right DC elimination.
    Source: /data/peer_county_panel.csv (Census BPS series).
    """
    panel: dict[str, dict[int, int]] = {}
    with open(DATA / "peer_county_panel.csv") as f:
        rdr = csv.DictReader(row for row in f if not row.lstrip().startswith("#"))
        for row in rdr:
            if row["metric"] != "residential_permits_units":
                continue
            try:
                fy = int(row["fiscal_year"])
                v = int(float(row["value"]))
            except (ValueError, KeyError):
                continue
            panel.setdefault(row["county"], {})[fy] = v

    years = [2022, 2023, 2024, 2025]
    fig, ax = plt.subplots(figsize=(7.4, 4.3))
    colors = {
        "Loudoun": "#d62728",
        "Prince William": "#11365d",
        "Stafford": "#888888",
        "Fauquier": "#8a6c00",
        "Culpeper": "#2ca02c",
        "King George": "#9467bd",
    }
    order = ["Loudoun", "Prince William", "Fauquier", "Stafford", "Culpeper", "King George"]
    for county in order:
        if county not in panel:
            continue
        vals = [panel[county].get(y, None) for y in years]
        ax.plot(
            years,
            vals,
            marker="o",
            linewidth=2.0 if county == "Loudoun" else 1.2,
            color=colors[county],
            label=county + (" (treated)" if county == "Loudoun" else ""),
        )
        # Label the 2025 endpoint
        if vals[-1] is not None:
            ax.annotate(
                f"{vals[-1]:,}",
                (years[-1], vals[-1]),
                textcoords="offset points",
                xytext=(6, 0),
                fontsize=7.5,
                color=colors[county],
                va="center",
            )

    # Shade the event window
    ax.axvspan(2024.7, 2025.3, color="#f7e0e0", alpha=0.55, linewidth=0)
    ax.text(
        2025,
        max(v for d in panel.values() for v in d.values() if v) * 0.97,
        "Mar 2025 Loudoun\nby-right DC elim.",
        ha="center",
        va="top",
        fontsize=7.5,
        color="#992222",
    )

    ax.set_xticks(years)
    ax.set_xticklabels([str(y) for y in years])
    ax.set_ylabel("Residential housing units authorized")
    ax.set_title(
        "Peer-County Residential Permit Differential: Loudoun 2024->2025 -53% YoY\n"
        "Post by-right DC elimination vs. NoVA peer mean +2%"
    )
    ax.legend(loc="upper right", fontsize=7.8, ncol=2)

    ax.text(
        0.0,
        -0.22,
        "Source: U.S. Census Building Permits Survey county year-end files 2022-2025 (co{YY}12y.txt). "
        "Panel at /data/peer_county_panel.csv. 2024 Loudoun = grandfathering-rush peak; "
        "2025 Loudoun = first full post-event year. PWC read-across is discounted ~0.27x "
        "(Stage 3b §b.1 exposure-ratio adjustment) = CAPEX Spillover -20 pct residential permit "
        "deterrent Year-1.",
        transform=ax.transAxes,
        fontsize=6.5,
        ha="left",
        color="#444",
    )
    fig.tight_layout()
    fig.savefig(OUT / "fig_peer_county_permits.png", bbox_inches="tight")
    plt.close(fig)


# ---------- fig 8 (NEW Stage 6b): Spillover channel contributions ----------
def fig_spillover_channels():
    """Bar chart decomposing CAPEX Spillover cumulative FY27-FY31 deficit
    delta vs. Pre-Cancellation Digital Gateway into constituent channels.
    Computed inline from the scenario CSVs so the chart stays in sync with
    the model output.
    """
    # Load revenue detail
    from collections import defaultdict as dd
    a_rev_by_line = dd(lambda: dd(float))
    c_rev_by_line = dd(lambda: dd(float))
    with open(DATA / "scenario_revenue_detail.csv") as f:
        rdr = csv.DictReader(f)
        for row in rdr:
            fy = int(row["fiscal_year"])
            amt = float(row["amount_usd"])
            line = row["revenue_source"]
            if row["scenario"] == SCENARIO_PRE_DG:
                a_rev_by_line[fy][line] += amt
            elif row["scenario"] == SCENARIO_SPILLOVER:
                c_rev_by_line[fy][line] += amt

    # Credit spread (C expenditure side).
    cs_c = 0.0
    with open(DATA / "scenario_expenditure_detail.csv") as f:
        rdr = csv.DictReader(f)
        for row in rdr:
            if row["line_item"] != "spillover_credit_spread_ds":
                continue
            if row["scenario"] == SCENARIO_SPILLOVER:
                cs_c += float(row["amount_usd"])

    # Cumulative deltas by revenue line.
    def cum_delta(line: str) -> float:
        return sum(
            c_rev_by_line[fy].get(line, 0.0) - a_rev_by_line[fy].get(line, 0.0)
            for fy in a_rev_by_line
        )

    dc = cum_delta("data_center_tax_revenue")
    res = cum_delta("residential_real_estate")
    # Stage 3b residential spillover vs. Stage 4 LOW residential separate out.
    low_res = {}
    low_spill_res = {}
    base_res = {}
    with open(DATA / "non_dc_revenue_projection.csv") as f:
        rdr = csv.DictReader(f)
        for row in rdr:
            if row["revenue_line"] != "residential_real_estate":
                continue
            fy = int(row["fiscal_year"])
            amt = float(row["amount_usd"])
            if row["scenario"] == "low":
                low_res[fy] = amt
            elif row["scenario"] == "low_with_spillover":
                low_spill_res[fy] = amt
            elif row["scenario"] == "base":
                base_res[fy] = amt
    spill_effect = sum(low_spill_res[fy] - low_res[fy] for fy in low_res)
    res_fed_low_vs_base = sum(low_res[fy] - base_res[fy] for fy in low_res)

    # Non-DC excluding residential lines.
    nondc_lines_split = [
        "non_dc_commercial_real_estate",
        "personal_property_vehicles",
        "non_dc_business_tangible",
        "local_sales_tax",
        "bpol_tax",
        "food_and_beverage_tax",
        "consumer_utility_tax",
        "communications_sales_tax",
        "motor_vehicle_license",
        "recordation_tax",
        "transient_occupancy_tax",
        "cigarette_tax",
        "investment_income",
    ]
    fed_contraction_other_split = sum(cum_delta(l) for l in nondc_lines_split)
    earmarked = sum(cum_delta(l) for l in ("agency_revenue", "fire_levy_revenue"))
    state_aid = cum_delta("state_aid_gf_direct")

    # Net-of-Schools-split effect: split-base revenue loss is offset 57.23% by Schools expenditure reduction.
    SPLIT_NET = 1.0 - 0.5723  # 0.4277

    bars = [
        ("DC CAPEX deterrence\n(Pageland + new-build + writedown)", -dc * SPLIT_NET, "#d62728"),
        ("Residential Stage 3b spillover\n(peer-county-grounded; Loudoun analog)", -spill_effect * SPLIT_NET, "#ff7f0e"),
        ("Federal-contraction housing drag\n(Stage 4 LOW residential)", -res_fed_low_vs_base * SPLIT_NET, "#1f77b4"),
        ("Other split-base non-DC LOW vs BASE\n(vehicles, sales, BPOL, investment, etc.)", -fed_contraction_other_split * SPLIT_NET, "#17a2b8"),
        ("Agency + Fire Levy\n(earmarked, direct)", -earmarked, "#a36a00"),
        ("LCI lag / state aid", -state_aid, "#6b7280"),
        ("Credit-spread incremental DS\n(Stage 3b/6b; Moody's 1-notch)", cs_c, "#2ca02c"),
    ]

    fig, ax = plt.subplots(figsize=(7.8, 4.8))
    names = [b[0] for b in bars]
    vals = [b[1] / 1e6 for b in bars]
    colors = [b[2] for b in bars]
    y = list(range(len(bars)))[::-1]
    ax.barh(y, vals, color=colors, edgecolor="#222", linewidth=0.5)
    for yi, v in zip(y, vals):
        ax.text(v + (4 if v > 0 else -4), yi, f"${v:+,.1f}M", va="center", ha="left" if v > 0 else "right", fontsize=8)
    ax.set_yticks(y)
    ax.set_yticklabels(names, fontsize=8)
    ax.set_xlabel("Contribution to CAPEX Spillover cumulative FY27-FY31 deficit delta vs. Pre-Cancel DG, USD millions (positive = adds to deficit)")
    ax.set_title(
        "CAPEX Spillover Deficit Decomposition vs. Pre-Cancel DG: Channel Contributions\n"
        f"(Total cumulative delta: ${sum(vals):,.0f}M, split-base losses net of 57.23% Schools offset)"
    )
    ax.axvline(0, color="#222", linewidth=0.7)
    ax.set_xlim(min(vals) * 1.15 - 8, max(vals) * 1.25 + 8)
    ax.text(
        0.0,
        -0.21,
        "Source: Stage 6b integrated model (/data/scenario_revenue_detail.csv + /data/scenario_expenditure_detail.csv). "
        "Split-base revenue losses are reduced 57.23% by the Schools-transfer expenditure offset. "
        "Residential spillover = Stage 3b peer-county-grounded overlay layered on Stage 4 LOW.",
        transform=ax.transAxes,
        fontsize=6.4,
        ha="left",
        color="#444",
    )
    fig.tight_layout()
    fig.savefig(OUT / "fig_spillover_channels.png", bbox_inches="tight")
    plt.close(fig)


# ---------- Documented constants for the visceral Figures 9 and 10 ----------
# See docstring above for source citations. Kept here so the computed numbers
# in the figures and captions are all traceable to a single place.
TEACHER_COST_PER_YEAR = 90_000        # $/yr; PWCS 2024-25 avg $75K base * 1.20 benefits load
COUNTY_FTE_FULLY_LOADED = 115_000     # $/yr; Stage 5 op-reduction calc
PWC_POLICE_BUDGET_FY26 = 160_670_000  # PWC-BUD-FY26-EXP p.65
PWC_PUBLIC_SAFETY_FY26 = 420_396_976  # PWC-BUD-FY26-EXP p.65-66 Safe & Secure Community
PWC_MEDIAN_HOME_FY26 = 570_600        # PWC 2025 RE Assessments Annual Report
PWC_MEDIAN_HOME_TAX_FY26 = PWC_MEDIAN_HOME_FY26 * 0.00906  # $5,169.64/yr
# Rough order-of-magnitude PWC GF headcount (ex-Schools). Derived from
# FY26 GF Salaries & Benefits $617M with ~75% going to salary / ~25% benefits;
# ~$460M covered payroll / ~$85K avg base = ~5,400 FTE. Labeled "order of
# magnitude" in figure captions; not a published single-number figure.
PWC_COUNTY_FTE_ORDER_OF_MAGNITUDE = 5_400


# ---------- fig 9 (visceral): the size of the hole ----------
def fig_revenue_hole(data):
    """Two-panel figure for a non-expert audience.
    Left: CAPEX Spillover stacked bars FY27-FY31 showing projected revenue (teal)
          with the shortfall against committed expenditure (red with diagonal
          hatch so it reads even in grayscale / colorblind).
    Right: year-by-year department-level FTE layoff equivalents under the
           CAPEX Spillover scenario, with a proportional-share allocation of
           the annual gap across general-fund departments. Data pulled from
           /data/dept_fully_loaded_rates.csv and /data/spillover_dept_layoff_path.csv.
    """
    fys = [2027, 2028, 2029, 2030, 2031]
    revenues = [data[SCENARIO_SPILLOVER][fy]["total_revenue"] / 1e6 for fy in fys]
    deficits = [-data[SCENARIO_SPILLOVER][fy]["surplus_or_deficit"] / 1e6 for fy in fys]  # positive
    cumulative_shortfall_m = sum(deficits)  # ~1,167

    fig = plt.figure(figsize=(18.5, 10.4))
    gs = fig.add_gridspec(
        2, 2,
        width_ratios=[1.05, 1.15],
        height_ratios=[1.0, 0.12],
        wspace=0.22, hspace=0.10,
        top=0.86, bottom=0.06,
    )

    # === Left panel: stacked horizontal bars per FY ===
    axL = fig.add_subplot(gs[0, 0])
    y = list(range(len(fys)))[::-1]
    teal = "#1b8a8f"
    red = "#c0392b"
    for yi, rev, gap in zip(y, revenues, deficits):
        axL.barh(yi, rev, color=teal, edgecolor="#0e5052", linewidth=1.2)
        axL.barh(yi, gap, left=rev, color=red, edgecolor="#5a1511",
                 linewidth=1.8, hatch="///")
        axL.text(rev / 2, yi, f"Revenue\n${rev:,.0f}M", ha="center", va="center",
                 fontsize=13, color="white", fontweight="bold")
        axL.text(rev + gap / 2, yi, f"GAP\n${gap:,.0f}M", ha="center", va="center",
                 fontsize=13, color="white", fontweight="bold")
    axL.set_yticks(y)
    axL.set_yticklabels([f"FY{fy-2000}" for fy in fys], fontsize=15)
    axL.set_xlabel("USD, millions", fontsize=13)
    axL.set_title("Each Year: Revenue vs. Shortfall",
                  fontsize=16, pad=8)
    axL.set_xlim(0, max(r + g for r, g in zip(revenues, deficits)) * 1.08)
    axL.grid(axis="x", linewidth=0.5, alpha=0.5)
    axL.set_axisbelow(True)

    # Left-panel legend intentionally omitted: each bar segment is labeled
    # in-place with "Revenue $X" and "GAP $Y", so a separate legend is
    # redundant. Right-panel department legend remains.
    import matplotlib.patches as mpatches

    # === Right panel: year-by-year department-level layoff-equivalents ===
    axR = fig.add_subplot(gs[0, 1])

    # Load /data/spillover_dept_layoff_path.csv and dept rates.
    layoff_by_fy: dict[int, list[tuple[str, int]]] = {fy: [] for fy in fys}
    rate_by_dept: dict[str, float] = {}
    with open(DATA / "dept_fully_loaded_rates.csv") as f:
        rdr = csv.DictReader(f)
        for row in rdr:
            if row["personnel_convertible"].lower() != "true":
                continue
            rate_by_dept[row["department"]] = float(row["fully_loaded_rate_usd"])
    with open(DATA / "spillover_dept_layoff_path.csv") as f:
        rdr = csv.DictReader(f)
        for row in rdr:
            fy = int(row["fiscal_year"])
            if fy not in layoff_by_fy:
                continue
            dept = row["department"]
            layoffs = int(row["dept_fte_layoff_equiv"])
            layoff_by_fy[fy].append((dept, layoffs))

    # Preserve the order used in dept_fully_loaded_rates.csv.
    dept_order = list(rate_by_dept.keys())

    # Colorblind-friendly palette (tableau-cb with hand-tuned hues). 13 slots.
    dept_color = {
        "PWCS (Schools instructional)":            "#1f77b4",
        "Police":                                  "#d62728",
        "Fire & Rescue":                           "#ff7f0e",
        "Sheriff":                                 "#8c564b",
        "Adult Detention Center":                  "#c49c94",
        "Judicial / Courts":                       "#9467bd",
        "General Government":                      "#7f7f7f",
        "Community Development":                   "#17becf",
        "Social Services":                         "#2ca02c",
        "Community Services (Behavioral Health)":  "#bcbd22",
        "Parks & Recreation":                      "#e377c2",
        "Library":                                 "#8a6c00",
        "Other Human Services":                    "#aec7e8",
    }
    # Short display labels for legend (match the Y axis space budget).
    dept_display = {
        "PWCS (Schools instructional)":            "PWCS (Schools)",
        "Police":                                  "Police",
        "Fire & Rescue":                           "Fire & Rescue",
        "Sheriff":                                 "Sheriff",
        "Adult Detention Center":                  "Adult Detention Ctr",
        "Judicial / Courts":                       "Judicial / Courts",
        "General Government":                      "General Govt.",
        "Community Development":                   "Community Dev.",
        "Social Services":                         "Social Services",
        "Community Services (Behavioral Health)":  "Comm. Svcs (Behav. Health)",
        "Parks & Recreation":                      "Parks & Rec",
        "Library":                                 "Library",
        "Other Human Services":                    "Other Human Svcs",
    }

    y = list(range(len(fys)))[::-1]
    totals_per_fy = {}
    # Stack bars segment by segment in the stable dept_order
    for yi, fy in zip(y, fys):
        row = dict(layoff_by_fy[fy])
        left = 0
        total = 0
        for dept in dept_order:
            val = row.get(dept, 0)
            axR.barh(yi, val, left=left, color=dept_color[dept], edgecolor="#333", linewidth=0.4)
            left += val
            total += val
        totals_per_fy[fy] = total

    # End-of-bar total label
    maxtot = max(totals_per_fy.values())
    for yi, fy in zip(y, fys):
        t = totals_per_fy[fy]
        axR.text(t + maxtot * 0.012, yi, f"{t:,}",
                 va="center", ha="left", fontsize=13, fontweight="bold", color="#1a1a1a")

    axR.set_yticks(y)
    axR.set_yticklabels([f"FY{fy-2000}" for fy in fys], fontsize=15)
    axR.set_xlabel("FTE-year layoff equivalents (proportional-share allocation)", fontsize=12)
    axR.set_xlim(0, maxtot * 1.12)
    axR.set_title("Annual Layoff Equivalent, by Department", fontsize=16, pad=8)
    axR.grid(axis="x", linewidth=0.5, alpha=0.5)
    axR.set_axisbelow(True)

    # Per-dept cumulative FY27-FY31 totals for legend annotation
    cum_by_dept = {d: 0 for d in dept_order}
    for fy in fys:
        for dept, val in layoff_by_fy[fy]:
            cum_by_dept[dept] += val

    legend_handles = []
    for dept in dept_order:
        cum = cum_by_dept[dept]
        label = f"{dept_display[dept]}  (5-yr cum: {cum:,})"
        legend_handles.append(mpatches.Patch(color=dept_color[dept], label=label))
    axR.legend(
        handles=legend_handles,
        loc="center left",
        bbox_to_anchor=(1.02, 0.5),
        fontsize=9.5,
        frameon=False,
        title="Department (5-yr cumulative FTE-year-equivalents)",
        title_fontsize=10.5,
    )

    # Subtitle below axR title: approach
    axR.text(
        0.0, -0.14,
        "Proportional-share allocation across FY26 General Fund appropriation lines; "
        "PWCS Schools transfer (57.23% of General Revenue) is the single largest share.",
        transform=axR.transAxes, ha="left", va="top", fontsize=9.0, color="#333",
    )

    # === Bottom banner: headline number ===
    axB = fig.add_subplot(gs[1, :])
    axB.set_axis_off()
    peak_fy31 = totals_per_fy[2031]
    total_cum = sum(totals_per_fy.values())
    axB.text(
        0.5, 0.55,
        f"Cumulative five-year General Fund shortfall:  "
        f"${cumulative_shortfall_m:,.0f}M  (≈ ${cumulative_shortfall_m/1000:.2f}B)   "
        f"|   Proportional-share layoff equivalent:  "
        f"peak-year FY31 {peak_fy31:,} FTE,  five-year cumulative {total_cum:,} FTE-years",
        transform=axB.transAxes, ha="center", va="center",
        fontsize=15, fontweight="bold", color="white",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#5a1511",
                  edgecolor="#5a1511"),
    )

    # Figure-level title and caption
    fig.suptitle(
        "The Shortfall in Concrete Terms",
        fontsize=22, fontweight="bold", y=0.965,
    )
    fig.text(
        0.5, 0.917,
        "Prince William County General Fund, CAPEX Spillover scenario, FY27-FY31  |  "
        "Left: revenue vs. shortfall  |  Right: department-level FTE layoff equivalent",
        ha="center", va="top", fontsize=13.5, color="#333",
    )
    fig.text(
        0.5, 0.005,
        "Sources: Left panel: /data/scenario_results.csv (Stage 6b). "
        "Right panel: /data/spillover_dept_layoff_path.csv derived from "
        "/data/dept_fully_loaded_rates.csv and /data/scenario_results.csv; "
        "department rates from PWC FY26 Adopted Budget Expenditures (PWC-BUD-FY26-EXP p.65-67) "
        "and Budget Summary FTE table (PWC-BUD-FY26-SUMM p.44); PWCS teacher rate from PWCS FY26 "
        "Adopted Budget and 2025-26 salary schedule (pwcs.edu) with VRS teacher rate 18.53 percent per Code of Va. 51.1-145. "
        "Assumes layoffs fall on each department proportional to its FY26 appropriation share; "
        "actual incidence would vary by contract, union agreement, and state mandate. "
        "Non-departmental, debt service, and transfers are excluded (not personnel-convertible).",
        ha="center", va="bottom", fontsize=8.5, color="#333", wrap=True,
    )
    fig.savefig(OUT / "fig_revenue_hole.png", bbox_inches="tight", dpi=180)
    plt.close(fig)


# ---------- fig 10 (options menu): the nine Section 9 gap-closing options ----------
def fig_options_menu():
    """Table-style figure: nine rows, four columns.
    Columns: (1) Option, (2) What it closes, (3) Human-scale consequence,
             (4) Reversibility.
    Rows color-coded by political/fiscal difficulty using a non-red-green palette.

    Implementation note: matplotlib's text wrap="True" only wraps on figure
    resize, which is unreliable. We pre-wrap each cell's text with textwrap
    and use a multi-line string, sizing the row by the line count of the
    widest cell so the table always fits cleanly.
    """
    import textwrap

    GAP_FY31 = 365_000_000   # CAPEX Spillover FY31 annual gap
    GAP_CUM = 1_167_000_000  # Cumulative FY27-FY31

    schools_cut_partial = 37_000_000  # cut to 55% share = ~$37M/yr
    teachers_partial = schools_cut_partial / TEACHER_COST_PER_YEAR
    teachers_full = GAP_FY31 / TEACHER_COST_PER_YEAR
    fte_full_gap = GAP_FY31 / COUNTY_FTE_FULLY_LOADED

    # Colorblind-safe difficulty palette (no red/green single-channel signal);
    # every row is also labeled [LOW]/[MED]/[HIGH] so color is redundant.
    DIFF_FACE = {"low": "#d4e6f1", "medium": "#f7e0a3", "high": "#d7c3e3"}
    DIFF_EDGE = {"low": "#1f6fa0", "medium": "#8a6c00", "high": "#5e3b7b"}

    # Column width characters (tuned so pre-wrapped text fits the column
    # at the chosen fontsize). First column is narrower.
    col_widths_chars = [24, 26, 58, 26]

    raw_rows = [
        (
            "(a) Real-estate tax-rate increase to $1.023/$100",
            "100% of the gap on rate alone",
            "+$714/yr on a median $570,600 home (+13% vs. FY26)",
            "Ongoing; annually re-set",
            "high",
        ),
        (
            "(b) CIP deferral: $498M of GF-supported issuances delayed 24 months",
            "~10% of annual gap (~$35M/yr debt service relief)",
            "Judicial Center, Public Safety Training Center, Juvenile Services Center, "
            "Fire stations each slip 2+ years",
            "Reversible; foregone service capacity accumulates",
            "medium",
        ),
        (
            "(c) Schools-transfer renegotiation (share cut)",
            "~12% of annual gap (55% share = -$37M/yr)",
            f"At 55% share: ~{teachers_partial:,.0f} PWCS teacher-equivalents (at $90K fully loaded). "
            f"Full-gap-via-Schools-alone would be ~{teachers_full:,.0f} teachers -- not feasible without service collapse.",
            "Requires mutual amendment with School Board; politically radioactive",
            "high",
        ),
        (
            "(d) Operating reductions (FTE-equivalent)",
            "100% of gap requires the full $365M/yr cut",
            f"~{fte_full_gap:,.0f} FTE eliminated (of ~{PWC_COUNTY_FTE_ORDER_OF_MAGNITUDE:,} "
            f"GF county workforce ex-Schools, order of magnitude). "
            f"Constrained by 2024 IAFF CBA and SSC step/merit schedule.",
            "Service cuts are reversible; attrition-only path is slow",
            "high",
        ),
        (
            "(e) Reserve drawdown",
            "Bridge covers ~18-21 months at CAPEX Spillover pace, then gone",
            "$182.7M unassigned + stabilization + DC-stabilization reserves. "
            "Already below 7.5% PSFM floor in FY27 in every scenario.",
            "One-time; reserves rebuild over years",
            "low",
        ),
        (
            "(f) New revenue sources (meals, CE&P rate, BPOL, etc.)",
            "Individually modest; stacked adds ~$25-40M/yr",
            "Meals tax restored to 4%: +$13M/yr. Each $0.25 on CE&P rate: +$8M/yr. "
            "Transient occupancy, cigarette, cannabis require state enabling.",
            "Ongoing; statutory caps constrain upside",
            "medium",
        ),
        (
            "(g) Partial-recovery pathway (Partial Recovery)",
            "Saves ~$84M/yr average (~$420M cumulative vs. C)",
            "Requires clarifying ordinance + credibility with capital allocators across subsequent Boards.",
            "Partial; fiscal benefit grows with durability of signal",
            "medium",
        ),
        (
            "(h) Credit-rating preservation",
            "Direct ~$1M cumulative; rating narrative is load-bearing",
            "Addresses Moody's September 2025 credit-opinion concerns on DC-concentration + governance predictability.",
            "Preserves future issuance cost",
            "low",
        ),
        (
            "(i) Cure: re-notice and re-enact the voided ordinances",
            "Recovers Pageland-specific revenue (~$58M/yr avg vs. C)",
            "Lowest dollar cost on menu (administrative expense in hundreds of thousands). "
            "45-60 day procedural timeline. Has been available for the full 20 months and not exercised.",
            "Reversible via cure in either direction",
            "medium",
        ),
    ]

    # Pre-wrap each cell; compute row line-count as max across cells.
    wrapped_rows = []
    for opt, closes, cost, rev, diff in raw_rows:
        cells = [
            textwrap.fill(opt, width=col_widths_chars[0]),
            textwrap.fill(closes, width=col_widths_chars[1]),
            textwrap.fill(cost, width=col_widths_chars[2]),
            textwrap.fill(rev, width=col_widths_chars[3]),
        ]
        lines = max(c.count("\n") + 1 for c in cells)
        wrapped_rows.append((cells, lines, diff))

    # Figure sizing: ~0.42 inch per text line plus padding; total_lines drives height.
    total_lines = sum(r[1] for r in wrapped_rows)
    header_in = 0.9
    footer_in = 0.9
    top_pad_in = 1.8    # title + subtitle + legend band
    per_line_in = 0.36
    fig_w = 16.0
    fig_h = top_pad_in + header_in + per_line_in * total_lines + footer_in + 0.3
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # Column boundaries (fraction of axis width).
    # Widths roughly proportional to col_widths_chars, then tweaked for visual weight.
    col_edges = [0.000, 0.205, 0.380, 0.810, 1.000]
    col_headers = ["Option", "What it closes", "What it costs, in human terms", "Reversibility"]

    # Vertical layout (in axis coordinates):
    #   [legend band]
    #   [column header row]
    #   [data rows, one per option]
    #   [footer banner]
    # Compute from top down.
    legend_band_h = 0.050
    header_row_h = header_in / fig_h
    footer_row_h = 0.060
    y_cursor = 1.0

    # === Legend band (Political/fiscal difficulty key) ===
    y_cursor -= legend_band_h
    legend_y = y_cursor + legend_band_h / 2
    ax.text(
        0.005, legend_y, "Political / fiscal difficulty:",
        ha="left", va="center", fontsize=12.5, fontweight="bold", color="#333",
    )
    dx = 0.14
    for i, (label, key) in enumerate([("LOW", "low"), ("MEDIUM", "medium"), ("HIGH", "high")]):
        sx = 0.22 + i * dx
        ax.add_patch(plt.Rectangle(
            (sx, legend_y - 0.018), 0.026, 0.036,
            facecolor=DIFF_FACE[key], edgecolor=DIFF_EDGE[key], linewidth=1.2,
            clip_on=False,
        ))
        ax.text(sx + 0.032, legend_y, label, ha="left", va="center",
                fontsize=11.5, fontweight="bold", color=DIFF_EDGE[key])

    # === Column header row ===
    y_cursor -= 0.012  # small gap after legend
    header_top = y_cursor
    header_bot = y_cursor - header_row_h
    for i in range(4):
        ax.add_patch(plt.Rectangle(
            (col_edges[i], header_bot), col_edges[i + 1] - col_edges[i],
            header_top - header_bot,
            facecolor="#11365d", edgecolor="#11365d", clip_on=False,
        ))
        ax.text(
            (col_edges[i] + col_edges[i + 1]) / 2,
            (header_top + header_bot) / 2,
            col_headers[i],
            ha="center", va="center", color="white",
            fontsize=14, fontweight="bold",
        )
    y_cursor = header_bot

    # === Data rows ===
    data_row_unit_h = (y_cursor - footer_row_h - 0.020) / total_lines
    for cells, lines, diff in wrapped_rows:
        row_top = y_cursor
        row_bot = y_cursor - lines * data_row_unit_h
        for i in range(4):
            ax.add_patch(plt.Rectangle(
                (col_edges[i], row_bot), col_edges[i + 1] - col_edges[i],
                row_top - row_bot,
                facecolor=DIFF_FACE[diff], edgecolor=DIFF_EDGE[diff],
                linewidth=0.8, clip_on=False,
            ))
        # Difficulty tag
        ax.text(
            col_edges[0] + 0.004, row_top - 0.008,
            f"[{diff.upper()}]",
            ha="left", va="top", fontsize=9, fontweight="bold",
            color=DIFF_EDGE[diff],
        )
        # Option text (top-anchored, starts below the difficulty tag)
        ax.text(
            col_edges[0] + 0.004, row_top - 0.032, cells[0],
            ha="left", va="top", fontsize=10.5, fontweight="bold",
            color="#1a1a1a",
        )
        ax.text(
            col_edges[1] + 0.006, row_top - 0.018, cells[1],
            ha="left", va="top", fontsize=10.5, color="#1a1a1a",
        )
        ax.text(
            col_edges[2] + 0.006, row_top - 0.018, cells[2],
            ha="left", va="top", fontsize=10.5, color="#1a1a1a",
        )
        ax.text(
            col_edges[3] + 0.006, row_top - 0.018, cells[3],
            ha="left", va="top", fontsize=10.5, color="#1a1a1a",
        )
        y_cursor = row_bot

    # === Footer banner ===
    y_cursor -= 0.010
    footer_top = y_cursor
    footer_bot = y_cursor - footer_row_h
    ax.add_patch(plt.Rectangle(
        (col_edges[0], footer_bot), col_edges[-1] - col_edges[0],
        footer_top - footer_bot,
        facecolor="#5a1511", edgecolor="#5a1511", clip_on=False,
    ))
    ax.text(
        0.5, (footer_top + footer_bot) / 2,
        f"Gap to close:  CAPEX Spillover FY31 annual  ${GAP_FY31/1e6:,.0f}M    "
        f"|    Cumulative FY27-FY31  ${GAP_CUM/1e6:,.0f}M  (approx. ${GAP_CUM/1e9:.2f}B)",
        ha="center", va="center", color="white",
        fontsize=14, fontweight="bold",
    )

    # Figure-level title and subtitle
    fig.suptitle(
        "The Menu: What It Takes to Close the CAPEX Spillover Gap",
        fontsize=20, fontweight="bold", y=0.995,
    )
    fig.text(
        0.5, 0.965,
        "Prince William County General Fund, FY27-FY31   |   "
        "Nine gap-closing options from Section 9 of the Fiscal Risk Report",
        ha="center", va="top", fontsize=13, color="#333",
    )
    # Source note (bottom of figure)
    fig.text(
        0.5, 0.005,
        "Sources: Gap figures from /data/scenario_results.csv CAPEX Spillover (Stage 6b).   "
        "Teacher-equivalents = $1.17B or $37M divided by $90K fully loaded per teacher "
        "(PWCS 2024-25 avg base ~$75K from PWCS Board budget docs x 1.20 benefits load).   "
        "FTE-equivalent = $365M / $115K fully loaded per county FTE (Stage 5 op-reduction calc).   "
        "Option sizing: /model/pwc_5yr.py gap-closing menu.",
        ha="center", va="bottom", fontsize=9, color="#333",
    )

    fig.savefig(OUT / "fig_options_menu.png", bbox_inches="tight", dpi=180)
    plt.close(fig)


# ---------- stage-electricity: driver decomposition bar chart ----------
def fig_electricity_drivers():
    """Horizontal stacked/ranked bar decomposing the 2022-2026 Dominion
    residential rate-increase envelope by driver. DC-attributable portion
    of each driver is shown in a darker overlay segment.

    Source: /data/electricity_drivers.csv and /research/electricity_cost_decomposition.md.
    """
    # Load from CSV so the figure tracks the data file.
    rows = []
    with open(DATA / "electricity_drivers.csv") as f:
        for line in f:
            if line.startswith("#") or line.strip().startswith("driver") or not line.strip():
                continue
            parts = line.strip().split(",")
            if len(parts) < 7:
                continue
            rows.append({
                "driver": parts[0],
                "point": float(parts[1]),
                "low": float(parts[2]),
                "high": float(parts[3]),
                "dc_attr": float(parts[5]),
            })

    # Display labels (map from csv key to human label).
    label_map = {
        "natural_gas_reset_2022_russia_ukraine": "Natural-gas reset\n(Russia/Ukraine LNG)",
        "q1_2026_middle_east_hormuz": "Q1 2026 Middle East\n(Strait of Hormuz)",
        "pjm_capacity_auction": "PJM capacity auction\n(load + retirements + queue)",
        "transmission_buildout_nova": "Transmission build-out\n(Dominion zone)",
        "generation_capital_cvow_gas_solar_battery": "Generation capital\n(CVOW, gas, solar, battery)",
        "grid_inflation_materials_labor_transformers": "Grid inflation\n(transformers, labor)",
        "residual_storms_ev_ratebase_reliability": "Residual\n(storms, EV, rate-base)",
    }

    # Sort ascending by point share so largest appears at top of horizontal bars.
    rows_sorted = sorted(rows, key=lambda r: r["point"])
    labels = [label_map.get(r["driver"], r["driver"]) for r in rows_sorted]
    points = [r["point"] * 100 for r in rows_sorted]  # percentage of envelope
    dc_shares = [r["dc_attr"] * 100 for r in rows_sorted]  # percent of envelope attributed to DC
    non_dc_shares = [p - d for p, d in zip(points, dc_shares)]

    fig, ax = plt.subplots(figsize=(8.2, 4.8))
    y = list(range(len(labels)))
    # non-DC portion in steel blue; DC-attributable overlay in gold.
    ax.barh(y, non_dc_shares, color="#4e79a7", edgecolor="#222", linewidth=0.6, label="Non-DC-attributable")
    ax.barh(y, dc_shares, left=non_dc_shares, color="#b8860b", edgecolor="#222", linewidth=0.6, label="DC-attributable")

    for yi, (p, d) in enumerate(zip(points, dc_shares)):
        ax.text(p + 0.5, yi, f"{p:.0f}% (DC {d:.0f}%)", va="center", fontsize=8, color="#222")

    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=8.5)
    ax.set_xlabel("Share of the 2022-2026 Dominion residential rate-increase envelope (%)")
    ax.set_xlim(0, 38)
    ax.set_title(
        "Decomposition of the 2022-2026 Dominion residential rate-increase envelope\n"
        "Envelope approximately +$550/year on a typical 1,000 kWh customer; DC share approximately 30 percent"
    )
    ax.legend(loc="lower right", fontsize=8)
    ax.text(
        0.0,
        -0.18,
        "Sources: /data/electricity_drivers.csv; /research/electricity_cost_decomposition.md. "
        "Envelope = composite of base-rate proceedings plus fuel / capital riders; Virginia SCC Case No. PUR-2025-00058; "
        "EIA Electric Power Monthly; PJM 2025/26 and 2026/27 BRA reports; Dominion 2024 IRP; JLARC December 2024 Data Centers in Virginia; "
        "IEA Oil Market Report April 2026 (Q1 2026 Hormuz).",
        transform=ax.transAxes,
        fontsize=6.5,
        ha="left",
        color="#444",
    )
    fig.tight_layout()
    fig.savefig(OUT / "fig_electricity_drivers.png", bbox_inches="tight")
    plt.close(fig)


# ---------- stage-electricity: household comparison ----------
def fig_electricity_vs_retax():
    """Side-by-side comparison: plausible no-DC counterfactual annual electricity
    saving on a typical PWC household vs. CAPEX Spillover FY31 real-estate tax
    increment on a median $570,600 home.

    Source: /data/electricity_drivers.csv (DC-attributable share of envelope),
    /data/scenario_results.csv (CAPEX Spillover required nominal tax rate FY31).
    """
    # Household values (from research/electricity_cost_decomposition.md §3).
    elec_point = 165
    elec_low = 110
    elec_high = 248
    retax_point = 714
    retax_low = 570
    retax_high = 1050

    fig, ax = plt.subplots(figsize=(7.4, 4.6))
    x = [0, 1]
    points = [elec_point, retax_point]
    lows = [elec_low, retax_low]
    highs = [elec_high, retax_high]
    colors = ["#2ca02c", "#d62728"]
    labels = [
        "Plausible DC-attributable\nelectricity saving\n(no-DC counterfactual)",
        "CAPEX Spillover FY31\nRE-tax increment\n(median $570,600 home)",
    ]
    bars = ax.bar(x, points, color=colors, edgecolor="#222", linewidth=0.6, width=0.55)
    # Error bars representing the low-to-high range.
    err_low = [p - l for p, l in zip(points, lows)]
    err_high = [h - p for p, h in zip(points, highs)]
    ax.errorbar(x, points, yerr=[err_low, err_high], fmt="none", ecolor="#222", capsize=8, linewidth=1.1)
    for xi, p, lo, hi in zip(x, points, lows, highs):
        ax.text(xi, p + 30, f"${p}/yr", ha="center", va="bottom", fontsize=11, fontweight="bold")
        ax.text(xi, hi + 55, f"range ${lo}-${hi}", ha="center", va="bottom", fontsize=8, color="#444")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=9.5)
    ax.set_ylabel("Annual household impact, USD")
    ax.set_ylim(0, 1250)
    ax.set_title(
        "Household comparison: 'oppose data centers to save on electricity' vs. real-estate tax reality\n"
        "Net cost to typical PWC household at point estimate: +$549/year (RE tax minus electricity saving)"
    )

    # Net-cost annotation between the two bars.
    ax.annotate(
        "",
        xy=(1, retax_point),
        xytext=(0, elec_point),
        arrowprops=dict(arrowstyle="<->", color="#222", lw=1.1),
    )
    ax.text(
        0.5,
        (elec_point + retax_point) / 2 + 80,
        "net +$549/yr\n(ratio 4.3x)",
        ha="center",
        va="bottom",
        fontsize=10,
        fontweight="bold",
        color="#222",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#fff3e0", edgecolor="#b8860b"),
    )

    ax.text(
        0.0,
        -0.18,
        "Sources: /data/electricity_drivers.csv (30% DC share of the 2022-2026 Dominion residential rate envelope, range 20-45%); "
        "/data/scenario_results.csv CAPEX Spillover FY31 required nominal rate $1.031/$100 vs. FY26 $0.906/$100 on $570,600 median home "
        "(PWC 2025 Real Estate Assessments Annual Report); range reflects CAPEX Spillover parameter band (low Stage 4 + point/high Stage 3b overlay).",
        transform=ax.transAxes,
        fontsize=6.5,
        ha="left",
        color="#444",
    )
    fig.tight_layout()
    fig.savefig(OUT / "fig_electricity_vs_retax.png", bbox_inches="tight")
    plt.close(fig)


# ---------- C&P Cure: rate wall (Reddit graphic 1 of 2) ----------
def fig_cp_cure_rate_wall():
    """Required C&P (data-center personal-property) tax rate by fiscal year if
    the Board attempts to plug the CAPEX Spillover deficit on data-center
    revenue alone. Bars sit against peer-county C&P rates and the +$5/$100
    "leave-Virginia" tip-out threshold from research/va_tax_competitive_notes.md.

    Source: /data/cp_cure_carveout_with_elasticity.csv,
            /data/va_county_tax_stack.csv.
    """
    rows = []
    with open(DATA / "cp_cure_carveout_with_elasticity.csv") as f:
        for r in csv.DictReader(f):
            rows.append(r)

    years = [int(r["fiscal_year"]) for r in rows]
    rates = []
    feasible = []
    for r in rows:
        try:
            rates.append(float(r["required_rate"]))
            feasible.append(r["feasible"].strip().lower() == "true")
        except ValueError:
            rates.append(float("nan"))
            feasible.append(False)

    PWC_FY27 = 4.50
    LOUDOUN = 4.15
    LEAVE_VA = LOUDOUN + 5.00  # $9.15/$100
    INFEASIBLE_DISPLAY = 26.0  # tall bar to communicate "off the chart"

    plot_rates = [r if (f and r == r) else INFEASIBLE_DISPLAY for r, f in zip(rates, feasible)]
    colors = []
    for r, f in zip(rates, feasible):
        if not f or r != r:
            colors.append("#5a0000")  # infeasible: dark red
        elif r > LEAVE_VA:
            colors.append("#d62728")  # past leave-VA threshold
        elif r > PWC_FY27 + 0.5:
            colors.append("#ff7f0e")  # past tolerance band
        else:
            colors.append("#1f77b4")  # within tolerance

    fig, ax = plt.subplots(figsize=(9.0, 5.6))
    x = list(range(len(years)))
    bars = ax.bar(x, plot_rates, color=colors, edgecolor="#222", linewidth=0.7, width=0.62)

    # Reference lines with legend entries
    ax.axhline(PWC_FY27, color="#1f77b4", linestyle="--", linewidth=1.0,
               label=f"PWC FY27 adopted (\\${PWC_FY27:.2f})")
    ax.axhline(LOUDOUN, color="#2ca02c", linestyle="--", linewidth=1.0,
               label=f"Loudoun TY26 (\\${LOUDOUN:.2f})")
    ax.axhline(LEAVE_VA, color="#d62728", linestyle=":", linewidth=1.4,
               label=f"+\\$5 vs Loudoun: leave-Virginia threshold (\\${LEAVE_VA:.2f})")

    # Bar labels
    for xi, r, f, plotted in zip(x, rates, feasible, plot_rates):
        if f and r == r:
            ax.text(xi, plotted + 0.4, f"\\${r:.2f}", ha="center", va="bottom",
                    fontsize=11, fontweight="bold", color="#222")
        else:
            ax.text(xi, INFEASIBLE_DISPLAY + 0.4, "INFEASIBLE\n(no rate ≤ \\$25\nfills the hole)",
                    ha="center", va="bottom", fontsize=9, fontweight="bold", color="#5a0000")

    ax.set_xticks(x)
    ax.set_xticklabels([f"FY{y}" for y in years])
    ax.set_ylabel("Required C&P tax rate, $ per $100 of assessed value")
    ax.set_ylim(0, INFEASIBLE_DISPLAY + 4.0)
    ax.set_title(
        "C&P rate PWC would have to set to plug the CAPEX-spillover deficit on data-center taxes alone"
    )
    # Legend below the plot, three columns, so the plot face stays clean.
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.10), ncol=3,
              fontsize=8.5, frameon=False)

    src = (
        "Sources: /data/cp_cure_carveout_with_elasticity.csv (FY27-FY31 required-rate solve, Schools Item 7-C carve-out, "
        "with new-build elasticity vs. Loudoun differential per research/location_elasticity_notes.md). "
        "Peer rates from /data/va_county_tax_stack.csv. Bar color = orange past tolerance band, red past leave-VA threshold, "
        "dark red where no rate ≤ \\$25/\\$100 closes the gap because the elasticity-induced AV erosion outpaces the rate."
    )
    ax.text(
        0.0, -0.22, "\n".join(textwrap.wrap(src, width=130)),
        transform=ax.transAxes, fontsize=6.8, ha="left", va="top", color="#444",
    )
    fig.tight_layout()
    fig.savefig(OUT / "fig_cp_cure_rate_wall.png", bbox_inches="tight")
    plt.close(fig)


# ---------- C&P Cure: depreciation cliff (Reddit graphic 2 of 2) ----------
def fig_cp_cure_cliff():
    """Data-center C&P revenue trajectory FY27-FY36 under three paths from the
    held-rate simulator in model/cp_cure_scenario.py:
       (a) FY27 adopted baseline at $4.50, normal refresh
       (b) Board holds rate at $7.00 from FY27, refresh slows to 50% by FY31
       (c) Board holds rate at $10.00 from FY27, refresh slows to 25% by FY31
    All three series come from the same cohort-depreciation engine, so the
    FY31->FY32 transition is continuous.

    Source: /data/cp_cure_baseline_fy27_fy36.csv,
            /data/cp_cure_held_rate7_fy27_fy36.csv,
            /data/cp_cure_held_rate10_fy27_fy36.csv.
    """
    def read_traj(path):
        out = {}
        with open(path) as f:
            for r in csv.DictReader(f):
                out[int(r["fiscal_year"])] = float(r["cp_revenue"]) / 1e6
        return out

    baseline = read_traj(DATA / "cp_cure_baseline_fy27_fy36.csv")
    rate7 = read_traj(DATA / "cp_cure_held_rate7_fy27_fy36.csv")
    rate10 = read_traj(DATA / "cp_cure_held_rate10_fy27_fy36.csv")

    years = sorted(baseline.keys())
    base_y = [baseline[y] for y in years]
    r7_y = [rate7[y] for y in years]
    r10_y = [rate10[y] for y in years]

    fig, ax = plt.subplots(figsize=(9.6, 5.8))
    ax.plot(years, base_y, color="#1f77b4", lw=2.4, marker="o",
            label="Baseline: rate held at \\$4.50, refresh normal")
    ax.plot(years, r7_y, color="#ff7f0e", lw=2.4, marker="s",
            label="Hike to \\$7.00, operators slow refresh in PWC (50% by FY31)")
    ax.plot(years, r10_y, color="#d62728", lw=2.4, marker="^",
            label="Hike to \\$10.00, operators slow refresh in PWC (25% by FY31)")

    ax.axvspan(2031.5, 2036.5, color="#fde8e8", alpha=0.55,
               label="Depreciation-cliff window (FY32-FY36)")

    # Year-1 uplift annotation: $10 path gets the largest one-year revenue spike.
    spike_y = rate10[2027]
    ax.annotate(
        f"Year-1 uplift:\n\\${spike_y:.0f}M at \\$10 rate\n(base still intact)",
        xy=(2027, spike_y), xytext=(2027.1, 610),
        fontsize=9, color="#444",
        arrowprops=dict(arrowstyle="->", color="#444", lw=0.8),
    )
    # Cliff-floor annotation
    floor_val = rate10[2033]
    ax.annotate(
        "Schedule C floor:\n5% of original cost\nafter 4 years",
        xy=(2033, floor_val), xytext=(2033.4, 540),
        fontsize=9, color="#444",
        arrowprops=dict(arrowstyle="->", color="#444", lw=0.8),
    )
    # Crossover annotation: where does each hike path fall below baseline?
    cross7 = next((y for y in years if rate7[y] < baseline[y]), None)
    cross10 = next((y for y in years if rate10[y] < baseline[y]), None)
    cross_text_lines = []
    if cross7:
        cross_text_lines.append(f"\\$7 hike falls below baseline by FY{cross7}")
    if cross10:
        cross_text_lines.append(f"\\$10 hike falls below baseline by FY{cross10}")
    if cross_text_lines:
        ax.text(0.98, 0.96, "\n".join(cross_text_lines),
                transform=ax.transAxes, fontsize=9, ha="right", va="top",
                bbox=dict(boxstyle="round,pad=0.35", facecolor="#fff3e0",
                          edgecolor="#b8860b", linewidth=0.8))

    ax.set_xticks(years)
    ax.set_xticklabels([f"FY{y}" for y in years], rotation=0)
    ax.set_ylabel("Data-center C&P tax revenue, \\$M / year (nominal)")
    ax.set_xlabel("")
    ax.set_ylim(0, 700)
    ax.set_title(
        "PWC data-center C&P revenue if a sustained rate hike triggers operators to slow refresh in PWC"
    )
    ax.legend(loc="lower left", fontsize=8.8)

    src = (
        "Sources: /data/cp_cure_baseline_fy27_fy36.csv, /data/cp_cure_held_rate7_fy27_fy36.csv, "
        "/data/cp_cure_held_rate10_fy27_fy36.csv. All three trajectories produced by the same cohort-depreciation engine "
        "in model/cp_cure_scenario.py (PWC Schedule C 50/35/20/10/5%, floor at year 4) with new-build elasticity vs. "
        "Loudoun differential (research/location_elasticity_notes.md) and a refresh-slowdown that converges over five years."
    )
    ax.text(
        0.0, -0.17, "\n".join(textwrap.wrap(src, width=130)),
        transform=ax.transAxes, fontsize=6.8, ha="left", va="top", color="#444",
    )
    fig.tight_layout()
    fig.savefig(OUT / "fig_cp_cure_cliff.png", bbox_inches="tight")
    plt.close(fig)


def main():
    data = load_scenario_results()
    fig_revenue_mix_fy26()
    fig_scenario_deficit(data)
    fig_fy27_adopted_vs_scenarios(data)
    fig_required_tax_rate(data)
    fig_reserve_trajectory(data)
    fig_debt_service_ratio(data)
    fig_canceled_capex()
    fig_peer_county_permits()
    fig_spillover_channels()
    fig_revenue_hole(data)
    fig_options_menu()
    fig_electricity_drivers()
    fig_electricity_vs_retax()
    fig_cp_cure_rate_wall()
    fig_cp_cure_cliff()
    print("Wrote figures to", OUT)


if __name__ == "__main__":
    main()
