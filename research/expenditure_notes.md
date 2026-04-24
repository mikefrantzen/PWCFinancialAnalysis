# Stage 5 — PWC Committed Expenditure Trajectory FY27–FY31

**Sub-agent:** model (Stage 5).
**As of:** 2026-04-18.
**Audience:** PWC Board of Supervisors → Finance Office.
**Companion artifacts:** `/model/expenditures.py`, `/data/expenditure_assumptions.csv`, `/data/expenditure_path.csv`, `/data/debt_service_schedule.csv`, `/citations/stage5.bib`.
**Raw PDFs:** `/data/raw/pdfs/afy26_*.pdf`; layout-preserving text in `/data/raw/text/afy26_*.txt`.

This stage builds the "committed" side of the five-year model — what the County will owe regardless of the data-center revenue outcome. Stage 6 subtracts Stage 4 + DC revenue from this envelope to compute the gap.

## 1. Scope and structure

"Committed" here means legally required, contractually owed, or approved-in-the-CIP-or-budget. The trajectory does **not** include discretionary initiatives that could still be deferred. Seven blocks:

1. **Schools transfer** — 57.23% of General Revenues under the 2013 PWC-Schools Revenue Sharing Agreement. Implemented as a callable function so Stage 6 can apply it to any scenario's revenue path.
2. **Public safety** — Police, Fire & Rescue, Sheriff, Courts, ADC (GF portion), plus Fire & Rescue Levy (special revenue but operationally contractual once stations are open and CBAs are ratified).
3. **General government + community services** — all remaining departments, grown at a blended operating-inflation rate.
4. **Debt service** — tranche-level schedule from the FY26 Adopted CIP book (existing + approved new issuances FY26–FY31).
5. **Pension (VRS) + OPEB** — employer contributions. Reported as *informational-only* because Salaries & Benefits in the department blocks already include these fringe costs; the pension block surfaces the underlying magnitudes and provides the stress hook for Stage 6.
6. **Operating inflation** — applied to non-personnel, non-debt lines. Documented assumptions with low/base/high.
7. **Capital (PAYGO)** — cash-financed capital from the adopted Five-Year Plan.

Base scenario defaults to the County's Adopted FY26-2030 Five-Year Plan assumptions. Low and High scenarios flex merit-rate, non-personnel inflation, and health-insurance trend — **without** altering the Schools transfer share (contractual).

## 2. Documents relied upon

All cited using `@PWC-*` keys in `citations/stage5.bib`:

- **PWC-BUD-FY26-SUMM** — FY2026 Adopted Budget, Budget Summary section (pp. 34–48 of `afy26_budget_summary.pdf`). Contains the verbatim Adopted FY26-2030 Five-Year Plan table (p. 40, "Five-Year Budget Plan") and the plan assumptions narrative (p. 41).
- **PWC-BUD-FY26-EXP** — FY2026 Adopted Budget, Expenditures section (`afy26_expenditures.pdf`, pp. 64-67). Agency-level FY26 adopted line items by functional area.
- **PWC-BUD-FY26-COMP** — FY2026 Adopted Budget, Compensation section (`afy26_compensation.pdf`, pp. 74–77). Publishes the 5-year cumulative compensation schedule ($311.3M FY26-30) and the detailed step/merit, market, CBA, and insurance assumptions. **Authoritative on the 3% annual merit/step, the 10% annual health/dental trend, the 15.89% VRS employer rate, and the 1.44% supplemental sworn-pension rate.**
- **PWC-BUD-FY26-DEBT** — FY2026 Adopted Budget, Debt Service section (`afy26_debt_service.pdf`, pp. 416–425). Six-year tranche-level funding-source and debt-service tables FY26–FY31 for every existing and approved new issuance.
- **PWC-BUD-FY26-CIP** — Adopted FY2026-2031 Capital Improvement Program (`afy26_cip.pdf`). 15.4MB; pulled and cached but not line-by-line transcribed into this stage (the Debt Service section extracts the bond-service picture we need).
- **PWC-BUD-FY26-REV** — FY2026 Adopted Budget, Revenues section (`afy26_revenues.pdf`). Cross-referenced for the "Total General Revenues" definition.
- **PWC-REV-FY26-30** — Adopted Estimate of General Revenue FY2026-2030 (2025-06-16). Authoritative source for the revenue base subject to the 57.23/42.77 split.
- **PWC-PSFM-24** — Principles of Sound Financial Management, 2024 Update. Cited for Policy V (debt: 10% of revenue, 3% of assessed value) and Section 2.04 (Five-Year-Plan construction with Schools 57.23% requirement).
- **PWC-ACFR-FY25** — FY2025 ACFR. Source for the VRS NPL, OPEB net position, and the -100bp discount-rate sensitivity used in the pension stress section.

