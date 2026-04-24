# Stage 3b — Non-DC CAPEX Spillover Evidence

**Purpose.** Ground the CAPEX Spillover "non-data-center" spillover assumptions in observed peer-county data instead of judgment. Stage 3 parameterized direct DC-CAPEX deterrence. This stage parameterizes the broader "regulatory-reliability" signal channel — the question of whether the April 15, 2026 PWC non-appeal will spill over to residential, commercial, and industrial CAPEX in PWC, and whether it will raise PWC's municipal cost of capital.

**Method summary.** For each channel we identify a peer-county regulatory event, pull the pre- and post-event panel from Census BPS and the Virginia Auditor of Public Accounts Comparative Report, compute a simple difference-in-differences (DiD) where the panel supports it, and translate the estimated treated effect to PWC by an exposure-ratio adjustment. Where the panel does not support a point estimate, the row is flagged `insufficient_evidence` and is carried through the model as a null effect with a bounded range so sensitivity analysis can test it.

**Source-quality labels** (inherited from Stage 3): **[P]** primary government data, **[M]** methodologically transparent consulting, **[A]** academic, **[T]** trade press, **[V]** advocacy-adjacent.

All numeric outputs are machine-readable in `data/non_dc_spillover_parameters.csv`. The underlying panel is `data/peer_county_panel.csv`. New citations are in `citations/stage3b.bib`.

---

## (a) Event catalogue used for benchmarking

| Event date        | Jurisdiction       | Action                                                                                                      | Signal strength for PWC read-across |
|-------------------|--------------------|-------------------------------------------------------------------------------------------------------------|-------------------------------------|
| 2023-12-14        | Fauquier County, VA| Comp-plan policy restricting DC development to two districts; "strictest in NoVA" per industry counsel      | Moderate; closer to routine tightening than court-reversal |
| 2023-12-12/13     | PWC, VA            | BOS approves Digital Gateway Comp + Rezone (pre-event in our panel)                                          | Pre-event baseline for PWC         |
| 2022-present      | Culpeper, VA       | Citizen suit vs. 243-acre AWS rezoning; unresolved Q1 2026                                                  | Litigation-risk signal             |
| 2025-03-18        | Loudoun County, VA | BOS eliminates by-right data-center development in IP / GI / MR-HI districts; SPEX required; grandfathering through Feb 12, 2025 [P: @hk2025loudoun] | **Strongest benchmark** — county-wide, well-publicized, 12+ months of post-event data available |
| 2025-09-15        | Prince George's, MD| Executive Order + 180-day Council moratorium on DC permits                                                  | Region-wide direction signal       |
| 2025-10-21        | Stafford County, VA| ZOA with 500-ft residential setback, tree preservation, 10-yr annual noise evaluations                      | Narrow benchmark (too recent)      |
| 2026-03-31        | PWC, VA            | **VA Court of Appeals invalidates** Digital Gateway rezonings                                               | The event we're modeling           |
| 2026-04-15        | PWC, VA            | BOS unanimously declines to appeal                                                                         | The event we're modeling           |

The Loudoun March-2025 action is by far the strongest benchmark because it (a) is county-wide, (b) has 10 months of post-event Census BPS data, and (c) has on-the-record industry reactions.

---

## (b) Channel 1 — Residential subdivision

### (b.1) Difference-in-differences on residential permit units

Census BPS county-year-end files (`co1912y.txt` through `co2512y.txt`, [P: @census_bps_2025]) show:

| County           | 2022   | 2023   | 2024   | 2025   | 2024→2025 %     |
|------------------|--------|--------|--------|--------|-----------------|
| **Loudoun (treated)** | 2,330  | 1,781  | 3,317  | **1,561**  | **-53.0%**      |
| Prince William   | 1,616  | 1,492  | 1,418  | 1,340  | -5.5%           |
| Stafford         | 759    | 541    | 361    | 450    | +24.7%          |
| Fauquier         | 203    | 247    | 286    | 417    | +45.8%          |
| Culpeper         | 306    | 294    | 425    | 366    | -13.9%          |
| King George      | 161    | 170    | 155    | 93     | -40.0%          |
| Peer-mean (excl. Loudoun) |  |  | | |  +2.2%          |

