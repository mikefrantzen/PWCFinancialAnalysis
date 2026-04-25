---
title: "C&P Cure Scenario — Can a C&P Rate Hike Plug the CAPEX Spillover Deficit?"
subtitle: "Stage 8 fourth-scenario analysis"
date: 2026-04-25
horizon: FY27–FY31 (rate-hike window) + FY32–FY36 (depreciation cliff)
inputs:
  - research/depreciation_regime_notes.md
  - research/location_elasticity_notes.md
  - research/va_tax_competitive_notes.md
  - model/cp_cure_scenario.py
  - data/cp_cure_*.csv
---

# Premise

Layer a fourth scenario on top of CAPEX Spillover. The hypothesis under test: the Board, faced with the FY27–FY31 cumulative $1,151M deficit derived in Stage 6b, attempts to close the gap entirely by raising the data-center C&P tax rate above the FY27 adopted $4.50/$100. The scenario answers four questions:

1. What rate is required, year by year, to plug the annual CAPEX Spillover deficit on C&P revenue alone?
2. Does the rate hike trigger a behavioral response (new-build redirection + refresh-cycle slowdown) that erodes the C&P assessed-value base?
3. Does PWC's Schedule C depreciation curve (50/35/20/10/5%, floor at year 4) produce a revenue cliff if the behavioral response sticks?
4. Combined with Virginia's possible 2027 modification of the data-center sales-and-use tax exemption (Va. Code § 58.1-609.3(18)), where do hyperscalers actually redirect — outside PWC, outside Northern Virginia, or outside Virginia?

Model code: `model/cp_cure_scenario.py`. Outputs: `data/cp_cure_*.csv`.

# Headline finding

**The C&P Cure strategy works for exactly one year, then becomes infeasible.**

| FY | Required C&P rate (Schools carve-out) | Differential vs Loudoun ($4.15) | Behavioral response |
|---|---:|---:|---|
| 2027 | **$4.73** | +$0.58 | Within tolerance; new-build factor 100% |
| 2028 | **$15.34** | +$11.19 | Past leave-VA threshold; new-build factor 27.6%, effective new CAPEX collapses from $4.9B to $1.34B |
| 2029 | **$24.66** | +$20.51 | At rate-cap, AV-elasticity feedback loop binding; new-build factor at the 20% floor |
| 2030 | **INFEASIBLE** | — | No rate ≤ $25/$100 closes the gap given the elasticity-induced AV erosion |
| 2031 | **INFEASIBLE** | — | Same |

Under the Schools-shared treatment (no Item 7-C carve-out for the further increment), only FY27 has a feasible rate ($7.25). FY28–FY31 are all infeasible — Schools claims 57.23% of the marginal C&P revenue, which roughly doubles the rate needed, pushing every year past the AV-erosion cliff.

The strategy is self-defeating. By FY28 the required rate already exceeds the +$5/$100 "leave-Virginia" tip-out threshold identified in the location-elasticity research. The very behavioral response that the rate hike provokes — operators redirecting net-new CAPEX to Loudoun, Henrico, the Fredericksburg compact, Berkeley County WV, or out of state — collapses the C&P assessed-value base that the Board is taxing. Higher rate × shrinking base does not converge.

# Why the model says infeasible

The C&P revenue formula is `revenue = rate × AV / 100`. Both terms move together when the Board hikes the rate:

- **Rate up.** Each $0.10 of additional rate adds revenue in proportion to AV. At an FY27 baseline AV of ~$5.9B (calibrated to match CAPEX Spillover DC revenue), each $0.10 = $5.9M.
- **AV down.** The behavioral response cuts new gross capitalized cost added to PWC's books. The piecewise-linear elasticity (research/location_elasticity_notes.md §6, calibrated to industry-survey thresholds in research/va_tax_competitive_notes.md):
  - $0–$1 differential vs Loudoun: 0% reduction (tolerance band)
  - $1–$2: 0–5% (Bisnow-cited operator commentary)
  - $2–$5: 5–30% (inflection range; net-new redirected)
  - $5–$10: 30–70% (leave-VA threshold crossed)
  - $10+: capped at 80% (existing fiber/peering lock-in keeps a residual)
- **Compounding via PWC Schedule C.** New CAPEX gets only 50% AV factor in year 0, but it is the source of replacement vintages that keep the cohort book full. Once a vintage hits year 4+, it sits at the 5% floor permanently. Suppress new CAPEX for two years and the AV trajectory begins to bleed irreversibly.

The model's iterative solver demonstrates this mechanically: at FY28 the rate has to absorb both a higher target deficit ($154M vs. $84M FY27) AND a smaller AV base (because FY27's new CAPEX was already reduced by elasticity). By FY29 the AV base has shrunk further; by FY30 there is no rate within a politically-defensible cap that closes the gap.

# Depreciation cliff (FY32–FY36)

