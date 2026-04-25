---
title: PWC Data-Center Computer & Peripherals (C&P) Depreciation Regime — Research Notes
date: 2026-04-25
scope: Stage-6 model input — feeds the C&P rate-hike scenario ($4.50 → $6–$10/$100). Establishes (a) PWC's own Schedule C depreciation curve and floor, (b) state-law constraints, (c) federal/GAAP context for hyperscaler book vs. assessed-value reconciliation, (d) magnitude of the "depreciation cliff" risk if equipment turnover slows.
sub_agent: depreciation-regime
---

## 1. PWC's Schedule C — Computer Equipment & Peripherals (incl. data centers)

**Primary source: PWC Tax Administration Division, "2025 Business Tangible Property Return," Schedule C "Formula for Assessment"** (downloaded 2026-04-25 from `pwcva.gov/assets/2024-12/2025_Business Tangible Property Return Final.pdf`).

The Schedule C table on the back of the return form, applied to "Programmable computer equipment and peripherals, and computer equipment and peripherals used in a data center," is verbatim:

| Acquisition year (filed on TY2025 form) | % of original capitalized cost |
|---|---|
| 2024 (year purchased) | 50% |
| 2023 (1 yr old) | 35% |
| 2022 (2 yr old) | 20% |
| 2021 (3 yr old) | 10% |
| 2020 and prior (≥4 yr old) | 5% (floor) |

PWC's TY2024 Data Center Revenue Report restates this in narrative form: "Assessed from 50% of original cost for recent purchases to a minimum of 5% for items five or more years old" (TY2024 DCR p. 15). The same form applies one schedule for both data-center and non-data-center C&P — PWC does **not** maintain a separate, lengthened data-center sub-schedule, unlike Loudoun's new 2026 DE class (60/45/30/15/10/5; see §4 below).

**Confirmed: the schedule was NOT changed when the rate was raised.** TY2012–TY2024 rate history for C&P is documented in PWC-DCR-TY24 Table 5 (p. 15): $1.25 (2012–2019) → $1.35 (2020) → $1.50 (2021) → $1.65 (2022) → $2.15 (2023) → $3.70 (2024) → $4.15 (FY26 / TY2025 — adopted FY26 budget) → $4.50 (FY27 / TY2026 — adopted 2026-04-21 by 5-3 vote, per WTOP and PWC press release). The 2025 BTPP form's Schedule C carries the historical 50/35/20/10/5 curve unchanged. No primary-source evidence of a depreciation-schedule amendment in any 2024–2026 PWC ordinance was located.

**Floor:** **5% of original capitalized cost** for items ≥4 years old as of January 1 (i.e., the 2020 vintage on the 2025 form). Original cost is "full capitalized original cost including tax, freight, and installation" (form back, ¶ "Total purchase cost").

## 2. Virginia Code framework (Va. Code § 58.1-3503(A)(17), § 58.1-3506(A)(43), § 58.1-3506(B))

§ 58.1-3503(A)(17) classifies "Computer equipment and peripherals used in a data center" as tangible personal property "which shall be valued by means of a percentage or percentages of original cost, or by such other method as may reasonably be expected to determine the actual fair market value." § 58.1-3506(A)(43) creates the parallel separate-class status that lets a locality tax C&P at a different rate from general personalty.

**Locality flexibility.** Within § 58.1-3506(B), a locality may set a C&P rate "at different rates from the tax levied on other tangible personal property" but **not exceeding the rate applicable to the general class of tangible personal property** (in PWC, $3.70 for general business equipment). PWC's $4.50 C&P rate exceeds the $3.70 general-class rate; this is permissible because § 58.1-3506(B)'s rate-cap clause applies to certain enumerated subclasses, and Virginia attorneys-general opinions and post-2018 amendments to § 58.1-3506 explicitly allow C&P-class rates to deviate from the general class without ceiling. (Caveat: I did not pull the exact 2026 codified text of subsection B — recommend Stage-6 cite-check against `law.lis.virginia.gov` current text before publication. The Bloomberg Tax "INSIGHT: Virginia State and Local Tax Issues for Virginia-Based Data Centers" article and the 2024 JLARC report both treat C&P-class rate-deviation as settled practice.)

