# Stage 4 — Non-Data-Center Revenue Drivers (FY27–FY31)

**Sub-agent:** Stage 4 (research + model).
**As of:** 2026-04-18.
**Audience:** PWC Board of Supervisors → Finance Office.
**Companion artifacts:** `/model/revenue_drivers.py`, `/data/revenue_driver_assumptions.csv`, `/data/non_dc_revenue_projection.csv`, `/citations/stage4.bib`.

This stage models the FY27–FY31 trajectory of every NON-data-center general-fund revenue line under three directional scenarios (low, base, high). Data-center revenue is owned by Stage 6 using Stage 2 (canceled Pageland parcels) and Stage 3 (spillover elasticities); this module carves DC out of the FY26 baseline and projects what remains.

## 1. Scenario design (directional, not symmetric)

| Scenario | Macro frame | Residential price path | Federal workforce | Office absorption |
|---|---|---|---|---|
| base | FY26 PWC Adopted Estimate held | 0%/yr nominal | flat at current -23.5k VA civilian loss | flat |
| low  | Federal contraction persists + housing softens | -2.0%/yr nominal (-10% cumulative) | cumulative -40k VA civilian jobs by FY31 | -3%/yr |
| high | Federal stabilization | +1.5%/yr nominal | recovers to -10k cumulative | +2%/yr |

Scenario cases are documented as named constants in `/data/revenue_driver_assumptions.csv` with source citations. They are **not symmetric around base** — they reflect realistic distributions anchored on published data, following the Stage 4 brief.

## 2. Driver-by-driver methodology and evidence

### 2.1 Residential real estate (≈50% of non-DC real-property tax)

- **Baseline.** FY26 adopted real-estate tax = $1,025.922M (PWC-REV-FY26-30 p.2). Data-center real-property carve-out ≈ $170M (TY2024 audited DC real property was $144.2M per PWC-DCR-TY24 p.23; analyst-projected to $170M in FY26 given continued DC build-out to TY2025). Residential share of the non-DC remainder = 67.7% / (67.7% + 16.5%) ≈ 80% → FY26 residential RE tax ≈ $686M.
- **Price path.** Case-Shiller DC-Washington MSA NSA index peaked June 2022 at 344.2; Dec-2025 reading 339.1 = **-1.5% cumulative** from peak. [@csi_dcxrnsa_2026]. The low case extends the softening to -2.0%/yr (-10% cumulative over 5 yr), which is consistent with the FHFA HPI NoVA CBSA deceleration through 2025 [@fhfa_hpi_2026q1] and with ACS household-formation forecasts under federal-contraction scenarios [@brookings_hamilton_2026]. Base holds nominal flat. High case extends the FHFA CAGR at +1.5%/yr (modest), reflecting "shocks resolved" rather than any boom case.
- **Federal-job pass-through.** Each 10k VA federal-civilian jobs lost passes through to NoVA residential prices at an elasticity of 0.5–2.5% in the low case (Hamilton Project / Brookings 2026Q1 regional housing model [@brookings_hamilton_2026]). At cumulative -40k VA jobs, that's -2.0% to -10% residential price drag on top of the base path. In the module this drag is split evenly across the 5-yr window and added to the price path.
- **Assessment mechanics.** PWC's landbook locks January 1 of the tax year and appears in fiscal-year-N+1 revenue (one-year lag documented in PWC-RE-2025). FY27 revenue reflects the TY2026 landbook, i.e. late-2025 market conditions. The module applies the price change per fiscal year after the lag is already in the FY26 baseline value.
- **New construction.** PWC Community Development: 694 units finished in 2024 (PWC-RE-2025). Base assumes 700/yr; low case 400/yr on demand weakness; high case 900/yr on builder response. Each unit at $570.6k average assessment (PWC-RE-2025).
- **Elasticity cites.** Bartik 2005 and Devereux-Lockwood 2007 bound tax elasticities [@bartik2005; @devereux2007]; they are directly applied only to BPOL/FDI, but the housing pass-through coefficient references the Brookings metro-price sensitivity literature [@brookings_hamilton_2026].

**Result.** Residential RE tax (USD millions):

| FY | low | base | high |
|---|---:|---:|---:|
| 2027 | 662.7 | 688.6 | 702.5 |
| 2028 | 638.3 | 689.0 | 717.0 |
| 2029 | 614.8 | 689.3 | 731.7 |
| 2030 | 592.3 | 689.7 | 746.6 |
| 2031 | 570.7 | 690.1 | 761.7 |

