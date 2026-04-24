# Stage 3 — Spillover Evidence and Elasticities

**Purpose.** Provide the empirical and theoretical basis for quantifying "spillover" from the April 15, 2026 Prince William County (PWC) Board of Supervisors decision not to appeal the March 31, 2026 Virginia Court of Appeals ruling that invalidated the Pageland-area Digital Gateway rezonings. Beyond the directly canceled Pageland projects (Stage 2), we hypothesize two second-order channels the PWC Finance Office must model:

1. **New-CAPEX deterrence** — reduced hyperscaler and colocation CAPEX siting decisions in PWC's Data Center Opportunity Zone Overlay District, because overlay reliability has been credibly challenged.
2. **Accelerated write-down / de-risking** — already-sited or optioned operators accelerate discretionary capital away from PWC (paused expansions, terminated options, land-bank impairment, staggered phase starts delayed) in response to the overlay-reversal precedent.

This document populates CAPEX Spillover in Stage 6. Point estimates and ranges are written in `/data/spillover_parameters.csv`. All citations are in `/citations/stage3.bib`.

**Source-quality labeling (used throughout):**
- **[P]** Primary data / government document (PWC, JLARC, court ruling).
- **[M]** Methodologically transparent consulting report (Mangum, Chmura).
- **[A]** Academic or peer-reviewed source.
- **[T]** Trade / industry press with on-the-record quotes.
- **[V]** Advocacy or activist source (clearly labeled as such).

---

## (a) Fiscal multipliers from data-center investment

### a.1 — Per-MW and per-sqft tax revenue, PWC-specific

PWC's own 2023 Data Center Industry Tax Revenue Report [P: @pwc2024dcreport] is the most authoritative local source. Extracted values:

| Metric (tax year 2023)                         | Value                    |
|------------------------------------------------|--------------------------|
| Total data-center tax revenue                  | **$166.4 M**             |
| ... real property                              | $75.4 M                  |
| ... computer equipment & peripherals           | $66.4 M                  |
| ... furniture & fixtures                       | $23.3 M                  |
| ... fees & licensing                           | $1.3 M                   |
| Turnkey DC buildings                           | 33 parcels / 48 buildings|
| Turnkey MW capacity                            | 622 MW                   |
| Turnkey sqft                                   | 4.75 M sqft              |
| Turnkey assessed value                         | $4.72 B                  |
| Computer-equipment tax rate                    | $2.15 / $100             |
| Furniture & fixtures + real-estate tax rate    | $3.70 / $100 & $0.906/100|
| DC share of commercial assessment growth 2023  | **74%**                  |
| DC share of general revenue (tax year 2023)    | ~10% (of $1.73 B GR)     |

Derived ratios (arithmetic shown):
- **Revenue per operating MW (turnkey basis):** $166.4 M ÷ 622 MW ≈ **$268 K/MW/yr**. This is an upper-bound because the numerator includes some revenue attributable to powered-shell and under-construction facilities' land value, while the denominator only counts turnkey MW. A conservative estimate that credits all revenue against all megawatts (622 turnkey + 400 powered-shell + 357 under-construction = 1,379 MW potential) gives $166.4 M ÷ 1,379 MW ≈ **$121 K/MW/yr** at PWC's current (lower) effective rates.
- **Revenue per sqft (operational):** $166.4 M ÷ 4.75 M sqft ≈ **$35/sqft/yr** for turnkey; roughly $18/sqft including powered-shell + under-construction.

### a.2 — PWC finance's own Digital Gateway estimate

PWC Finance projected the PW Digital Gateway (2,139 acres, 22 M sqft, ~1,700 MW, 37 buildings) at **$24.7 B capital investment** and **$400.5 M annual tax revenue at buildout** [T: @pwt2023dgvote, @potomaclocal2023dgapproved]. Implied ratio: **$400.5 M ÷ 1,700 MW = $235 K/MW/yr**, which falls between the two PWC-derived ratios above and provides the mid-point we adopt below.

### a.3 — Statewide multipliers (for the "bleed-out" check)

Mangum Economics 2020 [M: @mangum2020] and 2024 [M: @nvtc2024mangum] biennial reports:

| Metric                                                        | 2018 (2020 rpt) | 2023 (2024 rpt) |
|---------------------------------------------------------------|-----------------|-----------------|
| VA direct DC operational jobs                                 | 14,644          | 12,140          |
| VA direct construction jobs                                   | n/a in 2018 base| 14,240          |
| Total VA jobs supported (multiplier applied)                  | 45,290          | 78,140          |
| VA state + local tax revenue generated (direct + indirect)    | $600 M          | ~$2.6 B (2022)  |
| Local-govt benefit:cost ratio — Loudoun                       | 15.1:1 (2018)   | 26:1 (2022)     |
| Local-govt benefit:cost ratio — PWC                           | **17.8:1**      | **13:1**        |
| Local-govt benefit:cost ratio — Henrico                       | 8.6:1           | —               |
| Hypothetical residential tax hike absent DC revenue — Loudoun | 21%             | —               |
| Hypothetical residential tax hike absent DC revenue — **PWC** | **7%**          | —               |

JLARC Dec 2024 [P: @jlarc2024dc]: "For the five localities with relatively mature data center markets, data center revenue ranged from less than 1 percent to 31 percent of total local revenue. Loudoun $733M (31%), Prince William $110M (7%)."

**Methodology caveats:**
- Mangum is sponsored by NVTC and data-center operators; methodology is transparent (IMPLAN Pro, standard regional multipliers) but the framing is industry-favorable.
- All IMPLAN-based multipliers assume the counterfactual is no activity at all, not "activity moved across the county line." For regional spillover questions — "would Loudoun or Stafford have captured this CAPEX if PWC said no?" — IMPLAN multipliers over-state *net* state loss.
- PWC's 13:1 benefit:cost ratio (2022 Mangum) is the lowest of the three peer counties in the report; this is because PWC's residential service load grew faster than Loudoun's during the 2018–2022 period. It is still high enough that the *fiscal-solvency* hypothesis does not rest on the multiplier; it rests on the base level of revenue.

---

## (b) Elasticity of new-CAPEX siting to regulatory risk

There is no peer-reviewed micro-elasticity estimate for "CAPEX siting response to overlay-zone reversal" — no published paper has had the natural experiment yet. We therefore synthesize three strands of evidence.

### b.1 — Data Center Watch aggregate (2024–2025)

Data Center Watch [V, quantitatively documented: @dcwatch2025] aggregates local-opposition outcomes nationally:

| Metric                                   | Mar 2025 cut | Dec 2025 cut  |
|------------------------------------------|--------------|---------------|
| Total dollar value "blocked"             | $18 B        | (rolled into) |
| Total dollar value "delayed"             | $46 B        | (rolled into) |
| Total blocked + delayed (combined)       | **$64 B**    | **$152–156 B**|
| Activist groups                          | 142 (24 st.) | ~"hundreds" (42 st.)|
| States with documented opposition        | 28           | 42            |

Two implications for our modeling:

1. The **blocked:delayed ratio ≈ 28:72** (early-2025 read). Roughly three-quarters of opposition-affected CAPEX is *deferred*, not killed outright. Operators resubmit at alternative sites. This is consistent with developer practice of optioning multiple land banks and siting where approvals clear fastest.
2. The **doubling from $64 B → $152 B in nine months** captures accelerating regulatory risk in 2025, the year preceding the PWC ruling. PWC's non-appeal arrives into an already-risk-averse siting environment; the marginal deterrent effect on CAPEX at the *overlay-reliability* margin is therefore higher than in a 2022 baseline.

Data Center Watch is advocacy-adjacent (backed by 10a Labs). Its dollar tallies are built from media, filings, and petitions and tend to be generous in what counts as "delayed" (any project that missed a self-declared milestone). Use the aggregate for *direction and order-of-magnitude*, not for point precision.

### b.2 — Analogous-events stack (catalogued below in §d)

Every neighboring or analog Virginia jurisdiction has tightened in 2024–2025. The conclusion drawn by industry counsel: Virginia is moving toward a regime where *every* data-center siting requires legislative approval, and approvals have become more contested. A PWC overlay reversal places PWC's overlay closer to the regulatory-discretion profile of counties like Fauquier that have historically required case-by-case legislative approval.

### b.3 — Parallels from other large-CAPEX siting literatures

Manufacturing FDI literature [A: @bartik2005; @devereux2007] estimates location-specific tax elasticities of -0.3 to -0.6 for business investment — i.e., a 10% effective-rate increase reduces CAPEX by 3–6%. These are not directly applicable because regulatory-reversal is a step-function shock, not a continuous rate change. But they bound one channel: if the PWC regulatory signal is treated by operators as a ~10% risk-premium on future cash flows, the siting response is on the order of -3% to -6% of marginal new CAPEX in the affected jurisdiction.