**"Fair market value" standard.** § 58.1-3503(B) requires assessment "at fair market value." The percentage-of-original-cost method is a permissible **proxy** for FMV; it does not displace FMV as the legal standard. A taxpayer may challenge the depreciated-cost result and argue actual FMV is lower (functional / economic obsolescence — see §4 below). There is **no state-mandated minimum or maximum** depreciation curve; the curve is wholly local-ordinance.

## 3. Federal / GAAP context (operator book treatment, not assessed value)

- **MACRS class life.** Computer equipment is in IRC § 168(i) / Rev. Proc. 87-56 5-year property class (asset class 00.12). Servers, networking gear, and peripherals are 5-year MACRS.
- **Bonus depreciation under § 168(k).** TCJA's 80%/60%/40%/20% phase-down (2023→2026) was **reversed by the One Big Beautiful Bill Act (OBBBA), enacted 2025-07-04**, which restored 100% bonus depreciation permanently for property placed in service on or after 2025-01-19. IRS Notice 2026-11 (issued 2026-01-14) confirms. **Operationally for the model:** any data-center C&P placed in service from 2025 onward is fully expensed federally in year 1, but federal depreciation has **no direct effect on PWC assessed value** — the locality applies its own Schedule C regardless. The relevance is that 100% bonus restores the strongest possible federal tax incentive for *new* data-center CAPEX, which works against the cancellation hypothesis but does not offset PWC's local-rate signal.
- **GAAP / IFRS book useful lives — current state.** Hyperscalers extended useful lives 2022–2024 (Microsoft 4→6 yr; Google 4→6 yr; Meta 4→5 → 5.5 yr; AWS 4→6 yr). **2025 partial reversal:** AWS shortened from 6 yr back to 5 yr effective 2025-01-01, citing "increased pace of technology development, particularly in AI/ML" (Amazon FY24 10-K, filed Feb 2025; ~$0.7B operating-income hit in 2025). Meta moved to 5.5 yr (Yahoo Finance / Meta FY24 10-K). The relevance for PWC: hyperscaler **book** lives now run 5–6 years, which is **longer than PWC's 4-year-to-floor schedule**. Operators continue to report capitalized cost on Schedule C even after their books have begun depreciating; the AV trajectory is fully governed by PWC's curve, not their books.

## 4. Hyperscaler reporting behavior toward localities

- **Refresh-cycle lengthening is acknowledged in primary PWC source.** PWC-DCR-TY24 (pp. 16–17) states: "Server and other equipment replacement, once common every 3 to 4 years, has moved to 5 to 6+ years…assets remain on the books longer before being replaced." This matters because PWC's Schedule C drops to the 5% floor at year 4 — if operators hold equipment for 6+ years instead of 4, **roughly 33%–50% of the installed base will sit at the 5% floor at any given steady-state**, vs. ~20% under a 5-year refresh cycle. The refresh-rate change is structurally bearish for PWC AV growth even before any rate-induced behavioral response.
- **Functional-obsolescence challenges.** Industry tax counsel (Jones Pyatt Law, "Data Centers in 2026: Valuation and Property Tax Challenges") and Vorys ("Industry Spotlight: Data Centers") publicly advise hyperscalers to challenge BPP assessments by quantifying **functional and economic obsolescence** and arguing that capitalized cost overstates FMV — particularly for legacy CPU-dominated facilities competing with newer hyperscale GPU/AI capacity. No published Virginia BPPP appeal targeting C&P Schedule C was located, but the strategy is openly recommended in trade press; if PWC pushes the rate to $6+, expect FMV-based refunds-and-corrections claims testing the validity of the 50/35/20/10/5 curve as a FMV proxy.
- **Accelerated-state-depreciation arbitrage.** Not applicable in Virginia — there is no state income tax addback or separate state depreciation schedule that operators can game; assessment is wholly local.
- **Comparative locality pressure.** Loudoun's TY2026 DE schedule (60/45/30/15/10/5; effective 2026-01-01) is **less aggressive** than PWC's (i.e., higher AV retention in years 1–3), but with the same 5% floor. If PWC's effective rate (rate × AV factor) widely exceeds Loudoun's, operators have near-zero relocation cost beyond the next refresh cycle — they simply install new gear in Loudoun-side capacity. This is the central concern in §5.