If the Board sustains the high rate and operators respond by halting refresh, the existing C&P base depreciates through PWC Schedule C until it sits at the 5% floor.

**Cliff under $7.00 rate held flat, 50% refresh halt:**

| FY | C&P AV | C&P revenue |
|---|---:|---:|
| 2032 | $6.55B | $458.9M |
| 2033 | $5.91B | $413.5M |
| 2034 | $5.64B | $395.0M |
| 2035 | $5.64B | $395.0M |
| 2036 | $5.78B | $404.6M |

Revenue stabilizes around $400M because the 50% refresh-rate baseline keeps adding new vintages.

**Cliff under $7.00 rate held flat, 100% refresh halt:**

| FY | C&P AV | C&P revenue |
|---|---:|---:|
| 2032 | $5.18B | $362.6M |
| 2033 | $3.57B | $249.9M |
| 2034 | $2.75B | $192.8M |
| 2035 | $2.48B | $173.6M |
| 2036 | $2.48B | $173.6M |

Revenue collapses 52% in four years and reaches steady-state at the floor of the 2026–2031 vintage cohorts. **Even at a $10 rate with full refresh halt, FY36 revenue is $248M — about 30% below the FY27 baseline of ~$350M.** The cliff is structural: at PWC's 4-year-to-floor schedule, any sustained refresh suppression creates a revenue collapse on the same timescale.

# Two cliffs the FY27 budget already reveals (separate from the rate-hike scenario)

The depreciation regime research (research/depreciation_regime_notes.md §4) flags two slower-moving cliffs that exist regardless of whether PWC raises C&P:

1. **Refresh-cycle lengthening.** Hyperscalers extended GAAP useful life from 4 years (2018–2022) to 5–6 years (2024–2025) — Microsoft 4→6, Google 4→6, Meta 4→5.5, AWS 4→6 (then 6→5 in 2025 citing AI workload pace). PWC's 4-year-to-floor curve doesn't care about book life — but operators only file actual capitalized-cost retention. If they hold equipment 6 years instead of 4, **at any steady state ~33–50% of the installed base sits at the 5% floor** vs. ~20% under a 5-year refresh. The FY27 PWC C&P revenue is implicitly forecasting a younger vintage mix than actual fleet aging may produce.
2. **OBBBA 100% bonus depreciation (federal).** The One Big Beautiful Bill Act (enacted 2025-07-04) restored 100% bonus depreciation permanently. This is irrelevant for PWC's local C&P AV (PWC applies its own Schedule C regardless of federal treatment) — but it sharpens federal tax incentives for *new* hyperscaler CAPEX, which competes for the same boards-of-directors approval that the Board's rate signals against. The two policy paths point in opposite directions.

# Location elasticity — does CAPEX leave PWC, NoVa, or Virginia?

The research synthesizes the answer in three layers:

**Layer 1 — outside PWC, inside NoVa.** Loudoun is the obvious near substitute at $4.15/$100 vs. PWC's $4.50, with similar power, network, and fiber. Loudoun's TY2026 schedule (60/45/30/15/10/5) is also less aggressive than PWC's (i.e., higher AV retention). At PWC differential of +$1–2, the redirect is mild and absorbed within the regional cluster. Fairfax at $4.57 is roughly tied with PWC. Henrico raised to $2.60 (from $0.40) in 2025 and remains attractive. The Fredericksburg compact (Stafford / Spotsylvania / Caroline / King George at $1.25 dedicated DC class) is positioned for marginal redirect within the hour drive of PWC's existing operator footprints.

**Layer 2 — outside NoVa, inside Virginia.** Stafford / Spotsylvania picked up Loudoun overflow after the 2025 by-right elimination; expect the same to happen to PWC at differential ≥$2. Henrico (White Oak) is the most analogous "post-recruitment normalize" peer pivot — went from $0.40 to $2.60 without losing the cluster. Culpeper has town-level negotiated agreements and a county BPP of ~$2.05.

**Layer 3 — outside Virginia.** The leave-VA threshold sits around +$5/$100 differential vs. Loudoun, conditioned on the 2026 General Assembly outcome on the sales-and-use tax exemption. **The first multi-billion-dollar post-Pageland announcement explicitly outside Virginia is Berkeley County WV's $4B / 550-acre development reported as Google in February 2026.** Berkeley County's effective tax yield is ~30% of nominal under WV's 2023 microgrid law, but the political signal is that hyperscalers are already pricing in a non-Virginia option. Maryland (Frederick, Howard, Montgomery) offers a 10-year sales/use exemption. Texas, Arizona, Iowa, Oregon, Ohio all have permanent or long-duration property/sales-tax incentives.

**Recapitalization vs. new build.** The elasticities differ sharply (location_elasticity_notes.md §6):
- **New build:** −1.0% to −1.5% per +$1/$100 differential, with strong threshold effects above +$2.
- **In-place refresh:** −0.1% to −0.3% in years 1–3, rising to −0.5% to −1.0% per year over 7+ years. Equipment is sticky once a building is operational; the operator has the contracts, the network drops, the power. They can slow refresh and let PWC's Schedule C run the AV down — that's the cliff in the section above.