For the *step-function* piece we fall back on the analog cases.

### b.4 — Synthesized elasticity parameters (feeding Stage 6 CAPEX Spillover)

Judgment informed by the above, not directly measured:

- **New-overlay CAPEX reduction, year 1 post-ruling:** point 35%, range 20–55%. Rationale: the PWC ruling + non-appeal resembles Warrenton 2023 (where Amazon's site-plan advanced but was bogged in litigation for 3+ years), but is broader (hits 2,139 acres of rezoning simultaneously). Operators who have not yet closed on PWC parcels mostly reprice or exit. Operators with in-construction facilities continue.
- **New-overlay CAPEX reduction, years 2–3:** point 25% and 18% respectively. Rationale: partial recovery as risk premium normalizes or PWC issues clarifying resolutions. This mirrors the Loudoun by-right-elimination trajectory, where applications paused ~6 months then resumed with longer approval cycles [P: @hk2025loudoun; @loudounnow2025phase2].
- **New-overlay CAPEX reduction, years 4–5:** point 10%, range 5–20%. Structural risk premium persists but CAPEX decisions adjusted for it.

---

## (c) Write-down / asset-impairment mechanics and triggers

### c.1 — GAAP framework

Under ASC 360 (long-lived assets) [A: @ey2025impairment] a data-center operator must test for impairment when events indicate carrying value may not be recoverable. A zoning reversal that eliminates the highest-and-best-use of land is a textbook Step-1 trigger:

1. **Recoverability test.** Estimate undiscounted cash flows from the asset's *new* highest-and-best-use. If land was valued at $3.0 M/acre as data-center-ready (per PWC 2023 comps [P: @pwc2024dcreport p.9]) and reverts to residential/agricultural use at ~$0.1–0.3 M/acre, the recoverability test fails.
2. **Impairment measurement.** Write down to fair value (new highest-and-best-use).
3. **Disclosure.** For SEC registrants (Digital Realty, Equinix, Iron Mountain), material impairments are disclosed in 10-K footnotes and MD&A. Private operators (QTS since Blackstone acquisition, Compass, Stack, EdgeConneX, PowerHouse) disclose only in SEC-registered debt issuances and lender covenants.

Digital Realty's 2024 10-K reported a provision for impairment of **$191.2 M** [P: @dlr202410k], illustrating that material impairments are a normal-course event. The specific driver is not broken out by jurisdiction.

### c.2 — Triggers for public disclosure

Public disclosure of a jurisdictional write-off typically requires one of:
- An SEC registrant with a material ($>$ ~1% of total assets) exposure to the affected jurisdiction.
- A lender-covenant breach.
- An activist-investor disclosure demand (rare).

The PWC Pageland exposure is too small relative to any single public operator's balance sheet to force a named disclosure; expect aggregated "land held for development" write-downs in 2026–2027 10-Ks with geographic detail buried or withheld. This matters for the Finance Office because the *absence* of a public write-down headline is not evidence no write-off occurred — it is the default.

### c.3 — Impairment acceleration parameter (feeding Stage 6)

- **Probability of accelerated write-down on already-optioned PWC overlay land within 24 months:** point 40%, range 25–60%. Rationale: options lapse, LLC-held parcels are re-marketed to residential/industrial buyers at a discount, and at least one SEC registrant's 2026 or 2027 10-K records a "Northern Virginia land bank" impairment.
- **Expected assessed-value haircut on 'contingent' overlay parcels (Devlin, northern Digital Gateway, Innovation Park fringe) over 24 months:** point 25%, range 10–45%. This flows straight through to PWC real-estate tax revenue via re-assessment.
- **Construction-pipeline slip (months added to powered-shell → turnkey transition for projects not yet under construction on overlay land):** point 9 months, range 3–18 months. Not a write-down per se, but shifts revenue into later fiscal years — fiscally equivalent to a partial write-down for FY27–FY29.

---

## (d) Analogous-event case studies

### d.1 — Loudoun County, VA — by-right elimination (March 2025)

[P: @hk2025loudoun; @loudounnow2025phase2]. On March 18, 2025 the Loudoun BOS eliminated by-right data-center development in the Industrial Park, General Industry, and Mineral Resources-Heavy Industry zoning districts. All new applications require Special Exception (SPEX). A grandfathering resolution preserves applications accepted before February 12, 2025.

- **What changed:** By-right → discretionary.
- **Industry response:** A pause of roughly 6 months in new applications, then resumption with extended approval timelines. Phase 2 (site-standards) launched September 2025 with a 14-month rollout. Industry counsel at Holland & Knight and McGuireWoods advised clients to revisit all Loudoun land-bank assumptions.
- **Quantitative impact reported:** No county-published dollar figure; sector CRE brokers informally report 12–24 months added to approval cycles.

**Read-across to PWC.** Loudoun's tightening is a *policy* action, debated in public and structured with grandfathering for approved projects. PWC's April 2026 non-appeal is a *judicial* overturn without grandfathering, which removes the contractual-like certainty that operators typically rely on when committing multi-year CAPEX.

### d.2 — Fauquier County — strictest-in-Virginia policy (Dec 2023)

[P: @mcguire2024nvatightening; @pec2024fauquier]. Fauquier adopted a comprehensive-plan policy restricting data-center development to two zoning districts, characterized by industry counsel as "the strictest in Northern Virginia — possibly the state."

- **Industry response:** Projects like the Remington Innovation Campus (SDC Capital, 204 acres, 7 buildings, submitted May 2025) must now seek both a comp-plan amendment and a zoning map amendment — a two-step process that was one step before.
- **Warrenton/Amazon:** Separately, the 42-acre, $40M-land-basis Amazon site in Warrenton has been in litigation for 3+ years; Amazon has not pulled but has not built. This is the closest analog to the PWC "asset stranded by litigation" pattern.

### d.3 — Culpeper County — AWS rezoning litigated (2022–present)

[T: @dcd2022culpepersued; @baxtel2022culpepersued]. Six landowners sued in 2022 to void the 4-3 BOS approval of 243-acre AWS rezoning. As of early 2025 the case is unresolved. AWS has not disclosed an impairment — consistent with §c.2: the project is in litigation, not yet lost, so carrying value remains recoverable.

**Read-across to PWC:** Pageland is the *first case in Virginia* where a rezoning approval was overturned on appeal and the defending county elected not to appeal further. This materially changes the litigation-risk math for operators holding Virginia overlay land.

### d.4 — Fairfax County — zoning ordinance amendment (Sep 2024)

[T: @ffxnow2024ordinance; @venable2024nvatightening; @dcf2024fairfax]. Fairfax BOS adopted 8-2 a data-center ZOA imposing 200-ft residential setbacks, 1-mile Metro setbacks, equipment enclosure, and noise studies. Six pending applications faced redesign or special-exception paths.

- Chair McKay on the vote: "We want to put in place protections for data centers in Fairfax County and not repeat the challenges that have been faced in neighboring Prince William and Loudoun counties."
- **Quantitative:** Fairfax market is ~3M sqft vs. Loudoun 30M+ and PWC 80M+ at buildout; Fairfax tightening has small absolute CAPEX impact but is a bellwether for Northern Virginia regulatory direction.

### d.5 — Stafford County — ZOA with 500-ft setbacks (Oct 2025)

[T: @potomaclocal2025stafford]. Stafford BOS adopted a ZOA on October 21, 2025 including a 500-ft residential setback (up from 100 ft), mandatory tree-preservation, 10-year annual noise evaluations, and backup-generator restrictions. Grandfathering limited to rezonings/CUPs approved on or before Oct 21, 2025.

### d.6 — Warrenton, VA — Amazon litigation (2022–present)

[T: @fauquier2024warrenton; @dcd2023warrenton]. Amazon's 220,000-sqft, $40M-land site has been stuck in litigation since site-plan submittal. Warrenton Town Council members who supported the project were swept out in November 2024.

**Read-across:** Confirms that in Virginia, even a *single* litigated project can hold up $40M+ in capital for 3+ years. A 2,139-acre loss is roughly two orders of magnitude larger in scale.

### d.7 — Prince George's County, MD — permit moratorium (Sep 2025)

[T: @conduitstreet2025pgpause; @marylandmatters2025pg]. Executive Order from County Executive Braveboy on Sep 15, 2025; 180-day Council moratorium on data-center permits; task-force recommendations delivered Nov 30, 2025 including tighter setbacks and an overlay zone for brownfields.

**Read-across:** Maryland parallels Virginia's trajectory 12–18 months later. It signals the region-wide direction of travel.

### d.8 — Cascade Locks, OR — project canceled by recall (2023)

[V: @dcwatch2025]. Roadhouse Digital's $100M Cascade Locks project canceled after voters recalled supporters — the only *completely* canceled analog in the Data Center Watch stack.

**Read-across:** Full cancellation is rare; partial delay is the norm. Supports our blocked:delayed ~25:75 split in §b.1.

### d.9 — HB 1601 veto (May 2025)

[T: @exponent2025dcwatch]. Gov. Youngkin vetoed HB 1601, which would have required applicants to assess "risks to water and agricultural resources, parks, historic sites, and forestlands." The bill was redirected to localities, *increasing* the number of jurisdiction-by-jurisdiction reviews. This is an important regulatory-environment modifier: localism in Virginia's data-center regulation is now structurally stronger.

---

## (e) Parameter recommendations to Stage 6 CAPEX Spillover

All parameters and ranges are re-stated machine-readably in `/data/spillover_parameters.csv`. Key recommendations with arithmetic and source backing:

### e.1 — Direct revenue displaced by Pageland cancellation (Stage 2 owns, restated for continuity)

- **PWC finance's own estimate:** $400.5M/yr at full Pageland buildout [T: @pwt2023dgvote].
- **Our cross-check:** 1,700 MW × $235K/MW/yr = $399.5 M/yr — matches.
- **Phasing:** Buildout was planned 2027–2035; fiscal-impact curve ramps ~$50M (FY28), ~$120M (FY29), ~$210M (FY30), ~$320M (FY31), ~$400M (FY32+). Stage 2 owns this schedule; CAPEX Spillover subtracts it from the Pre-Cancellation Digital Gateway baseline.

### e.2 — New-CAPEX deterrence on remaining overlay (the "spillover" piece)

- **Addressable base:** PWC's non-Pageland overlay and contingent-overlay pipeline. Stage 2 inventory. Our working figure: ~60 M sqft / ~6,000 MW of announced-but-not-yet-rezoned capacity countywide.
- **Year-1 reduction:** 35% (range 20–55%).
- **Year-2 reduction:** 25% (range 15–40%).
- **Year-3 reduction:** 18% (range 10–30%).
- **Year-4 reduction:** 12% (range 5–25%).
- **Year-5 reduction:** 10% (range 5–20%).
- **Revenue impact:** at $235K/MW/yr, a 35% year-1 reduction on ~500 MW/yr pipeline ≈ $41M/yr lost at buildout. Compounded across the 5-year window, undiscounted cumulative lost fiscal-impact ≈ $280M (point estimate); range $150–$450M.
- **Source backing:** §b.4, synthesis of Data Center Watch aggregates and analog-case trajectories. Explicitly labeled *judgment-informed* in the CSV.

### e.3 — Write-down / impairment effect on existing PWC overlay land

- **Probability of impairment disclosure:** 40% (range 25–60%) within 24 months, per §c.3.
- **Assessed-value haircut on contingent parcels:** 25% (range 10–45%).
- **Translation to PWC FY27 real-estate tax:** if ~$1.3 B of currently vacant DC-zoned land (PWC 2023 report, p.9) takes a 25% haircut, at the $0.906/$100 rate the direct PWC real-estate tax hit is about $3.0M/yr. Small in absolute terms, but it is the *leading indicator* that larger future revenue is re-pricing.
- **Construction-pipeline slip:** 9 months (range 3–18). For the powered-shell + under-construction base (~757 MW potential), a 9-month slip defers ~$40M of FY27 computer-equipment revenue into FY28, and so on.

### e.4 — Partial-recovery scenario (Partial Recovery, for contrast)

Partial Recovery assumes PWC reverses course within 1–2 years via a clarifying resolution or settlement. Parameters:
- Year-1 deterrence still 35% (can't un-ring the bell).
- Year-2 deterrence cut in half to 12%.
- Years 3–5 deterrence cut to 5%.
- Write-down probability 15% (cut from 40%).
- Confidence discount on returning CAPEX: 15% (operators still price a risk premium).

### e.5 — Evidence that cuts AGAINST the spillover hypothesis (intellectual honesty)

1. **Loudoun recovered.** By-right elimination in Loudoun (March 2025) produced a ~6-month pause and then resumed application flow. If PWC follows suit, CAPEX Spillover may over-state the decline.
2. **Capacity flight to other VA counties may be partially a *state-level* wash.** If Stafford, King George, or Spotsylvania absorb the displaced CAPEX, state-level GDP is little changed and Virginia politically can afford the tightening. PWC, however, does not capture that spillover — this strengthens the PWC-specific fiscal case.
3. **Hyperscaler demand is price-inelastic in the short run.** NVIDIA supply constraints and AI-training CAPEX cycles mean that the industry's *total* Virginia footprint is power-constrained, not land-constrained. If PWC exits the race, someone else absorbs it — same VA jobs, not same PWC taxes.
4. **PWC's DC tax revenue was already growing 50% YoY.** $110M (2022) → $166M (2023). Even a complete halt in new capacity still lets existing plant throw off computer-equipment revenue for the next refresh cycle (3–5 years), so the *near-term* revenue cliff is smaller than the buildout projection implies.
5. **PWC retains multiple non-Pageland overlay sites.** Devlin Road area, Innovation Park expansions, and the Independent Hill / I-95 corridor remain on-overlay and uncontested. CAPEX Spillover should not model 100% pipeline loss; our 35% year-1 is deliberately well below that.

These five counter-points are exactly why we do not model CAPEX Spillover at the upper bound of our ranges. The Finance Office review should focus on whether our *point estimates* are defensible; the ranges are designed to bracket the counter-case.

---

## Source-quality audit (for Finance Office review)

| Cite-key               | Type          | Sponsor / bias risk                     | Use for                          |
|------------------------|---------------|-----------------------------------------|----------------------------------|
| @pwc2024dcreport       | P — PWC OMB   | None for numbers; county self-report    | All PWC revenue-per-MW math      |
| @jlarc2024dc           | P — VA JLARC  | None                                    | Local-revenue share, VA context  |
| @mangum2020            | M — Mangum    | Sponsored by NVTC + operators           | 2018 baseline multipliers        |
| @nvtc2024mangum        | M — Mangum    | Sponsored by NVTC + operators           | 2023 baseline multipliers        |
| @dcwatch2025           | V — adv-adj.  | Activist-adjacent (10a Labs)            | Order-of-magnitude on opposition |
| @exponent2025dcwatch   | T             | Law-firm client alert                   | HB 1601 veto context             |
| @hk2025loudoun         | T             | Law-firm client alert                   | Loudoun mechanics                |
| @mcguire2024nvatightening | T          | Law-firm client alert                   | Fauquier mechanics               |
| @ffxnow2024ordinance   | T             | Local news                              | Fairfax mechanics                |
| @venable2024nvatightening | T          | Law-firm client alert                   | Comparative NVA context          |
| @potomaclocal2025stafford | T          | Local news                              | Stafford mechanics               |
| @dcd2022culpepersued   | T             | Trade press                             | Culpeper analog                  |
| @dcd2023warrenton      | T             | Trade press                             | Warrenton analog                 |
| @conduitstreet2025pgpause| T           | MD counties assoc.                      | PG County analog                 |
| @marylandmatters2025pg | T             | News                                    | PG County analog                 |
| @potomaclocal2026dgvote| T             | News                                    | The April 15 2026 non-appeal vote|
| @virginiamercury2026dgcourt| T         | News                                    | The March 31 2026 court ruling   |
| @pwt2023dgvote         | T             | Local news                              | Digital Gateway $24.7B / $400.5M |
| @potomaclocal2023dgapproved | T        | Local news                              | Digital Gateway scale            |
| @dlr202410k            | P — SEC       | None                                    | Impairment-mechanics precedent   |
| @ey2025impairment      | A — accting.  | None                                    | ASC 360 framework                |
| @bartik2005            | A             | Peer-reviewed                           | Tax-elasticity literature bound  |
| @devereux2007          | A             | Peer-reviewed                           | Tax-elasticity literature bound  |
| @richmond2023dcfocus   | T — Fed       | None                                    | Contextual statewide data        |
| @whro2026dogecuts      | T             | Investigative journalism                | Federal-contracting context (Stage 4 handoff) |

---

## Handoffs

- **To Stage 2:** request confirmation of Stage 2's Pageland buildout schedule; our §e.1 cross-check ($235K/MW/yr × 1,700 MW = $399.5M) suggests Stage 2 should model $400M annual as the FY32+ steady-state.
- **To Stage 4:** the federal-contracting-contraction evidence [@whro2026dogecuts] informs Stage 4, not Stage 3; we flag -23,500 federal civilian jobs through Nov 2025 as a key input for non-DC revenue modeling.
- **To Stage 6:** all point estimates and ranges in `/data/spillover_parameters.csv` are keyed by `parameter_name` for direct ingest into the CAPEX Spillover model.