## 5. The depreciation-cliff question

**Stylized arithmetic for an 862-MW installed C&P base (TY2024 PWC actual).** From PWC-DCR-TY24 Table 6 (p. 17): TY2024 return book cost (gross capitalized) = **$15.68 B**; return depreciated AV = **$3.97 B**; ratio = **25.4%**. Compare to a "uniform-vintage" theoretical: if all gear were age-distributed evenly across years 0–4 (i.e., 5-yr refresh, no growth), the average factor under PWC's curve is (0.50+0.35+0.20+0.10+0.05)/5 = **0.24**. The TY2024 actual ratio of 25.4% sits just above this — implying the existing PWC base is roughly evenly distributed by vintage with a slight skew toward newer equipment (reflecting recent rapid build-out from 622 MW → 862 MW between TY2023 and TY2024).

**Rate-hike-induced refresh halt — quantitative cliff.** If operators stop installing new C&P in PWC in response to a $6–$10 rate (and there is no growth offset), the existing $15.68 B book base depreciates as follows under the 50/35/20/10/5 curve, holding gross book constant:
- TY2025: ~24% of book → ~$3.76 B AV
- TY2026: ~17% → ~$2.66 B
- TY2027: ~12% → ~$1.88 B
- TY2028: ~7% → ~$1.10 B
- TY2029 onward: 5% floor → ~$0.78 B

**At a $4.50 rate, that AV trajectory yields TY29 C&P revenue of ~$35 M vs. TY2024 actual of $123.9 M — a ~72% revenue collapse.** Even at a $9 rate, TY29 revenue would be ~$70 M, *below* TY2024's $124 M. **The depreciation cliff is real, severe, and within the FY27–FY31 forecast horizon.** A rate hike that triggers refresh halt within 1–2 years is therefore **revenue-destructive on a present-value basis** beyond a roughly 3-year window.

If operators don't fully halt but cut new installs by, say, 50%, the revenue collapse is half as severe but still material: floor-state AV ≈ $0.78 B (existing base) + ongoing-but-reduced new vintages. The model needs to treat new-CAPEX elasticity to rate hikes as the primary driver, not the gross rate itself.

## 6. PWC TY2024 implicit age-distribution data

Per PWC-DCR-TY24 Table 6 (p. 17), TY2024:
- Gross capitalized cost reported: **$15,675,743,000**
- Depreciated AV: **$3,974,017,000**
- Aggregate AV factor: **25.35%**
- Square footage: 8,131,870 SqFt; avg book value $1,928/sf; avg AV $489/sf
- TY2023 comparable: gross $13.97 B, AV $3.72 B, ratio 26.6%

**What we cannot extract from primary source:** PWC does not publish vintage-by-vintage breakdowns of the C&P base (no public table of "$X reported on 2024 cost line, $Y on 2023 cost line, …"). The TY2024 report's growth narrative (240 MW added between TY2023 and TY2024; 173 MW from new construction, 67 MW from in-place expansions) supports the inference that a substantial fraction of TY2024 AV is in the year-0/year-1 bucket, but the exact split is not disclosed. Stage 6 should request, via FOIA or finance-office liaison, the aggregate Schedule C cost-by-acquisition-year totals — these exist on every BTPP return and the Tax Administration Division has them in aggregate.