## 3. Schools-transfer formula (revenue-linked)

**Formula:** `schools_transfer(revenue_base) = 0.5723 × revenue_base`.
Implemented in `model/expenditures.py::schools_transfer(revenue_base)`. Stage 6 imports this callable.

### Eligible revenue base

The base to which the 57.23% is applied is the **"Total General Revenues"** line in the Adopted Budget revenue book — the same line cited to PWC-BUD-FY26-REV p.63 and PWC-REV-FY26-30 p.2 ($1,732,673,500 FY26 Adopted). Its composition, documented on those pages:

| INCLUDED (general revenue subject to 57.23% split) | FY26 Adopted $ |
|---|---:|
| Real Estate Taxes (net of exonerations & relief; incl. public service corp. and penalties/interest) | $1,025,922,000 |
| Personal Property Taxes (vehicles + business tangible incl. data-center CE&P + prior year + penalties) | $436,245,500 |
| Local Sales Tax | $102,500,000 |
| Food & Beverage (Meals) Tax | $40,250,000 |
| BPOL Tax | $37,167,000 |
| Investment Income (General Fund share) | $29,400,000 |
| Consumer Utility Tax | $15,500,000 |
| Motor Vehicle License | $13,390,000 |
| Communications Sales Tax | $11,500,000 |
| All Other (cigarette, transient occupancy, bank franchise, daily rental, consumption, tax on deeds GF share, PILT, etc.) | $20,799,000 |
| **Total General Revenue (Schools base)** | **$1,732,673,500** |

**EXCLUDED from the 57.23% base:**
- Agency Revenue ($240.3M FY26) — retained by originating agencies.
- PPTRA fixed reimbursement ($54.3M Va. Code § 58.1-3524 — separately accounted).
- Categorical federal and state aid, CSA state pass-through.
- Fire Levy, Stormwater Management Fee, Solid Waste fees.
- Transfers in, use of fund balance, bond proceeds.
- Capital Project / Enterprise / Internal Service fund revenue.

### Contractual floor and durability

The 2013 PWC-Schools Revenue Sharing Agreement (as referenced in PWC-ACFR-FY25 p.9: *"The current Agreement, adopted in 2013, splits the County's General Revenues, 57.23 percent to the School System and 42.77 percent to the County."*) does **not** contain a dollar floor — the protection runs through the share formula alone. PSFM-24 Section 2.04 further obligates the Five-Year Plan to honor the split. Absent a formal Board-to-School-Board renegotiation of the Agreement, the 57.23% share must be funded. This is the single largest expenditure rigidity in the model.

**Stage 6 implication:** every $1 decline in General Revenue translates to a $0.5723 decline in Schools funding. Conversely, the County cannot absorb DC-revenue shocks by reducing only its own operating spending — ~57¢ of every revenue dollar lost flows through to Schools regardless.

### Sanity check

Applying `schools_transfer()` to the published FY26-FY30 General Revenue base:

| FY | GR base | schools_transfer() | Adopted Plan | Match? |
|---|---:|---:|---:|---|
| 2026 | $1,732,673,500 | $991,609,044 | $991,609,044 | exact |
| 2027 | $1,807,905,700 | $1,034,664,432 | $1,034,664,432 | exact |
| 2028 | $1,889,734,014 | $1,081,494,776 | $1,081,494,776 | exact |
| 2029 | $1,974,751,404 | $1,130,150,228 | $1,130,150,228 | exact |
| 2030 | $2,063,873,884 | $1,181,155,024 | $1,181,155,024 | exact |

## 4. Public safety

### FY26 adopted baseline (General Fund)

From PWC-BUD-FY26-EXP pp. 65-66 "Safe & Secure Community" subtotal = **$420,396,976** (FY26 Adopted, GF only):

- Adult Detention Center transfer: $39.16M
- Circuit Court Judges: $2.10M
- Circuit Court Clerk: $7.08M
- Commonwealth's Attorney: $15.06M
- Criminal Justice Services: $8.48M
- Fire & Rescue (GF portion): $147.66M
- General District Court: $2.37M
- J&DR Court: $0.79M
- Magistrates: $0.12M
- Police: $160.67M
- Public Safety Communications: $17.31M
- Sheriff: $19.60M