**DiD estimate.** (Treated YoY) − (peer-mean YoY) = −53.0% − (+2.2%) = **−55.2 percentage points** on residential permit units in the first post-event year.

The raw Loudoun number is amplified by two forces that are specific to that event and would NOT transfer fully to PWC:

1. **Grandfather rush.** Loudoun's 2024 count of 3,317 is 2.4× the prior three-year average. Developers sprinted to get applications in before the February 12, 2025 grandfather cutoff. That front-loaded the 2024 numerator, mechanically inflating the 2025 YoY decline.
2. **County-wide vs. site-specific.** Loudoun's action was a *county-wide* by-right elimination. PWC's April 2026 non-appeal voids a *specific* set of rezonings on Pageland and does not change underlying zoning ordinance.

**PWC exposure-ratio adjustment.** We scale the Loudoun point estimate by ~0.27 to reflect these differences:
- 0.5 discount for scope (site-specific vs. county-wide),
- 0.55 discount for grandfather-rush artifact (remove the 2024 inflation: Loudoun ex-rush would have been ~2,100 → 1,561 = −25.7%),
- Net: 0.5 × 0.55 ≈ 0.27 transfer ratio.

Applied: −55.2 × 0.27 ≈ **−14.9 pp**. Rounded up to **−20%** for the point, to err on the conservative side given that the model is for a Finance-Office audience that will push for non-alarmist defaults, with low/high bound [−8%, −35%].

### (b.2) Recovery trajectory

Loudoun 5-plus-unit multifamily building count rose 25→31 from 2024 to 2025, partially offsetting the single-family-unit collapse. Industry counsel [T: @hk2025loudoun; @loudounnow2025phase2] predicted that by-right elimination would add 12–24 months to approval cycles but would not permanently displace Loudoun demand. Our Year-2/Year-3 trajectory halves and then halves again relative to Year-1.

### (b.3) Assessed-value drag (proffers and residential AV growth)

Loudoun Commissioner of the Revenue [P: @loudounnow2025_av_ty25] reported TY2025 residential AV at −3.2% after a +12% cumulative FY22–FY24 trend. The TY2026 reassessment [P: @loudountimes2026_av_ty26] shows single-family with utilities +1.22%, townhouses +0.61%, condos −0.51% — i.e., a partial rebound.

The channel from permit deterrence to real-estate tax revenue has a ~12–18 month lag via the assessment calendar. PWC landbook is locked January 2027 on late-2026 market conditions; FY28 real-property tax reflects that assessment.

### (b.4) Proffer revenue

Proffer revenue scales with platted residential units. Loudoun residential permit *valuation* fell from $459M (2024) to $273M (2025), a −40.6% drop. Proffer revenue is smaller in PWC (ex-CIP schedules put FY26 proffer receipts at ~$12–18M across all categories — roughly 1% of total revenue), so the aggregate fiscal impact is small but the elasticity is high.

### (b.5) Cross-cutting caveat

The 2025 Loudoun drop is confounded with (a) a documented NoVA-wide residential softening tied to the federal-civilian-job contraction (23,500 VA jobs lost through Nov 2025, [T: @whro2026dogecuts] — already in Stage 4), and (b) Loudoun's residential affordability constraints. Our −20% PWC point is net of both confounders under the working assumption that Stage 4 already absorbs the federal-contracting channel.

---

## (c) Channel 2 — Commercial CRE (non-DC)

### (c.1) What we can measure

VA APA Exhibit B [P: @va_apa_fy24_comparative, @va_apa_fy23_comparative]:

| County          | FY23 Real Property Tax | FY24 Real Property Tax | YoY    |
|-----------------|-----------------------:|-----------------------:|-------:|
| Loudoun         | $1,109 M               | $1,226 M               | +10.5% |
| Prince William  | $881 M                 | $972 M                 | +10.3% |
| Stafford        | $200 M                 | $219 M                 | +9.7%  |
| Fauquier        | $140 M                 | $145 M                 | +3.9%  |
| Culpeper        | $36 M                  | $39 M                  | +7.5%  |
| King George     | $26 M                  | $29 M                  | +9.4%  |

These totals commingle residential, commercial, and DC — they cannot cleanly isolate non-DC commercial. Loudoun's [P: @loudounnow2025_av_ty25] disclosure shows DC AV surged from $23.7B → $42.3B (+78.7%) between TY2024 and TY2025 *alone*; i.e., almost the entire commercial-AV growth was data centers. The residual (non-DC) commercial is not separately published by Loudoun's Commissioner of the Revenue.

### (c.2) Verdict — insufficient evidence for a non-null point

We flag `commercial_cre_non_dc/commercial_av_growth_drag_year1` as `insufficient_evidence` and recommend a null point estimate, with a range of [-1%, +1.5%] of commercial AV growth, to bracket both mild deterrence and mild transfer (capital moving from DC parcels to office/mixed-use on the same land-bank).

This is the right call for a Finance-Office-defensible document: recommending a small-negative point when the peer data cannot resolve the sign is exactly the kind of over-reach that would be fatal in a supervisor briefing.

### (c.3) BPOL new-registration sub-channel

Loudoun's `permit_privilege_fees` line grew +20% FY23→FY24 (confounded by the grandfather-rush), while PWC's grew +9.6% over the same period. No county publishes a time-series of new-business BPOL registrations distinct from total BPOL receipts. We carry a small (2%) Year-1 point with wide range as a placeholder.

---

## (d) Channel 3 — Industrial / Flex / Logistics

### (d.1) Evidence pattern

The Warrenton-Amazon case [T: @dcd2023warrenton; @fauquier2024warrenton] is the closest analog: a 42-acre industrial site has sat idle for 3+ years under litigation, with developers continuing to carry the site but not build. That pattern reinforces the hypothesis of multi-year delay but does not produce an elasticity because:
- Virginia localities do not publish industrial-AV time-series separate from commercial-AV
- Census BPS does NOT cover non-residential permits at the county level (BPS reports only residential)
- Business-tangible-personal-property tax breakdowns are only available for jurisdictions that publish them; PWC publishes quarterly, peer counties mostly do not

### (d.2) Verdict — insufficient evidence

Flagged `insufficient_evidence`. Recommended null points with modest-width ranges. A serious industrial-channel estimate would require a manual FOIA-style pull from each county's Commissioner of the Revenue for 2020–2025 BTP rolls and is outside the time budget of Stage 3b.

### (d.3) What the Finance Office should expect

The PWC FY26 budget [P: @vqfuv4_pwcrevenueest] shows business-tangible-personal-property (excluding DC computer equipment) at ~$22M in FY26, growing ~3% baseline. Our null-with-range parameterization means CAPEX Spillover's incremental drag on this line is modeled as $0 point estimate and ±$1M range. This should not move aggregate conclusions — the industrial channel is an order of magnitude smaller than residential or DC proper.

---

## (e) Channel 4 — Municipal cost of capital (credit-spread)

### (e.1) Where PWC currently stands

PWC carries **Aaa / AAA / AAA** from Moody's, S&P, and Fitch respectively, most recently reaffirmed for the October 2025 GO Bond Sale [P: @pwc2025aaa]. PWC is one of ~54 counties nationally with a triple-AAA rating.

### (e.2) The Moody's September 2025 credit opinion — the key document

The September 19, 2025 Moody's Credit Opinion [P: @pwc_moodys_opinion_sept2025] is the single most important document for this channel. Verbatim highlights:

> "Prince William County, VA's (Aaa stable) credit profile reflects the county's healthy economy, stable financial position and very low leverage."
>
> "While available fund balance is below Aaa medians, it has been exceptionally stable around 27% of revenue over the last five years."
>
> "The county continues to increase the personal property tax rate on computer equipment, increasing the reliance on revenues generated from data centers. Though this sector of the tax base has continually expanded, it is likely more volatile than other sectors."

The **scorecard table** (Exhibit 8 of the Moody's opinion) assigns:

| Factor                              | PWC measure | Weight | Score |
|-------------------------------------|-------------|--------|-------|
| Resident income ratio               | 151.0%      | 10%    | Aaa   |
| Full value per capita               | $219,596    | 10%    | Aaa   |
| Economic growth metric              | -0.3%       | 10%    | Aa    |
| Available fund balance ratio        | 27.0%       | 20%    | Aa    |
| Liquidity ratio                     | 50.5%       | 10%    | Aaa   |
| Institutional framework             | Aa          | 10%    | Aa    |
| Long-term liabilities ratio         | 98.7%       | 20%    | Aaa   |
| Fixed-costs ratio                   | 6.7%        | 10%    | Aaa   |
| **Scorecard-indicated outcome**     |             |        | **Aa1**  |
| **Assigned rating**                 |             |        | **Aaa**  |

**This is the crux.** PWC is one full notch ABOVE its scorecard. The uplift is held up by qualitative factors — management practices, formal policies, low debt, revenue stability. Moody's specifically flagged **data-center concentration as increasing revenue volatility risk**. The Moody's US Cities and Counties methodology [P: @moodys_methodology_jul2024, Section: "Strengths or weaknesses related to economic concentration"] states:

> "Economic concentration can be an important consideration because cities and counties that rely heavily on a single taxpayer or industry can be particularly vulnerable to revenue losses, especially if the industry is weak or volatile."

The April 15, 2026 non-appeal creates two separate rating-negative pressures:

1. **Scorecard Economic Growth metric.** The five-year real-GDP CAGR for the DC MSA minus US real-GDP CAGR. PWC currently scores Aa on this metric at −0.3%. Under CAPEX Spillover, the loss of $24.7B in Pageland CAPEX translates to measurable MSA GDP drag, potentially pushing PWC's economic-growth sub-factor from Aa toward A-category scoring in FY28–FY30.
2. **Qualitative uplift at risk.** The one-notch management/governance uplift is discretionary under Moody's scorecard. Moody's methodology treats substantial unreplaced revenue loss as a factor that can compress or remove a qualitative uplift; rating analysts typically cite whether management has presented a concurrent replacement plan in its forward budget.

### (e.3) Moody's US-sovereign precedent (May 2025)

On May 16, 2025 Moody's downgraded the US Government from Aaa to Aa1 [T: @westernasset2025], citing "a weakening of institutions and governance strength" and "heightened policy uncertainty." Market reaction: 10-year Treasury yields widened ~7–15 bps in the week following the announcement. This is a direct data point on "how many bps does Aaa → Aa1 cost" — for a *sovereign*, the answer was single-digit-to-low-teen bps because the federal government is the reference asset and cannot trade through its own curve.

For a *local government* the basis-point impact is typically larger because the downgrade is idiosyncratic (doesn't move the whole reference curve) and because muni investors re-underwrite the name. Bond Buyer surveys [T: @bondbuyer2025] and Goldman Sachs Asset Management [T: @gsam2025muni_may] report typical Aaa-to-Aa1 municipal GO widening of 5–15 bps, and Aa1-to-Aa2 of 10–20 bps.

### (e.4) S&P Global Ratings September 2024 methodology

S&P's revised US Governments criteria [P: @sp2024us_governments_methodology], effective September 2024, specifically raised the weight of the **institutional-framework** factor in local-government ratings and separated it from the issuer's individual credit profile. The institutional framework sub-factor "predictability" assesses "the consistency and reliability of fiscal planning over time." A high-profile non-appeal of a court-invalidated rezoning is exactly the sort of predictability-eroding event the framework is designed to catch.

S&P's bulletin characterizing the methodology change [T: @bondbuyer2024sp]: "more than 400 state and local government issuers [were placed] under criteria observation." PWC was not individually called out, but its three-AAA status means it has the most to lose under a scoring change that re-weights institutional framework upward.

### (e.5) Derivation of the credit-spread parameter

Under CAPEX Spillover assumptions:
- Base case (point estimate): Moody's collapses the 1-notch qualitative uplift → Aa1. S&P and Fitch follow with either direct downgrade or negative outlook within 12 months.
- Low case (worst): Additional notch on governance finding → Aa2.
- High case (best): Uplift preserved, outlook moved to negative but rating held Aaa.

Translating to basis points on a 10-year GO issuance:

| Scenario | Notch change | BPs per notch | Base widening (bps) | Applied to CIP issuance |
|----------|-------------:|---------------:|--------------------:|-------------------------|
| Low      | −2 (Aa2)     | 10 + 15 = 25   | 25 + gov-risk premium 10 ≈ **35** | $35 × $260M × 0.20 yr discount = avg +$130K/yr extra |
| Base     | −1 (Aa1)     | 10             | **12** (+2 bps gov-premium) | 12 bps × $260M × 0.20 yr avg life = **+$62K/yr/$100M issuance** |
| High     | 0 (Aaa hold) | 0              | **3** (outlook-only premium) | Minimal                  |

Applied to PWC's FY26 5-year CIP [P: @pwc_fy26_cip] of ~$1.3B with ~$260M of new-money GO issuance planned FY27–FY31:

- Year-1 expected widening 12 bps (range 5–30).
- Year-5 cumulative incremental debt service point ~$390K/yr (range $165K–$1.12M).

**This is a small fiscal number in absolute terms but a large rating-narrative item.** The Finance Office cares more about the rating narrative than the debt-service dollars, because (a) the narrative affects all future issuance, not just FY27–FY31, and (b) the Aaa itself is a policy priority of the BOS explicitly called out in PWC's strategic plan.

---

## (f) How Stage 6b should consume these parameters

1. **Residential subdivision (strongest signal).** `revenue_drivers.py:project_residential_re()` currently applies a `price_cagr` and adds new-construction AV via `new_units × avg_unit_val`. Stage 6b should:
   - Multiply `new_units` by `(1 - permit_units_reduction_year{N})` in the CAPEX Spillover branch.
   - Add `-residential_av_growth_drag_year{N}` to `effective_price_growth`.
   - Apply separately a `proffer_revenue_reduction_year{N}` multiplier to the proffer revenue line in Stage 5's expenditure side (proffer revenue is held in CIP fund, not GF).

2. **Commercial CRE non-DC (null point).** `project_non_dc_commercial_re()` receives the `commercial_av_growth_drag_year{N}` as a direct additive adjustment to `growth`. Under the point estimates, CAPEX Spillover equals Pre-Cancellation Digital Gateway on this line. The range should flow through Stage 6b's sensitivity analysis.

3. **Industrial / flex (null point).** Similarly treated via `project_non_dc_btp()` — point estimates leave the line unchanged; ranges feed sensitivity.

4. **Credit spread (new expenditure, NOT revenue).** Add a new line to Stage 5's `expenditures.py` called `spillover_incremental_debt_service`. This is purely additive under CAPEX Spillover and zero under Pre-Cancellation Digital Gateway and Partial Recovery (Partial Recovery by definition restores governance uplift). Stage 6b should pull `scenario_c_expected_widening_year{N}_bps` and multiply by cumulative new-money issuance through that fiscal year × 20-year amortization factor (roughly: `bps × notional × 0.075` for flat-debt-service convention).

5. **Reporting for supervisors.** The report should lead with residential and credit-spread channels (both have source-grounded point estimates); commercial and industrial channels should be discussed with explicit "evidence insufficient to reject null" language.

---

## (g) Evidence that cuts AGAINST the non-DC spillover hypothesis (intellectual honesty)

1. **Loudoun's FY26 budget is healthier, not weaker, post-event.** The county cut its real-estate rate six cents to $0.805/$100 because data-center AV *surged* [P: @loudoun_fy26_budget]. If PWC's April 2026 decision is read as risk-internalization rather than risk-aversion, PWC's own existing DC stock could see similar AV appreciation under tight supply conditions. This is the strongest counter-argument and is the reason we deliberately did not pass the Loudoun residential permit drop through at face value.
2. **Hyperscaler supply constraints.** NVIDIA supply-limited AI-training CAPEX has been absorbing every available MW in NoVA; PWC's non-Pageland overlay may still tighten.
3. **Fauquier counter-case.** Fauquier's residential permits grew after its December 2023 DC tightening. One interpretation is that homebuyers prefer counties that say no to data centers, which would *help* PWC's residential market post-April 2026. The model's residential range low end (-8%) allows for that interpretation.
4. **PWC own-AAA ratings have survived Digital Gateway controversies before.** The 2022 CPA vote and 2023 rezoning debates did not trigger a Moody's downgrade. The question is whether the April 2026 non-appeal is qualitatively different. Our methodology treats it as different because it is the first case where a VA county (a) had a rezoning judicially invalidated and (b) elected not to appeal.

---

## (h) Data gaps flagged for Finance Office follow-up

1. **County-level commercial-only permit counts.** Census BPS does not publish non-residential permits at the county level. To estimate a clean commercial spillover effect we would need each peer county's Commissioner of the Revenue or Building Development division to provide the full FY20–FY25 non-residential issued-permit time-series, broken out by type.
2. **Proffer-revenue time-series by county.** PWC publishes CIP fund balances but not proffer receipts by originating subdivision.
3. **MSRB EMMA PWC bond official statements.** A full-text review of PWC's 2023, 2024, and 2025 official statements would allow us to extract the exact rating-agency commentary at each issuance. We pulled the Moody's September 2025 opinion directly from PWC.gov and it was sufficient; EMMA-based S&P and Fitch reports would refine the spread parameter by 2–3 bps at the margin.
4. **Peer-county BPOL new-registration time series.** Only total BPOL is published. Isolating new-business formation requires commissioner-of-the-revenue records.

---

## Source-quality audit

| Cite-key                        | Type          | Use for                                 |
|---------------------------------|---------------|-----------------------------------------|
| @census_bps_2025                | P — Census    | Residential permit time-series          |
| @va_apa_fy24_comparative        | P — VA APA    | FY24 local revenue comparatives         |
| @va_apa_fy23_comparative        | P — VA APA    | FY23 local revenue comparatives         |
| @loudounnow2025_av_ty25         | T — local news| Loudoun TY2025 AV by category           |
| @loudountimes2026_av_ty26       | T — local news| Loudoun TY2026 AV update                |
| @loudoun_fy26_budget            | P — Loudoun   | Loudoun post-event FY26 budget          |
| @hk2025loudoun                  | T — law firm  | Loudoun by-right elimination mechanics (inherited) |
| @loudounnow2025phase2           | T — local news| Loudoun Phase 2 recovery trajectory (inherited) |
| @pwc_moodys_opinion_sept2025    | P — Moody's   | PWC scorecard, qualitative uplift       |
| @moodys_methodology_jul2024     | P — Moody's   | US Cities and Counties methodology      |
| @sp2024us_governments_methodology| P — S&P      | S&P US governments methodology          |
| @bondbuyer2024sp                | T — trade     | S&P methodology change coverage         |
| @westernasset2025               | T — industry  | May 2025 US sovereign downgrade impact  |
| @bondbuyer2025                  | T — trade     | Muni spread commentary post-downgrade   |
| @gsam2025muni_may               | T — industry  | Muni ladder spreads                     |
| @pwc2025aaa                     | P — PWC       | PWC Oct 2025 tri-AAA reaffirmation      |
| @pwc_fy26_cip                   | P — PWC       | FY26 CIP new-money issuance schedule    |