Low-scenario cumulative loss vs. base over FY27–FY31 ≈ $368M in unrecouped residential RE tax. (High-scenario gain vs. base ≈ +$213M.)

### 2.2 Non-DC commercial real estate (Innovation Park, office, industrial)

- **Baseline.** Non-DC commercial share of total AV ≈ 16.5% of $137.6B = $22.7B AV; at $0.906/$100 = $206M FY26 RE tax.
- **Sources on NoVA office vacancy.** JLL 2025Q4 NoVA Office Insight: vacancy ~22.1%, flat-to-down absorption [@jll_nova_2025q4]; Cushman & Wakefield 2026Q1 MarketBeat similarly [@cushman_nova_2026q1]. Stage 4 does not purchase these reports; it uses the published summary figures as cited. **Gap flagged:** absence of parcel-level absorption data within PWC (outside Innovation Park) means the commercial projection is aggregate and should be refined when CoStar Q1-2026 submarket data is accessible.
- **Innovation Park absorption.** 2024 PWC landbook added 836,500 sqft non-DC commercial (PWC-RE-2025 §Commercial). Going forward, base 200k sqft/yr at $250/sqft AV × $0.906/$100 = $0.45M/yr incremental RE tax; low -100k sqft/yr (give-back); high 500k sqft/yr.

**Result.** Non-DC commercial RE tax (USD millions):

| FY | low | base | high |
|---|---:|---:|---:|
| 2027 | 162 | 168 | 172 |
| 2028 | 157 | 168 | 177 |
| 2029 | 152 | 168 | 182 |
| 2030 | 148 | 168 | 187 |
| 2031 | 143 | 168 | 192 |

### 2.3 Federal-contracting exposure (transmission channels)

**Size of the shock.** Stage 3 flagged -23,500 VA federal civilian jobs as of Nov-2025 [@whro2026dogecuts]. The Brookings / Hamilton Project and Richmond Fed regional coverage [@brookings_hamilton_2026; @richmond2023dcfocus] identify NoVA (Arlington + Fairfax + PWC + Loudoun) as absorbing 65%+ of the federal civilian workforce and a large share of federal-services contracting (NAICS 5415 computer-systems design; 5416 mgmt/technical consulting). PWC's share of that NoVA pool is smaller than Fairfax's but material — ~6.5% of VA federal-contractor workforce as a population-weighted estimate [@bls_qcew_va_2025q2]. Average federal-worker total comp in NoVA is ~$140k fully loaded [@bls_qcew_va_2025q2].

**Aggregate PWC income-shock math.** In the low scenario with cumulative -40k VA jobs:
- PWC jobs implicated ≈ 40k × 6.5% = **2,600 PWC-based jobs**.
- Direct PWC income loss ≈ 2,600 × $140k = $364M.
- With a 1.8× IMPLAN-type indirect+induced multiplier (per Mangum 2020 [@mangum2020]), total PWC HH income loss ≈ $655M.
- PWC aggregate HH income ≈ $19.5B (ACS 5-yr median $115k × ~170k households).
- **Total 5-yr HH-income shock ≈ -3.4% in the low case; base -2.0%; high -0.9%.**

**Elasticity transmission to individual revenue lines:**

| Line | Elasticity to PWC HH income (low / base / high) | Source |
|---|---|---|
| Personal property vehicles | 0.9 / 0.7 / 0.5 | Bartik 2005 bound [@bartik2005] |
| Sales tax | 1.1 / 0.9 / 0.7 | CBO 2024 state sales-tax meta [@cbo2024salestax] |
| BPOL (contractor receipts) | 1.2 / 1.0 / 0.8 × 2 (contractor-concentrated) | Analyst synthesis; see §3 |
| Meals tax | 1.3 / 1.0 / 0.7 | Analyst synthesis |
| Housing prices (feeds residential) | 2.5% / 1.0% / 0.5% per 10k jobs lost | Brookings 2026Q1 [@brookings_hamilton_2026] |

**BPOL specifically.** PWC hosts numerous NAICS 5415/5416 federal-services contractors (Innovation Park, Gainesville commercial corridors). BPOL is a gross-receipts tax, so if contractor firms' revenue contracts ~6% in the low scenario, BPOL falls materially more than retail sales would. The module applies a 2× contractor-receipts concentration multiplier to the HH-income shock before the elasticity. Baseline BPOL is already falling ($39.6M FY25 → $37.2M FY26 adopted), so the low case compounds that decline.

### 2.4 State aid (GF direct — not the Schools component-unit line)