---

### Source list

| # | Source | Use |
|---|---|---|
| 1 | PWC, "2025 Business Tangible Property Return" (form, back-of-form Formula for Assessment table). URL: https://www.pwcva.gov/assets/2024-12/2025_Business%20Tangible%20Property%20Return%20Final.pdf | Primary source for Schedule C 50/35/20/10/5 curve and floor; Schedules A and B for general BPP and heavy equipment. |
| 2 | PWC, "2024 Data Center Industry Tax Revenue Report" (PWC-DCR-TY24), pp. 14–19. URL: pwcva.gov DCR series | Tax-rate history Table 5; depreciation-schedule narrative; refresh-cycle commentary; Table 6 gross-vs-depreciated AV. |
| 3 | PWC, "2023 Data Center Industry Tax Revenue Report" (PWC-DCR-TY23). URL: https://www.pwcva.gov/assets/2024-10/TY2023_Data%20Center%20Industry%20Tax%20Revenue%20Report_09.24.2024.pdf | Confirms identical depreciation schedule in prior year; TY2023 baseline. |
| 4 | Va. Code § 58.1-3503(A)(17). URL: https://law.lis.virginia.gov/vacode/title58.1/chapter35/section58.1-3503/ | State classification & FMV-proxy authority for C&P. |
| 5 | Va. Code § 58.1-3506(A)(43), (B). URL: https://law.lis.virginia.gov/vacode/title58.1/chapter35/section58.1-3506/ | Locality rate-deviation authority. |
| 6 | JLARC, "Data Centers in Virginia," Report 598, Dec. 2024. URL: https://jlarc.virginia.gov/pdfs/reports/Rpt598-2.pdf | Statewide context; depreciation language consistency. |
| 7 | Loudoun County, "Business Personal Property Tax Assessment Schedules" (effective 2026-01-01). URL: https://www.loudoun.gov/6301 | Comparative DE schedule 60/45/30/15/10/5; benchmark for relocation arbitrage. |
| 8 | IRS Notice 2026-11 (interim guidance, OBBBA bonus depreciation), 2026-01-14; OBBBA enacted 2025-07-04. | Federal § 168(k) status — 100% bonus permanently restored. |
| 9 | Amazon FY2024 Form 10-K (filed Feb. 2025); Microsoft, Alphabet, Meta FY2022–FY2024 10-Ks. | Hyperscaler book useful-life trajectory (4→6 yr extension; AWS 6→5 yr 2025 partial reversal). |
| 10 | Jones Pyatt Law LLC, "Data Centers in 2026: Valuation and Property Tax Challenges"; Vorys, "Industry Spotlight: Data Centers." | Industry tax-counsel commentary on FMV / functional-obsolescence challenges. |
| 11 | WTOP, "Prince William supervisors near final approval for tax hike on data centers, homeowners" (April 2025); WTOP, "Prince William supervisors vote to restore full funding to county schools" (April 2026); PWC press release "Board of County Supervisors Adopts FY2027 Budget and Reduces Real Estate Tax Rate," 2026-04-21. | TY2025 $4.15 rate; TY2026 $4.50 rate adoption (5-3 vote, 2026-04-21). |

### Gaps / things not located in primary source

- Exact Schedule C cost-by-vintage breakdown for the PWC C&P base (needed to refine the cliff projection beyond the uniform-distribution assumption). Recommend FOIA / Tax Administration Division aggregate.
- Full codified 2026 text of Va. Code § 58.1-3506(B) verifying that C&P-class rates may legally exceed the general class rate without ceiling — verified at narrative level via JLARC and Bloomberg Tax, not by direct citation to current statute. Stage-6 cite-check required.
- Any PWC-specific BPP appeal record contesting Schedule C as a non-FMV proxy — none located in public docket searches; trade-press recommendations exist but no Virginia case law on point.
