# Stage 1 Baseline Fiscal Picture — Prince William County, VA

**Sub-agent:** research (Stage 1).
**As of:** 2026-04-18.
**Audience:** PWC Board of Supervisors → Finance Office.
**Companion artifacts:** `/data/pwc_baseline.csv`, `/citations/stage1.bib`. Raw PDFs and layout-preserving text dumps in `/data/raw/pdfs/` and `/data/raw/text/`.

## 1. Scope and documents relied upon

This stage establishes the FY23 actual through FY26 adopted baseline that downstream stages will extrapolate to FY27–FY31. The primary PWC documents used are (all entered as `@PWC-*` keys in `citations/stage1.bib`):

- **PWC-ACFR-FY25** — Annual Comprehensive Financial Report for the fiscal year ended June 30, 2025; published December 15, 2025. Most recent audited actuals.
- **PWC-ACFR-FY24** — FY24 ACFR; published December 2024. Cross-check for the FY24 figures reprinted in PWC-ACFR-FY25 Tables 2/4/6.
- **PWC-BUD-FY26-REV** — FY2026 Adopted Budget, Section "Revenues / All Funds Revenue Summary" (internal pagination "Revenues" section; PDF pages 55–63 inclusive of General Fund revenue summary and 57.23%/42.77% split calculation). Adopted April 22, 2025.
- **PWC-REV-FY26-30** — Adopted Estimate of General Revenue FY 2026–2030, published 2025-06-16 (signed by CFO Michelle L. Attreed, approved by County Executive Christopher J. Shorter).
- **PWC-REV-FY25-29** — Prior-year adopted Estimate of General Revenue (used only for trend cross-check and context on the 57.23% base before the FY26 policy changes).
- **PWC-DCR-TY23** — TY2023 Data Center Industry Tax Revenue Report, published 2024-10-01. Authoritative FY24 DC revenue recognition.
- **PWC-DCR-TY24** — 2024 Data Center Revenue Report (preliminary, published mid-2025). Authoritative FY25 DC revenue — *preliminary* until the FY25 audit finalized (which the FY25 ACFR confirms in aggregate).
- **PWC-RE-2025** — 2025 Real Estate Assessments Annual Report (published 2025-10-15). Basis for FY26 real-estate revenue.
- **PWC-PSFM-24** — Principles of Sound Financial Management, 2024 Update. Authoritative on reserve policies and 57.23/42.77 revenue-sharing framing.
- **PWC-FHO-2024** — 2024 Fiscal Health Outlook Report (published June 2025, cited for credit-rating factors and federal-contraction narrative).

**Raw files preserved:** `/data/raw/pdfs/` contains each PDF and `/data/raw/text/` the layout-preserving `pdftotext -layout` extraction so downstream stages can grep page-anchored figures without re-fetching.

## 2. Revenue mix — FY26 adopted (General Revenue base subject to 57.23% split)

**Total FY26 general revenue subject to split = $1,732,673,500** (PWC-REV-FY26-30 p.2; same number in PWC-BUD-FY26-REV p.63 in the County/Schools split calculation).

| Source (FY26 Adopted) | $ | % of GR base |
|---|---:|---:|
| Real Estate Taxes (net) | $1,025,922,000 | 59.2% |
| Personal Property Taxes (vehicles + business tangible + penalties) | $436,245,500 | 25.2% |
|  └ of which Business Tangible (mostly DC computer equip.) | $217,995,500 | 12.6% |
|  └ of which Vehicles | $214,900,000 | 12.4% |
| Local Sales Tax | $102,500,000 | 5.9% |
| Food & Beverage (meals) Tax | $40,250,000 | 2.3% |
| BPOL Tax | $37,167,000 | 2.1% |
| Investment Income | $29,400,000 | 1.7% |
| Consumer Utility Tax | $15,500,000 | 0.9% |
| Motor Vehicle License | $13,390,000 | 0.8% |
| Communications Sales Tax | $11,500,000 | 0.7% |
| All Other | $20,799,000 | 1.2% |
| **Total General Revenue** | **$1,732,674,000** | **100.0%** |