- **FY26 adopted GF direct state revenue = $13.095M** (PWC-BUD-FY26-REV p.61; excludes PPTRA and pass-through schools aid).
- **PWCS enrollment.** Fall-2025 enrollment ≈ 91,543, down from ~92,200 peak 2023-24 [@pwcs_enroll_2026]. Base flat; low -0.3%/yr; high +0.3%/yr. Federal-worker outmigration is a mild enrollment risk.
- **SOQ per-pupil.** Virginia 2024–26 biennial budget SOQ per-pupil rose ~3.5%; base extends. Low 2.0% under state fiscal tightening; high 4.5% if JLARC SOQ recommendations fully funded [@va_soq_2026].
- **LCI drift.** PWC Local Composite Index = 0.4193 (2024–26). DC-driven AV inflates PWC's capacity denominator so PWC's LCI has risen relative to peers; continued AV growth raises LCI (worse for state share). Low case +1%/yr drift; base +0.5%/yr; high 0 [@va_lci_2026].
- **Interaction with Stage 5.** Schools component-unit state aid (approximately $700M/yr to PWCPS via SOQ formulas) is logged on the Schools side and enters Stage 5 as a Schools-budget input. The GF direct line modeled here is ~$13M, not material to the county total — included for completeness.

### 2.5 Smaller lines

| Line | FY26 base ($M) | Low 5yr CAGR | Base | High | Driver |
|---|---:|---:|---:|---:|---|
| Consumer utility | 15.5 | -1.0% | +0.5% | +1.0% | Structural decline (distributed gen); cap-limited [PWC-REV-FY26-30 p.21] |
| Communications sales | 11.5 | -5.0% | -3.0% | -1.5% | Cord-cutting ($12.4M FY23 → $11.5M FY26) |
| Motor vehicle license | 13.39 | -0.5% | +1.0% | +2.0% | Fleet growth; FY26 +3% |
| Recordation | 2.80 | -3.0% | +0.5% | +2.5% | Housing turnover + refi |
| Transient occupancy | 2.60 | -1.0% | 0 | +1.5% | Federal-travel sensitivity |
| Cigarette | 3.80 | -5.0% | -3.5% | -2.0% | Structural decline (PWC guidance to $3.0M outyears) |
| Investment income | 29.40 | (rate-path) | (rate-path) | (rate-path) | SOFR glide; see note below |

**Investment income rate-sensitivity — flagged.** The FY26 adopted $29.4M on the $2.2B general pool portfolio implies a general-fund-share yield of ~1.34% after the county's own restricted allocations. The market rate underlying this is ~4.5% (SOFR Dec-2025). If SOFR falls to 3.0% over the 5-yr window (low case / Fed cuts), the GF share compresses ~33%. The FY26 forecast does NOT embed rate-cut risk; Stage 4 flags this. Source: Fed H.15 SOFR projections 2026Q1 [@fed_sofr_2026q1]; PWC portfolio assumption from PWC-REV-FY26-30 p.3.

**Meals tax structural step.** 4% rate was in effect through 2025-12-31; 3% from 2026-01-01 (BOCS action). FY26 is a blended 3.5% year. FY27+ are full 3%. The module rebases FY26 $40.25M from the 3.5% blend to a FY27 3% base = FY26 × (3.0/3.5) ≈ $34.5M, then applies growth + federal exposure.

**PPTRA** is fixed at $54.288M by Va Code 58.1-3524 since 2006; held constant all scenarios. **Federal PILT** ($80k) held flat.

## 3. Aggregated trajectory — total non-DC revenue (USD millions)

| FY | low | base | high |
|---|---:|---:|---:|
| 2027 | 1,366.8 | 1,416.9 | 1,444.6 |
| 2028 | 1,321.9 | 1,420.4 | 1,476.3 |
| 2029 | 1,278.5 | 1,424.0 | 1,508.8 |
| 2030 | 1,236.7 | 1,427.8 | 1,542.0 |
| 2031 | 1,196.3 | 1,431.6 | 1,575.9 |
| 5yr total | 6,400.2 | 7,120.7 | 7,547.6 |
| vs. base ($M) | -720.5 | — | +426.9 |

Note that FY26 non-DC baseline is ≈$1.38B (FY26 adopted $1.733B split base minus ~$350M DC revenue). The base FY27 projection of $1.417B reflects modest growth plus the meals-rate rebase. The base trajectory is roughly flat because the FY26 forecast 5-yr implicit growth is almost entirely **attributed to DC lines that Stage 6 handles separately**, not to non-DC growth.