### Fire & Rescue Levy (special revenue)

FY26 Adopted = **$93,448,379** (PWC-BUD-FY26-EXP p.67). This is a special-revenue fund outside the General Fund but operationally contractual. Three new stations are being built (Stations 27, 29, 30) with fire-levy-supported debt service. I include it in the committed envelope because the stations, once opened, cannot be closed without BOCS action; the CBA with IAFF ratified January 2024 (BOCS Resolution 24-050) locks 30 new F&R FTEs through FY28 to support the 50-hour workweek transition.

### Personnel vs non-personnel split

From the agency pages (sampled):
- Police: personnel $141M of $160.7M total = 88%
- Fire & Rescue: personnel $120M of $147.7M = 81%
- Sheriff: personnel $16.4M of $19.6M = 84%
- Courts (combined): personnel ~55% of total
- **Weighted aggregate: ~75% personnel / 25% non-personnel.**

### Growth assumptions

- **Personnel growth: 4.0% annual (base).** Combines the Adopted Plan's 3.0% step/merit (PWC-BUD-FY26-COMP p.75 "Annual year of service/merit adjustments of 3.0% are included in each remaining year of the Five-Year Plan FY27-30") with ~0.5% market-adjustment drift (ADC and Sheriff market adjustments continuing) and ~0.5% approved-headcount additions (77 SSC FTEs added in FY26 plus the 30 F&R CBA positions phased through FY28).
- **Non-personnel growth: 3.5% annual (base).** Proxy: BLS state-and-local government services price index, 2020-2025 trailing 5-year CAGR of 3.6%. No PWC-specific published figure for non-personnel operating inflation exists; the services index is the closest match for courts, fleet, equipment, and professional-services purchasing patterns.
- **Fire Levy growth: 6.0% annual (base).** Anchored to the FY25→FY26 step-up of 20.67% ($77.4M→$93.4M) reflecting station build-out plus CBA personnel. Six percent is a conservative steady-state rate through FY31 once the three new stations phase in.

Low/high scenarios flex personnel ±1 percentage point and non-personnel ±1-1.5 percentage points.

## 5. General government + community services

FY26 adopted GF baselines from PWC-BUD-FY26-EXP pp. 65-66:

- **GOPI + MEGR (general government):** $120.98M (GOPI: BOCS, County Attorney, Elections, Facilities & Fleet, Exec Mgmt, Finance, HR, Human Rights, IT, OMB, Procurement) + $24.98M (MEGR: Development Services, Economic Dev, Planning, Public Works, Transportation) = **$146.1M**.
- **Non-Departmental:** $48.08M (admin & support, contingency, countywide insurance, unemployment).
- **HWES (community services):** $293.24M (Area Agency on Aging, Housing & Community Dev, Juvenile Court Service Unit, Library, Parks & Rec, Public Health, Social Services, VCE, Community Services, Youth Services).

Growth at **3.5% annual (base)** — blends the Adopted Plan's 3% merit/step with the BLS services-price index. Low scenario uses 2.0% (approximate replication of the County's own operating-line CAGR of 2.17% FY26-30); high uses 5.0% for caseload-driven upside plus tariff-pass-through. The Social Services CSA program grew +33% in FY26 alone (PWC-BUD-FY26-SUMM p.38), suggesting the 2% low case may already be too tight for community-services lines.

## 6. Debt service on approved CIP

### Methodology