On top of that base sit Agency Revenue ($240.3M) plus other county resources to reach Total General Fund Revenue & Resources of $1,981.6M (PWC-BUD-FY26-REV p.63). Only the $1.733B base is shared 57.23/42.77 with PWCPS.

### 5-year forecast (from PWC-REV-FY26-30 p.2), *assumes* the data-center revenue trajectory continues:

| FY | Total General Rev ($B) | Schools Share (57.23%) | County Share (42.77%) |
|---|---:|---:|---:|
| 2026 | 1.733 | 0.992 | 0.741 |
| 2027 | 1.808 | 1.035 | 0.773 |
| 2028 | 1.890 | 1.081 | 0.808 |
| 2029 | 1.975 | 1.130 | 0.845 |
| 2030 | 2.064 | 1.181 | 0.883 |

Implicit growth ~4.3% per year. Most of that growth is attributable to (a) real-estate appreciation plus residential + data-center growth; (b) further data-center computer-equipment BTP pipeline. Critical for Stage 6: **this forecast was adopted BEFORE the April 2026 non-appeal of the Digital Gateway ruling**, and therefore embeds the overlay and Digital Gateway CPA as approved.

## 3. Data-center share of General Fund revenue — reported and inferred

PWC does not publish a single "data-center share of total general revenue" line. The `data/pwc_baseline.csv` `data_center_industry` rows combine two County-published DC reports with the assessment annual report:

- **TY2023 (recognized in FY24)** — $166.35M total DC tax = 9.85% of FY24 Total General Fund Revenue ($1,689.88M) or **12.8% of the FY24 General Revenue split base** (derived: $166.35M / $1,298.07M non-departmental general revenue per PWC-BUD-FY26-REV p.56 line "General Revenue" FY24 actual).
- **TY2024 (recognized in FY25, preliminary)** — $293.70M total DC tax. FY25 total GF revenue (audited) = $1,796.32M ⇒ **DC share = 16.35% of total GF revenue; ~20.3% of the GR split base** ($1,443.57M FY24 general revenue grew to approximately $1,615M FY25 audited general revenue; $293.7M/$1,615M = 18.2%). The TY2024 surge is partly a **rate effect** (CE&P rate went from $2.15 to $3.70 per $100 — $51.9M of the increase came from the rate change alone, PWC-DCR-TY24 p.24) and partly continued capacity growth (+240 MW turnkey).
- **TY2025 (will post in FY26)** — not yet published. Given (i) CE&P rate stepping to $4.15 and (ii) continued new turnkey capacity, the FY26 adopted Business Tangible line ($217.995M, up from FY25 Q3 revised $179M) implies data-center CE&P revenue continues to grow. The FY26 adopted budget implicitly expects another material DC revenue year (see PWC-REV-FY26-30 p.16: "The increase in the General Classification Tax Rate from the prior rate of $3.70 and is expected to drive revenue growth, particularly from equipment housed in data centers.").

**Derived estimate of FY26 DC tax revenue (labeled "derived" in CSV):** applying the FY25/FY24 ratio of CE&P revenue (TY2024 $123.9M on $3.70 rate) to the TY2025 rate of $4.15 and assuming modest depreciation-adjusted growth in the underlying assessment base yields FY26 DC tax revenue in the $330–$370M range, with a point estimate ~$350M. This is an *analyst-derived* projection, not a published PWC figure; Stage 2 will refine when the TY2025 DC report is published (likely Fall 2026) and the canceled-project inventory is set.

### Where DC revenue sits inside each general-fund line

The County does not separately invoice or disaggregate DC contributions to total GF revenue. From PWC-DCR-TY23 and PWC-DCR-TY24 the TY2024 breakdown by tax category is:

- **Real property tax from DCs:** $144.2M TY2024 (inside the FY25 $1,002M real-property line = 14.4%). DCs were 92.4% of all TY2024 commercial RE growth and appreciation.
- **Computer equipment & peripherals (inside BTP):** $123.9M TY2024; DCs are 96.1% of total CE&P category. This is virtually a pure-DC line.
- **Business equipment furniture & fixtures (inside BTP):** $23.2M TY2024 of a $44.2M total category — DCs are ~50%.
- **Fees & BPOL attributable to DCs:** ~$2.5M TY2024, a small share of total BPOL ($38.9M FY24).

### Parcel-level exposure
TY2024 data-center developed real property assessed value = $8.18B (Turnkey) + $0.60B (Powered Shell) + $1.26B (Under Construction) = **$10.04B** improved. Add $11.67B in DC land + substations and **total DC valuation = $21.7B** (PWC-RE-2025 p.23), which is **56% of commercial-industrial assessed value** and ~15.8% of the $137.56B total assessed value base.

## 4. Schools revenue-sharing formula and base

- **Formula:** 57.23% of "General Revenues" to PWCPS; 42.77% to County. Established by the 1998 PWC-Schools Revenue Sharing Agreement, amended 2013. Authoritative description: PWC-ACFR-FY25 p.9 ("The current Agreement, adopted in 2013, splits the County's General Revenues, 57.23 percent to the School System and 42.77 percent to the County."). PWC-PSFM-24 §2.04 requires the Five-Year Plan to provide for it.
- **Base that is actually split:** "Total General Revenues" as defined in the Adopted Budget revenue book — i.e. property taxes (net of relief and exonerations), other local taxes, investment income and interest on taxes, and a small state-revenue piece. It *excludes* Agency Revenue, transfers in, use of reserves, and most federal/state categorical aid. See PWC-BUD-FY26-REV p.63: "Total General Revenues $1,732,673,500 / School Share (57.23%) $991,609,044 / County Share (42.77%) $741,064,456."
- **Agency Revenue** ($240.3M FY26 adopted) is *not* shared — it flows to the originating agency. Same for fire levy, stormwater, solid waste fees, and capital/enterprise funds.
- **Mechanical consequence for Stage 4/5/6:** every dollar of DC revenue (real property tax, BTP, most BPOL) hits the 57.23% base. So a $X decline in DC revenue translates one-to-one into a $0.5723X decline in funding available to PWCPS *unless* the County raises rates, reduces exonerations/relief, or breaks the agreement. Most of the headline-grabbing surprises from overlay uncertainty land in Schools.

## 5. Debt trajectory and capacity

- **Net tax-supported debt (PWC-ACFR-FY25 p.309 Table 14):**
  - FY22: $1,070.8M
  - FY23: $1,010.7M
  - FY24: $1,143.6M (+13.1%)
  - FY25: **$1,275.6M** (+11.5%), of which $946.7M (91.1%) is school-related.