**Cross-check vs. PWC adopted 5-yr forecast.** PWC-REV-FY26-30 forecasts total general-revenue base growing from $1.733B (FY26) to $2.064B (FY30) — 4.5% annual. Our base-case non-DC trajectory grows about 0.2%/yr. The difference is the implicit DC trajectory that Stage 6 models with spillover scenarios. This split is correct: non-DC lines in PWC are not the growth story; DC is.

## 4. Three biggest negative drivers in the low scenario (low vs. base, 5yr cumulative)

1. **Residential RE tax** — -$368M over FY27–FY31. Driver mix: -2.0%/yr price path plus federal-job housing pass-through. If federal contraction were absent, the residential line would sit much closer to base.
2. **Personal property vehicles** — -$120M. Vehicle rate cut ($3.70→$3.50) is already in FY26 baseline; the low-scenario decline stacks federal income shock (-3.4% HH income with 0.9 elasticity) and low-base growth (-2.5%/yr) on top.
3. **Non-DC commercial RE tax** — -$83M. Office vacancy compounding at -3%/yr plus Innovation Park give-back.

Close behind: **local sales tax** (-$67M, high HH-income elasticity) and **BPOL** (-$19M, contractor concentration effect already on a falling FY25→FY26 trend).

## 5. Surprises for Stage 6 integration

1. **The base non-DC trajectory is near-flat.** FY26 adopted's 4.5% revenue CAGR is almost entirely DC-driven; the residual non-DC base grows approximately 0.2% per year, not 4.5%. When Stage 6 layers CAPEX Spillover onto this, the sensitivity is pronounced because the non-DC baseline does not grow into the DC shortfall.

2. **Residential is the single biggest non-DC swing line.** A 10% residential price drop flows through to ~$70M/yr of RE tax — **roughly 1.5× the entire FY26 BPOL line**. PWC Finance's FY26 forecast does NOT assume negative price growth; the low scenario is materially below PWC's own forward book.

3. **Federal contraction is already in PWC's own narrative.** PWC-REV-FY26-30 p.1 explicitly notes rising UI claims tied to federal-workforce reductions. Stage 4 treats this as confirming evidence that the low scenario is within the plausible range PWC staff themselves acknowledge.

4. **Meals-tax rate cut is a $5.75M structural give-up** (FY26 blended → FY27 full-rate: $40.25M → ~$34.5M). This was a Board policy choice and is baked in; it is not reversible without a new ordinance action.

5. **Investment income faces a hidden rate risk.** $29.4M FY26 was sized during a high-rate environment; a Fed-cutting cycle cuts this line by ~$10M/yr in the low scenario. If Stage 6 uses the FY26 adopted number as the FY27 baseline without an SOFR adjustment, it will materially over-state surplus.

6. **LCI drift is a one-way ratchet.** DC-inflated AV has raised PWC's Local Composite Index, reducing state share of SOQ aid. When DC AV deflates (Stage 6 CAPEX Spillover), LCI should theoretically fall — but the state recalculates on a 2-yr lag, so any reversal enters in FY29+ at the earliest. Stage 5 Schools-budget modeling will inherit this timing.

7. **BPOL has the highest elasticity concentration risk.** Because PWC hosts a meaningful cluster of federal-services contractors, BPOL falls faster than the broader HH-income shock would suggest. The module applies a 2× contractor-concentration multiplier; Stage 6 could tighten this with parcel-level firm data if PWC Finance can supply it.

## 6. Source gaps / unresolved items

- **CoStar NoVA office submarket data** was not accessed; commercial RE projection uses aggregate JLL summary. Recommend Finance Office cross-check with CoStar PWC submarket absorption Q1-2026.
- **BLS QCEW NAICS 5415/5416 for PWC** — the public QCEW tables published through 2025Q2; Stage 4 used the PWC share of VA federal workforce at the population-weighted level. A firm-count-weighted PWC share would be more defensible.
- **ACS worker-by-industry for PWC** — not directly joined; inferred from Census LEHD OnTheMap PWC commuter patterns (~30% of PWC workers commute to federal-heavy Fairfax/Arlington).
- **PWCS enrollment 5-yr projection** — PWCS publishes annual but the forward 5-yr projection was not pulled in this stage; base assumes the published 2025-26 plateau.
- **FHFA HPI NoVA CBSA** — used the 2026Q1 release summary; not joined to a series-level CSV. Recommend Finance Office confirm the HPI series.

All gaps are flagged explicitly in `/data/revenue_driver_assumptions.csv` via source_key columns.