The tactical move under any sustained PWC rate divergence is the slow refresh, not the dramatic abandonment. That is the worst outcome for the Board: the rate hike doesn't trigger a visible exit, just a quiet AV slide that shows up on the FY30–FY32 audit as "DC C&P revenue declined despite higher rate."

# Combined with the 2027 Virginia exemption fight

The exemption-fight research (research/va_tax_competitive_notes.md) places the modal 2027–2028 outcome at a **partial extension to 2050 with conditions** (35–40% probability), with status quo (25–30%), pure repeal (10–15%), per-facility cap (15–20%), and a layered consumption excise (25–30%, possibly stacked).

If the exemption is materially tightened (~50% bundled probability), operators face a one-time 5–7% cost stack increase per refresh cycle ($60–90M one-time per 100-MW PWC campus, $20–30M/yr steady state). This compounds with any local C&P hike: the operator's "should I refresh in PWC or in Berkeley County WV" decision loses the state-level exemption advantage at the same time PWC pushes the local rate higher.

The C&P Cure model layers this as a uniform 6% drag on new CAPEX (`apply_exemption_loss=True`); the additional drag pushes FY27 from a $4.73 feasible rate to $4.94, and FY28 from $15.34 to $16.72 — but does not change the FY29–FY31 infeasibility verdict. The exemption fight does not save the C&P Cure strategy; it modestly worsens it.

# Implications

If the policy response to the CAPEX Spillover scenario is "raise C&P to fill the gap," the model finds:

1. **Year 1 ($4.73, +$0.23 from FY27 adopted) is feasible** — the rate is still within the regional tolerance band.
2. **Year 2 requires a 3.4× rate increase** to $15.34, past every observed regional precedent and across the leave-VA tip-out threshold. The behavioral response from year 1 already begins compounding.
3. **Years 4–5 are infeasible** at any rate ≤ $25/$100. The deficit is locked in; the rate path required by FY28 forfeits the C&P AV base the policy is taxing.
4. **The depreciation cliff is structural and arrives within the standard PWC five-year financial-forecast window.** Once new CAPEX is suppressed, AV declines to floor in 4 years regardless of rate.

The combined finding is that the C&P Cure is not a partial solution that closes part of the gap — it produces a one-year revenue uplift followed by a structural reduction in the C&P revenue base. **The expected NPV across FY27–FY36 (10-year horizon, including the cliff) is plausibly negative versus the no-hike CAPEX Spillover baseline.** A formal NPV computation, using a 4% discount rate and the cliff trajectories above, is the appropriate next step.

# Caveats and gaps

- **Vintage distribution of the existing $15.68B gross book is not public** at the cohort-by-acquisition-year level. PWC Tax Administration has it; FOIA request was recommended in the depreciation-regime research note. The cliff math uses a uniform-vintage approximation that the TY2024 actual 25.4% AV ratio supports but does not validate cohort-by-cohort.
- **Elasticity calibration is qualitative.** The piecewise function is anchored to documented thresholds (+$1 tolerance / +$2 inflection / +$5 leave-VA) but no published cross-sectional regression exists to estimate elasticity points directly. The Loudoun 2025 by-right elimination is the closest natural experiment; we used its observed −53% YoY residential-permit differential as a magnitude check.
- **Schools carve-out is a Board policy variable, not a calculation.** Item 7-C carved the FY26→FY27 $0.35 increment out of the 57.23% formula. Whether further increments would receive the same treatment is unmodeled and unknowable; the report shows both extremes.
- **The model treats new CAPEX as the only swing variable.** In reality operators also have refresh-timing flexibility (a separate axis with longer lags); we apply a small refresh-slowdown factor but do not model the 6-year refresh cycle explicitly. That refinement would show the cliff arriving slightly later and shallower.
- **No NPV / discount-rate analysis yet.** The "feasible only in year 1" finding is robust on undiscounted nominal terms. Discount-rate sensitivity is the natural next step.

# Recommendation for next steps

1. Run the formal NPV at 3.5–5% discount rates to confirm that the rate-hike strategy is net-negative under any plausible realization of the elasticity range.
2. FOIA PWC Tax Administration for cohort-by-acquisition-year aggregate Schedule C totals to sharpen the cliff math.
3. Consider a "rate-hike + cure" hybrid scenario: modest C&P hike (+$0.50 to $5.00) combined with the §1 ordinance cure-by-re-enactment to recapture some Pageland CAPEX. This is plausibly the best feasible policy combination for the Board.
4. Document the C&P Cure infeasibility result in any forward policy discussion: the policy space for revenue-side cures is narrower than the per-year required-rate calculation alone implies, because the elasticity-induced AV erosion and the Schedule C depreciation cliff together close off the strategy by FY30.