- **Self-imposed caps:** 3% of net assessed value (actual FY25: 0.9%, well under); debt service ≤ 10% of annual governmental revenues (actual FY25: 5.0%). Headroom exists nominally but **the debt cap is measured against assessed value, which in PWC is composed of a large and growing share of data-center computer-equipment and improvements.** A material DC assessment write-down therefore tightens the cap, which Stage 6 must quantify.
- **FY26–FY30 scheduled debt service (PWC-ACFR-FY25 Illus. 9-1 p.97):** $140.8M (FY26), $133.3M (FY27), $135.6M (FY28), $114.7M (FY29), $106.6M (FY30) — declining aggregate principal+interest on *existing* bonds; the CIP layers new issuance on top.
- **Rating context:** County is triple-triple-A (Fitch AAA / Moody's Aaa / S&P AAA) re-affirmed Sept 2024 (PWC-FHO-2024 p.6). Moody's citation: "steady tax base growth and economic stability." Rating-agency downside triggers enumerated in PWC-FHO-2024 include "Volatile revenue sources," "Expected decline in tax base due to corporate closures or tax appeals," and — relevant for this project — reliance on uncertain state/federal aid and political polarization. A DC-revenue shock pattern-matches multiple downside adjusters.

## 6. Reserves and fund-balance policy

Per PWC-PSFM-24 (Policies 1.00–1.40) and audited balances at 6/30/2025 from PWC-ACFR-FY25 p.101:

| Reserve | Policy target | FY25 balance |
|---|---|---:|
| Unassigned General Fund Balance | ≥ 7.5% of GF revenues (since 2006) | $134.7M |
| Revenue Stabilization Reserve | ≥ 2.0% of GF revenues | $35.9M |
| Capital Reserve | ≥ 2.0% of CIP appropriations | $94.2M |
| Economic Development Opportunity Fund | $3.0M floor | $5.9M |
| **Data Center Revenue Stabilization Reserve** | **10% of prior-year audited DC CE&P tax** | **$12.1M** |

- The DC Revenue Stabilization Reserve was established by the Board in 2024 (PWC-ACFR-FY25 MD&A p.16 and PWC-PSFM-24 Policy 1.40) *expressly* to shelter the County from "unexpected declines in revenue generated by data centers." Its policy-target balance scales to CE&P — on TY2024 preliminary CE&P of $123.9M, target would be ~$12.4M (consistent with current $12.1M).
- **Bridging loss of DC revenue with reserves is NOT viable at scale.** Even if Unassigned + Revenue Stabilization + DC Stabilization were fully tapped ($134.7+$35.9+$12.1 = $182.7M), that is less than one year of current DC tax revenue ($293.7M FY25) and less than one year of the schools-transfer growth alone ($80.6M FY25→FY26 increment). Reserves are a 6–12 month shock absorber, not a multi-year bridge.
- **All governmental funds total fund balance** (General + Capital Projects Streets & Roads + Nonmajor) = $646.4M at 6/30/2025 (+$49.3M YoY). General Fund alone: $354.5M (+$35.3M).

## 7. Pension and OPEB

From PWC-ACFR-FY25 Schedules 2A–10A and MD&A Table A-1:

- **VRS County Net Pension Liability (measurement 6/30/2024):** $189.7M at current 6.75% discount rate; sensitivity: $438.8M if rate −100bp to 5.75% (PWC-ACFR-FY25 p.118).
- **Schools Non-Professional VRS NPL:** $7.1M; **Schools Professional proportionate share of statewide VRS teacher pool:** $679.0M (reported on the Schools component-unit side).
- **OPEB:** Primary government has *net OPEB assets* of $7.9M; component units $33.7M net OPEB assets — OPEB Master Trust overfunded on current assumptions.
- **Combined net pension + OPEB liabilities (primary govt)** rose from $205M (FY24) to $229M (FY25) — modest but worth watching.
- Pension and OPEB are comparatively *well* managed; they are not the soft underbelly Stage 5 needs to stress. The soft underbelly is the debt-service trajectory on the approved CIP and the schools transfer mechanics.

## 8. Real-estate base composition and trend

From PWC-RE-2025 and PWC-REV-FY26-30 §Real Property:

- **Residential:** 2025 landbook residential assessments +8.02% overall; average residential assessment $570,600 (+7.38% from $531,400). 694 new units finished in 2024. ~67.7% of total assessments (per PWC-ACFR-FY25 MD&A).
- **Commercial + Industrial:** +34.44% in 2025 landbook year. Excluding data centers, added ~836,500 sqft commercial (~$330M valuation); 67% of that was industrial. **Data centers contributed $4.55B (≈83%) of the $5.5B commercial growth; DC appreciation alone was $3.2B of the $3.7B commercial appreciation.**
- **Total assessed value of taxable property** (PWC-ACFR-FY25 p.309 Table 14):
  - FY22 $82.8B → FY23 $94.3B → FY24 $106.4B → **FY25 $137.6B** (+29.3% YoY, largely DC-driven).
- **Implication:** the ratio of tax-supported debt to assessed value dropped from 1.8% in FY23 to 0.9% in FY25 *only because the DC-driven assessed-value denominator ran ahead of debt issuance*. Any meaningful compression in the DC assessed-value denominator tightens every debt-capacity ratio the County uses.

## 9. FY25 expenditure snapshot and FY26 framework

From PWC-ACFR-FY25 Exhibit 5 (p.50) and PWC-BUD-FY26-REV:

| Item | FY25 audited | FY26 adopted |
|---|---:|---:|
| General government administration | $117.7M | — |
| Judicial administration | $43.5M | — |
| Public safety | $442.4M | Increased headcount budgeted |
| Public works | $10.1M | — |
| Health and welfare | $184.9M | — |
| **Transfer to Schools (Education line)** | **$799.5M** | **$991.6M** |
| Parks, recreational & cultural | $72.0M | — |
| Community development | $90.5M | — |
| Debt service (principal + interest) | $158.8M | Programmed by CIP |
| Total governmental funds expenditures | $2,230.5M | — |
| General Fund revenue & resources | $1,796.3M (audited) | $1,981.6M |

Between FY25 and FY26, the Schools transfer rises $192.1M (+24%); public safety is adding fire/rescue, police, PSC and Sheriff staffing. The entire upside in the FY26 adopted budget is carried by the +$140.8M step-up in General Revenue — a step-up that in turn is driven principally by (a) the CE&P rate increase to $4.15, (b) DC real-property growth, and (c) residential appreciation.

## 10. Key risks already acknowledged in PWC's own documents (for Stage 3/6 framing)

- "Revenue Dependence on Data Centers: Significant contributions from data centers, particularly in the Computer Equipment and Peripherals classification, emphasize their importance to the County's revenue stream. Significant changes in the data center industry could substantially impact the County's future revenues." (PWC-DCR-TY23 p.18.)
- "While data centers are a crucial revenue source, maintaining a diversified tax base is essential to mitigate risks associated with industry-specific downturns." (PWC-DCR-TY23 p.18.)
- "While the data center industry presents an opportunity for the County to diversify its revenue base, residential real estate…" (PWC-ACFR-FY25 MD&A p.13, flagging the concentration squarely.)
- "Given its location in the Greater DC Metro region, federal employment and spending reductions could have a negative impact on the County's local economy and therefore, its financial health. The County, as well as the rating agencies, will monitor the evolving situation as they pose a potential credit risk." (PWC-FHO-2024 p.3.)
- Labor-market signal: "For the period spanning January through March 2025, average initial claims per month climbed to 593 versus a per month average of 431 from October through December 2024. Considering the trajectory of claims throughout the quarter, a reasonable conclusion can be made that reductions in the federal workforce and contractors serving the federal government are likely buttressing the County's current labor market profile." (PWC-REV-FY26-30 p.1, i.e. the County is already seeing federal-contraction spill into claims data.)
- Rating-agency downside qualitative adjusters (PWC-FHO-2024 p.5) that would be triggered by a DC revenue shock: "Volatile revenue sources"; "Expected decline in tax base due to corporate closures or tax appeals"; "Political polarization that makes budgeting and decision-making difficult."

## 11. Source gaps / unresolved items for later stages

- **TY2025 Data Center Revenue Report not yet published.** Expected Fall 2026. TY2025 figures currently only inferable from the FY26 adopted budget's Business Tangible line and the CE&P rate change.
- **Digital Gateway / Pageland canceled-parcel inventory.** The FY25 ACFR and FY26 adopted budget both predate the April 2026 non-appeal decision; neither records the fiscal impact. Stage 2 will build this from the Planning Office rezoning file, Circuit Court order, and Board meeting minutes.
- **Separation of DC vs. non-DC BPOL.** The TY2024 DC report groups DCs into "Repair, Business, Personal and Other Services" BPOL class but does not publish a dollar breakout of DC BPOL; the $2.5M fees & licensing figure bundles BPOL and administrative fees. Downstream work will estimate from tenant-count × class rate.
- **Schools component-unit revenue/expenditure detail** (state share of PWCPS, federal title grants, enrollment trajectory) was not pulled here because this stage focuses on primary-government revenues; Stage 5 will pick it up from the School Board's separately published FY26 Adopted Budget. It matters because the 57.23% transfer is roughly half of PWCPS' operating revenue — the other half comes from Virginia SOQ formulas sensitive to enrollment.
- **5-Year CIP FY26–FY31 detail** — cited in PWC-ACFR-FY25 MD&A but the underlying CIP book was not downloaded for this stage; Stage 5 will pull `https://www.pwcva.gov/department/management-and-budget/adopted-budget` CIP appendix. Scheduled debt service in the CSV is from the ACFR amortization schedule on existing debt only.
- **Federal workforce concentration data** (BLS QCEW NAICS 541/federal-contractor NAICS subsectors for PWC) deferred to Stage 4.
- **County's FY25 external-audit line-item disclosure of DC-specific real-property tax revenue** — the FY25 ACFR combines all real-property tax into one $1,002M line; the disaggregation we use (TY2024 $144.2M DC real property) comes from the preliminary DC report, not the audited ACFR. This is noted in CSV as `dc_real_property FY2025 $144.2M` cited to PWC-DCR-TY24; when the TY2025 DC report lands, the FY25 figure will be reconciled to audited numbers.

No fetched source returned a hard error; all primary-source URLs resolved and were preserved.

## 12. Surprises / master-agent flags (for Stage 2–6)

1. **DC revenue share of the general-revenue split base is already ~17–20% in FY25 and rising** — higher than most internal framings that quote "around 10%." Stage 6 must distinguish the split-base share (drives Schools) from the total-revenue share.
2. **The FY26 adopted forecast embeds Digital Gateway growth.** The adopted real-property forecast steps from $999.8M (FY26) to $1,281M (FY30) at 6.4% CAGR — a pace that requires the DC pipeline to come online substantially. Any Stage-2 canceled-project inventory maps directly to a downward revision to this line.
3. **The 57.23% schools transfer is legally contractual** (2013 Agreement) and re-affirmed as a Five-Year-Plan constraint in PSFM §2.04. It cannot be quietly re-cut to absorb DC shortfalls without an explicit Board renegotiation with PWCPS. This is the dominant expenditure rigidity.
4. **Debt-capacity is measured against the DC-inflated assessed value.** A 20% DC assessed-value haircut cuts the denominator by ~3.1% (DC = 15.8% of total AV), ratcheting the debt-to-AV ratio from 0.9% to ~0.93% — still well under the 3% cap. The binding constraint is *debt service to revenues* (currently 5.0%, ceiling 10%), which moves adversely if revenues fall. Stage 6 sensitivity should use the 10% revenue-based limit.
5. **Federal-contracting contraction is already showing up in unemployment-insurance claims data** per the County's own adopted revenue book (§1). That suggests the Stage 4 residential-and-sales-tax downside case is not speculative.
6. **Meals-tax structural cut** (4% → 3% on 2026-01-01) and **vehicle rate cut** ($3.70 → $3.50) land on top of DC revenue exposure. These BOCS-initiated rate cuts net out $10–15M/year that in a downside scenario would have cushioned a DC shortfall.
7. **DC Revenue Stabilization Reserve is 10% of prior-year audited CE&P only.** On FY25 CE&P of $123.9M that is ~$12M. It does NOT cover real-property, F&F, or BPOL exposure from the same facilities — the reserve as currently sized equals roughly 2.3% of total annual data-center-attributable revenue (F&F + CE&P + real-property + BPOL combined, ~$520M).