The FY26 Adopted CIP Debt Service schedule (PWC-BUD-FY26-DEBT pp. 420-424) is a complete tranche-level table FY26-FY31. The scheduling logic: existing debt amortizes on a declining balance; new CIP issuances layer on top according to the approved issuance schedule (each tranche's first year of debt service is generally the year after issuance).

### Grand totals (principal + interest per fiscal year, County + Schools existing + new CIP + admin)

| FY | County Existing | Schools Existing | New CIP | Admin | **Grand Total** |
|---|---:|---:|---:|---:|---:|
| 2026 | $30.37M | $118.46M | $2.35M | $0.20M | **$151.18M** |
| 2027 | $27.95M | $111.66M | $13.59M | $0.20M | **$153.19M** |
| 2028 | $22.05M | $103.96M | $35.35M | $0.20M | **$161.36M** |
| 2029 | $21.32M | $97.35M | $53.05M | $0.20M | **$171.71M** |
| 2030 | $18.08M | $91.83M | $66.11M | $0.20M | **$176.02M** |
| 2031 | $15.89M | $86.25M | $73.28M | $0.20M | **$175.42M** |

The **existing-debt envelope declines** year over year (pre-FY25 issuances amortize) while the **new-CIP envelope grows sharply** (FY26 $2.4M → FY31 $73.3M, +2,993%) as the approved issuance schedule phases in. The net effect is a total debt-service climb from $151M to $176M — a modest 3.1% CAGR.

### Approved new issuances (FY26-FY31)

From PWC-BUD-FY26-DEBT pp. 418-420:

| Project | Issuance year | Amount |
|---|---:|---:|
| Homeless Navigation Center – East | FY26 | $24.3M |
| Countywide Space | FY26 | TBD |
| Solid Waste Facility Infrastructure | FY26 | $15.7M (enterprise-supported) |
| Fire & Rescue Station 27 | FY27 | $19.9M (fire-levy-supported) |
| Public Safety Training Center Expansion | FY27 | $29.4M |
| Fire & Rescue Station 30 | FY28 | $35.0M (fire-levy-supported) |
| Fire & Rescue Station 3 | FY28 | $30.0M (fire-levy-supported) |
| Juvenile Services Center | FY28 | $27.2M |
| Fire & Rescue Station 29 | FY29 | $30.0M (fire-levy-supported) |
| Homeless Navigation Center – West | Multi-year | TBD |
| Judicial Center Expansion | Multi-year | **$200.0M** |
| Mobility Bond Referendum | Multi-year | **$241.9M** (NVTA 30%-supported) |
| Parks & Rec Bond Referendum | Multi-year | $41.0M |

### Funding offsets

Several tranches have dedicated non-GF funding sources:
- Fire Levy supports all F&R station debt.
- NVTA 30% supports the Mobility Bond Referendum ($22.2M in FY31 alone).
- Recordation Tax supports legacy transportation projects ($0.4–$2.8M/yr).
- Solid Waste enterprise supports the $15.7M Solid Waste Facility.
- Stormwater Management Fee offsets some legacy stormwater debt.
- BAB + QSCB federal reimbursements offset a declining $885K → $37K across FY26-FY31 of Schools debt.

These offsets are itemized in `debt_service_schedule.csv` rows with `issuance_name` prefixed `funding_offset_*` and negative totals. The net GF cost in FY26 is approximately $151M grand total − $4.96M County funding offsets − $0.88M School federal reimbursements = **~$145.4M net GF bite**.

### Debt-capacity stress — which tranches become infeasible?

Using PSFM Policy V 5.02(d): *"Annual net tax supported debt service expenditures shall not exceed 10% of annual revenues."*

At the County's own Adopted GR path, the debt-service-to-GR ratio stays at 8.47%–8.70% across FY27-FY31, well inside the 10% cap. Headroom of $25.8M–$40.3M per year (see `check_debt_capacity()` in the model).

**Stage 6 stress hook:** if DC revenue collapses and the GR base is compressed (CAPEX Spillover), this ratio tightens. The breach point for the published debt-service schedule:

| FY | Debt service | 10% cap requires GR ≥ | Published GR base | Breach if GR falls by |
|---|---:|---:|---:|---:|
| FY27 | $153.2M | $1,531.9M | $1,807.9M | $276.0M (−15.3%) |
| FY28 | $161.4M | $1,613.6M | $1,889.7M | $276.1M (−14.6%) |
| FY29 | $171.7M | $1,717.1M | $1,974.8M | $257.6M (−13.0%) |
| FY30 | $176.0M | $1,760.2M | $2,063.9M | $303.7M (−14.7%) |
| FY31 | $175.4M | $1,754.2M | $2,157.0M | $402.7M (−18.7%) |

FY29 is the tightest year. If the Stage 3 elasticity calibration says CAPEX Spillover compresses GR by more than about 13% in FY29 (an approximately $258M drop, comparable to stripping out roughly the full TY2024 DC total revenue of $293.7M), the County would breach its own debt policy and either (a) cancel planned issuances, (b) raise tax rates to restore GR, or (c) request a PSFM variance.

### CIP issuances at risk under debt-capacity stress

The following FY27-FY29 issuances are most exposed because they layer onto the trajectory right as the ratio tightens:

1. **Judicial Center Expansion ($200M, multi-year).** Debt service reaches $18.0M in FY30 alone. This is the single largest issuance on the schedule and the most political ("BOCS promise"). Under a severe CAPEX Spillover, deferring it to out-years could be the first large lever pulled.
2. **Mobility Bond Referendum ($241.9M, multi-year).** Nominally supported by NVTA 30% revenue, so technically insulated from GR compression — unless a DC-led real-estate contraction also reduces NVTA 30% receipts (which include grantor's tax). The NVTA offset grows from $0.3M (FY27) to $22.2M (FY31), so any NVTA revenue stress materially changes the GF share of this tranche.
3. **Fire & Rescue Stations 27, 29, 30 ($85M total).** Fire-levy-supported, so GR-insulated, but the Fire Levy is ultimately a property-tax levy — a DC-driven assessment haircut flows directly into fire-levy receipts too.
4. **Public Safety Training Center Expansion ($29.4M, FY27).** General fund supported. Lower political exposure than Judicial Center but still deferrable in principle.
5. **Juvenile Services Center ($27.2M, FY28).** GF supported.
6. **Countywide Space ($1.47M FY27 → $10.4M FY31 service; issuance TBD).** GF supported; the fastest-growing service line in the schedule; amount not yet final.
7. **Homeless Navigation Center – West (TBD amount, multi-year).** GF supported.

## 7. Pension (VRS) and OPEB

### VRS County plan

- **Net Pension Liability FY25 (measurement 6/30/2024):** $189.7M at 6.75% discount rate (PWC-ACFR-FY25 p.118).
- **−100bp sensitivity:** $438.8M if discount rate drops to 5.75% — an increase of $249M in the NPL. This is the stress hook for Stage 6.
- **Employer contribution rate FY26:** **15.89%**, held flat FY26-FY30 per PWC-BUD-FY26-COMP p.76 / PWC-BUD-FY26-SUMM p.41 ("Virginia Retirement System (VRS) contribution rate of 15.89% in FY26 is unchanged. The same rates are programmed each year for FY27-30."). The VRS Board sets employer rates biennially; FY27-FY28 rates had not been published as of April 2026, so the adopted rate is used as base.

### Supplemental sworn pension and 401(a)

- **1.44%** sworn supplemental pension (Police, F&R, Sheriff, ADC) held flat FY26-FY30.
- **0.50%** 401(a) Money Purchase Program held flat FY26-FY30.

### Covered payroll proxy

From PWC-BUD-FY26-SUMM p.37, FY26 Adopted General Fund Salaries & Benefits = $617.02M. Fringe benefits are roughly 30-35% of that per compensation-section subtotals, leaving approximately **$460M FY26 covered payroll**. The model applies:

- VRS: 15.89% × $460M × (1 + personnel_growth)^years = $73.1M FY26 scaled forward.
- Supplemental: 1.44% × payroll.
- 401(a): 0.50% × payroll.

### Health, dental, and retiree health credit

- **Health & dental insurance growth: 10.0% annual base** (PWC-BUD-FY26-COMP p.77). Cumulative 5-year cost: $74.36M. This is an exceptionally high trend for the County; AON's 2025 forecast for group employer premiums is roughly 9%, CMS's NHE projection for employer group premiums is roughly 6% (used as low scenario), and adverse medical-trend scenarios push 14% (high scenario).
- **Retiree health credit growth: 5.0% annual** (adopted plan).

### OPEB

- OPEB trust is **overfunded** — $7.9M net asset (primary govt) and $33.7M net asset (component units) as of FY25 ACFR. No contribution drift assumed; scenario flex sits in health/dental premium trend.

### Treatment in the model

The pension_opeb block is reported as `basis='embedded'` to signal that the values are already inside the public_safety/general_government/community_services personnel lines (via Salaries & Benefits). `summarize()` excludes embedded rows from the committed total. The purpose of the separate block is two-fold:

1. Expose the VRS stress hook (−100bp → $249M NPL increase). Stage 6 can flag this as a one-time balance-sheet impact, and it can also use a stressed employer rate (e.g., +200bp on 15.89%) to re-run the model.
2. Give the Finance Office an auditable view of how health-insurance trend alone drives benefit cost from approximately $52M FY26 to **$76.3M FY31** at the adopted 10% trend. At the "high" 14% trend, it reaches **$100M FY31**, a $24M delta that materially changes the CBA budget envelope.

## 8. Operating inflation

CPI-UA and state-and-local-services indices are used as published proxies. No PWC-specific index exists.

| Scenario | CPI proxy | BLS state-local services index |
|---|---:|---:|
| Low | 2.0% | (used as base) |
| Base | 3.0% | 3.6% |
| High | 4.5% | (used as base) |

CBO's February 2025 *Long-Term Budget Outlook* projects 2.4% average CPI-UA over 2026-2030; BLS trailing 12 months (Dec 2024) was 2.9%. The 2025 tariff regime creates upside risk (PWC-REV-FY26-30 p.2 explicitly flags "stagflation scenario could develop"), hence the 4.5% high scenario.

## 9. Capital (PAYGO)

Cash-financed CIP from PWC-BUD-FY26-SUMM p.40:

| FY | County CIP (PAYGO) |
|---|---:|
| 2026 | $33.1M |
| 2027 | $37.0M |
| 2028 | $59.0M |
| 2029 | $86.1M |
| 2030 | $101.6M |

FY31 extrapolated to $115.0M at ~13% growth (trailing 3-year rate was 14-46%; 13% is a conservative continuation).

## 10. FY31 extrapolation (the Adopted Plan stops at FY30)

The County's Adopted Five-Year Plan extends only to FY30. FY31 is extrapolated:

- **Schools transfer FY31:** GR base extrapolated at FY29→FY30 growth (4.51%) → $2,157.0M → Schools share $1,234.5M. (The Adopted GR FY30 was derived assuming the DC pipeline continues; Stage 6 will stress this assumption for Scenarios A/C/D.)
- **Debt service FY31:** taken directly from the FY26 Adopted CIP Debt Service schedule, which extends to FY31 (PWC-BUD-FY26-DEBT p.420).
- **Operating lines:** grown at the scenario operating-growth rate from FY30.
- **CIP PAYGO FY31:** 13% of FY30.

FY31 is **less reliable** than FY27-FY30 and flagged as `basis='extrapolated'` in the output CSV.

## 11. Committed-expenditure trajectory (base scenario)

`python3 model/expenditures.py` produces:

| Block | FY27 ($M) | FY28 ($M) | FY29 ($M) | FY30 ($M) | FY31 ($M) |
|---|---:|---:|---:|---:|---:|
| Schools transfer | 1,034.7 | 1,081.5 | 1,130.2 | 1,181.2 | 1,234.5 |
| Public safety (incl. Fire Levy) | 535.7 | 558.6 | 582.5 | 607.4 | 633.5 |
| General government | 201.0 | 208.0 | 215.3 | 222.8 | 230.6 |
| Community services | 303.5 | 314.1 | 325.1 | 336.5 | 348.3 |
| Debt service (total) | 153.2 | 161.4 | 171.7 | 176.0 | 175.4 |
| Capital PAYGO | 37.0 | 59.0 | 86.1 | 101.6 | 115.0 |
| **TOTAL COMMITTED** | **2,265.1** | **2,382.6** | **2,510.9** | **2,625.6** | **2,737.3** |
| *[info] pension/OPEB (embedded)* | 145.6 | 154.9 | 164.9 | 175.7 | 187.4 |

The total committed envelope grows from $2,265M (FY27) to $2,737M (FY31), a 4.8% CAGR. Schools transfer is 46% of the total and is formula-locked; debt service is another 6-7% and is schedule-locked. Together, roughly half of committed spending is unmovable in a multi-year window.

### Comparison to the County's Adopted Plan

- **Adopted Plan FY27 total GF expenditure (incl. Schools transfer):** $2,048.2M (PWC-BUD-FY26-SUMM p.40).
- **Model FY27 total committed:** $2,265.1M — $217M higher.

The gap arises from three choices:
1. **Fire Levy included** (~$99M in FY27 at the model's 6% growth). The Adopted Plan reports GF-only. Fire Levy is a separate levy but operationally committed once stations are approved; I include it.
2. **3.5% operating growth** (base) vs. Adopted Plan's implied 2.17% operating-line CAGR. This is deliberate: the 2.17% CAGR is not decomposed in the Adopted Plan and doesn't appear to include the full weight of the 10% health-insurance trend. Running the model's "low" scenario with 2.0% operating growth brings the FY27 total to $2,255.1M — still $207M above the Adopted Plan, with the gap fully explained by Fire Levy inclusion.
3. **No budgeted salary lapse.** The Adopted Plan includes −$22.3M of salary lapse (vacancy savings) across agencies. The model does not.

For Stage 6 consistency, the model's base scenario should be read as a **committed-spending ceiling under current policy** rather than a prediction of what the County will actually spend. The Adopted Plan is the County's optimistic expected case; the model is the contractually defended floor.

## 12. Stress hooks for Stage 6

1. **Revenue-linked Schools transfer.** Stage 6 substitutes a scenario-specific GR base and calls `schools_transfer()`. Every dollar of GR lost → 57¢ less to Schools; Stage 6 must then ask whether the County tries to backfill that via rate increases.
2. **Debt-capacity breach check.** `check_debt_capacity()` exposes the per-year headroom vs. the 10% revenue cap. Stage 6 passes stressed GR; breaches flag infeasible issuance tranches.
3. **VRS discount-rate stress.** Apply the −100bp NPL increase of $249M as a one-time balance-sheet shock and/or raise the employer rate 200bp to reflect a stressed contribution policy.
4. **Health-insurance trend stress.** Swap from 10% (base) to 14% (high) to show the $24M FY31 delta.
5. **Fire Levy rate elasticity.** Fire Levy collections scale with assessed value, which is DC-inflated. A 20% DC assessed-value haircut (per Stage 2) reduces fire-levy receipts ~5-8%, and the station CBA ramp continues regardless — so Fire Levy contributions from GF backfill may be needed.

## 13. Caveats

- The Adopted Plan's 2.17% county-operating CAGR is lower than typical NoVA peer budgets (Fairfax 3.5-4%, Loudoun 4-5%). PWC's published number may understate true operating pressure, especially with a 10% health trend baked in. The model's base 3.5% is more consistent with trailing ACFR actuals (FY23 $778.7M → FY25 $898.3M county operating = 7.4% CAGR over two years; pandemic-distorted). Finance Office review is warranted.
- Debt service here is taken at face value from the Adopted CIP. Any re-amortization, refunding, or prepayment would shift the tranches. The $200M Judicial Center and $241.9M Mobility Bond issuance amounts are printed as "Multiple" years in the source; the model accepts the published annual service figures.
- School Board component-unit operating expenditure is NOT in this model. The 57.23% transfer is ~42% of PWCPS revenue; the other ~58% (state SOQ funding + federal grants + non-revenue receipts) sits on the Schools component-unit side. Stage 6 should treat Schools' internal fiscal stress as a separate risk (enrollment × state formula sensitivity; deferred Stage 4).
- The "committed" frame deliberately excludes discretionary initiatives (parks-improvement recurring funding, climate-resilience staffing, noise-ordinance enforcement, etc.). In a severe CAPEX Spillover, the BOCS would cut discretionary before touching committed; Stage 7 should flag where the cuttable margin is.

## 14. Master-agent flags (for Stage 6)

1. **Schools transfer is the dominant rigidity.** It grows $200M over five years (FY26 $992M → FY31 $1,234M at 4.5% CAGR). It is indexed to the revenue base Stage 6 is stressing, so the model self-corrects: in CAPEX Spillover the Schools transfer shrinks in proportion to revenue. Institutional commitments (class-size reduction program, security program, 13th-high-school debt service) imply resistance to proportional reductions, so the political cost of allowing the transfer to contract is non-trivial.
2. **Debt service climbs $25M across the horizon** and the big step-ups are FY28 (+$8M) and FY29 (+$10M) as new CIP issuances start amortizing. Stage 6 should flag FY28-FY29 as the tightest years.
3. **Fire Levy is a sleeper risk.** Under CAPEX Spillover it loses assessed-value denominator *and* has three new stations opening with CBA personnel that cannot be unstaffed without bond-default risk.
4. **Health insurance 10% trend is aggressive** and if CMS's 6% proves more accurate, the County has a ~$24M FY31 benefit-cost upside. Unlike revenue, this is a trend the County can partially manage through plan design.
5. **FY31 extrapolation is the weakest number.** The County's own plan doesn't extend that far. Stage 6 should confidence-weight FY31 accordingly and not treat deltas to FY31 as precisely as earlier years.

No fetched source returned a hard error. The FY26 Adopted CIP PDF is 15.4MB but opens cleanly; the Debt Service section extract used here is the authoritative input.
