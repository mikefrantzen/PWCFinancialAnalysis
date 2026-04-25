# Virginia DC Tax Competitive Landscape — Research Note

**Sub-agent:** competitive-tax-research
**As of:** 2026-04-25 (one day after the 2026 GA special session recessed without a budget)
**Audience:** PWC Stage 6 modeler — input to a C&P rate-elasticity scenario ($4.50 → $6-$10/$100)
**Companion artifact:** `data/va_county_tax_stack.csv`

## 1. Va. Code § 58.1-609.3(18) — sales-and-use tax exemption (DCRSUT)

**Citation.** Va. Code § 58.1-609.3(18); locally classified DC computer equipment is at § 58.1-3506(A)(43).

**Current thresholds (administered via MOU with VEDP).**
- General: ≥ $150M capex; ≥ 50 new FT jobs at ≥ 150% of local average wage.
- Distressed locality: ≥ $70M; ≥ 10 jobs.
- 2040 extension: aggregate ≥ $35B / ≥ 1,000 direct jobs; MOU between 1 Jan 2023 and 1 Jul 2035.
- 2050 extension: aggregate ≥ $100B / ≥ 2,500 jobs.

**Sunset.** Base sunset is **30 June 2035**; per-operator extensions can push to 2040 or 2050.

**Forgone revenue.** JLARC: $135.9M FY23 → $928M FY24; $1.6–1.9B FY25 on $33.2B of tax-free purchases; cumulative ~$2.7B.

**JLARC 2024 (Report 598) recommendations.** Three options to the GA: (1) extend past 2035; (2) allow lapse to slow growth and grid impact; (3) **partial exemption to 2050 with energy-efficiency, residential-impact, and natural-resource conditions** — JLARC's "balance" option. Other key findings: 80% of state DC industry sits in Loudoun + PWC + Fairfax; Loudoun alone ≈50%. Dominion 2024 IRP forecasts DC peak demand reaching 9 GW within 10 years (a +25% lift on total system peak); VA must add 150% generation AND import 150% more out-of-state energy to serve half of unconstrained demand. PJM capacity auctions cleared at record prices partly because of NoVA DC load.

**2025 GA action.** HB 1600 / SB 800 (FY26 budget) directed the Joint Subcommittee on Tax Policy to study the DCRSUT in the 2025 interim. No statutory change.

**2026 GA action (just-concluded regular session + 23 Apr special session).** Of ~61 DC-related bills, 15 cleared both chambers; 46 carried to 2027. Most consequential:
- **SB 253 (Lucas) / HB 1393 (LeVere Bolling)** — cost-shift bills creating a GS-5 large-load tariff class, full PJM capacity-auction cost-causation onto DCs, expanded low-income weatherization. Spanberger amended to direct SCC to "take all measures to reasonably ensure" DC costs are not subsidized; GA rejected most amendments on 22 Apr 2026.
- **HB 155 (Thomas)** — pre-interconnection SCC review of high-power facilities; tabled.
- **HB 503 (McAuliff)** — bar socializing DC-dedicated transmission/generation costs onto general ratepayers; carried over.
- **Senate budget (Lucas omnibus)** — accelerates DCRSUT sunset to **1 Jan 2027**, redirects revenue to transportation/water.
- **House budget (Torian)** — preserves 2035 sunset but conditions exemption on clean-energy procurement and efficiency standards.
- Conferees did not reconcile in the regular session; the 23 Apr 2026 special session recessed without a deal. FY27 status is unresolved as of writing.

**Spanberger's position.** Confirmed: Spanberger took office 11 Jan 2026 after winning Nov 2025 against Earle-Sears. Her stated stance is contractarian — "the Commonwealth should abide by contracts we sign" — i.e., honor existing MOUs, allow new constraints prospectively. She has floated a *consumption-style* DC excise as an alternative to repeal. She has not endorsed the Senate's 2027 acceleration. She is more aggressive on cost-shift (SB 253 / HB 1393) than on the exemption itself.

**Probability assessment for 2027/2028 (sub-agent judgment, scenario weights).**
- Pure repeal pre-2035: **10–15%** — Spanberger contractarian framing, House resistance, ~$80B FY24-25 invested capital under MOUs.
- Status quo to 2035: **25–30%** — closest to the House FY26-27 budget.
- **Conditioned partial exemption to 2050 (JLARC option 3): 35–40%** — most likely conferee compromise.
- Per-facility or per-MW cap on exempt purchases: 15–20%.
- New consumption / excise tax layered on top of preserved exemption: 25–30% (not mutually exclusive with the others). Spanberger's preferred channel.

**Cost impact — 100 MW PWC campus (illustrative).**
A 100 MW campus carries ~$1.0–$1.5B of IT equipment alone (refresh ~3 yrs), plus $0.5–$0.7B M&E. At PWC's 6.0% combined SUT rate (4.3% state + 1.0% local + 0.7% NoVA regional), full repeal of the exemption costs **$60–$90M one-time per IT-equipment turn**, or ~$20–$30M/yr steady-state. Adding the qualifying M&E adds another ~$30–$50M one-time per build cycle. A *cap* (e.g., $30M/facility/yr exempt) is essentially nullified by month four for a hyperscaler refresh, leaving ~90% of refresh CAPEX still exempted; a *per-MW* cap (e.g., $300K/MW/yr) would meaningfully bind.

## 2. C&P / BPP rate table — Virginia DC counties

Structured CSV: `data/va_county_tax_stack.csv` (17 jurisdictions, all requested fields populated). Headlines:
- **Loudoun:** $4.15/$100 DC C&P, $0.805 RE. Held at $4.20 since 1987; cut to $4.15 for TY2026 alongside a *lengthened* depreciation schedule (longer recapture; net revenue effect positive).
- **Fairfax:** **no separate DC class** — DC equipment taxed at $4.57 general PP rate; $1.1225 RE.
- **Stafford / Spotsylvania:** $1.25/$100 DC class, set 2019 via the Fredericksburg Regional Alliance pact (with Caroline, King George, Fredericksburg). Deliberate recruit posture.
- **Henrico:** rotated from $0.40 (2017 ultra-recruit) to $2.60 for TY2026 — a 6.5× increase. The single most analogous "post-recruit normalize" pivot to PWC's own.
- **Chesterfield:** $0.24 — lowest published DC rate in VA (Meta-recruit posture from 2022).
- **Mecklenburg:** $3.40 nominal but ~$0.34 *effective* on Microsoft Boydton via a 20-yr 90% PILOT-style grant.
- **City of Virginia Beach:** $0.40 (Globalinx / Telxius cable-landing recruit).
- **Pittsylvania:** DC class under active drafting around the Stack Infrastructure / Berry Hill MOU ($73B / 30 yrs / 2,050 jobs).

## 3. City of Manassas as a redirect target

Manassas DC C&P = **$2.15/$100** (raised 72% in FY25 from $1.25); RE $1.43; same Dominion-adjacent fiber backbone as PWC. Technically attractive vs. PWC's $4.50, but:
- The single operating DC (Brickyard / Digital Realty) is leased to a bank; § 58.1-1202 Bank Franchise Tax preempts BPP — Manassas collects $0 BPP from its largest DC tenant. Distorts the recruit story.
- City area ~9.9 sq mi, largely built-out; few suitable parcels.
- Power is **Manassas Department of Utilities** (municipal), not Dominion. Some operators view this as a plus (industrial rate); hyperscalers requiring Dominion contract structures find it unsuitable.

**Verdict.** Credible *partial* redirect for a 5–25 MW operator displaced by a punitive PWC rate; not credible for a 200+ MW Pageland-class campus. Manassas Park is a non-factor (no DC class, ~2.5 sq mi).

## 4. PWC trajectory vs. peers (TY2022–TY2026)

| TY (FY adopted) | PWC | Loudoun | Fairfax | Stafford | Henrico | Chesterfield |
|---|---:|---:|---:|---:|---:|---:|
| 2022 | 1.65 | 4.20 | 4.57 | 1.25 | 0.40 | 1.80 |
| 2023 (FY24) | 2.15 | 4.20 | 4.57 | 1.25 | 0.40 | 0.24 |
| 2024 (FY25) | 3.70 | 4.20 | 4.57 | 1.25 | 0.40 | 0.24 |
| 2025 (FY26) | 4.15 | 4.20 | 4.57 | 1.25 | 0.40 | 0.24 |
| 2026 (FY27) | 4.50 | 4.15 | 4.57 | 1.25 | 2.60 | 0.24 |

- **Loudoun cut its headline rate** $0.05 for TY2026 while lengthening depreciation; offset is positive in revenue but headline is now LOWER than PWC.
- **Fairfax flat.**
- **Henrico raised aggressively** ($0.40 → $2.60) — same playbook PWC is now executing.
- **Stafford / Spotsylvania held the $1.25 line** — leaning *into* the recruit differential.
- **Chesterfield held $0.24.**
- **No NoVA peer cut its DC rate to recruit since 2023.**
- **PWC alone has raised every year for four years**; cumulative +172% (1.65 → 4.50).

## 5. Tip-out threshold

Direct operator statements are scarce (negotiation hygiene). Indirect evidence:
- **Historical Loudoun-PWC differential.** 2012-2022, PWC sat ~$3/$100 *below* Loudoun and captured Loudoun spillover when land cleared $2-3M/acre. As of TY2026, PWC is **$0.35 ABOVE** Loudoun — the 35-year regional ordering has inverted.
- **Industry commentary (Bisnow, Data Center Frontier, 2025).** Operators tolerate ~$1/$100 differential vs. the regional anchor when offset by land/fiber; redirect becomes credible above ~$2/$100; greenfield builds (no sunk land) flip earliest.
- **Out-of-state substitution.** Texas and Maryland (Frederick County, MD has no county PP tax) framed in 2026 coverage as the boundaries beyond which the marginal hyperscaler dollar leaves Virginia.

**Working assumption for the elasticity model:** redirect probability is approximately step-shaped with an inflection at ~$1.50–$2.00/$100 above the Loudoun-Fairfax mean ($4.36). PWC at $4.50 is +$0.14 — within tolerance. PWC at $7.00 is +$2.64 — past inflection. PWC at $10.00 is +$5.64 — past the leave-Virginia threshold for marginal builds.

## 6. Stylized 5-year tax stack — 100 MW campus

Assumptions: $1.0B IT (3-yr refresh), $0.5B M&E, $50M land, $200M shell; 5-yr horizon; first-year assessed value 50% of original cost on standard NoVA depreciation curve (60/40/30/20/10); RE base $250M; FY27 rates from CSV; out-of-state alt = Frederick County, MD (no county PP tax; MD state SUT exemption); DCRSUT assumed extended (status quo).

| Locality | DC C&P | Yr1 C&P tax | Yr1 RE tax | 5-yr cum. C&P | 5-yr cum. RE | 5-yr total |
|---|---:|---:|---:|---:|---:|---:|
| PWC @ $4.50 | 4.50 | $22.5M | $2.27M | $94M | $11.3M | **$105M** |
| PWC @ $7.00 | 7.00 | $35.0M | $2.27M | $146M | $11.3M | **$157M** |
| PWC @ $10.00 | 10.00 | $50.0M | $2.27M | $209M | $11.3M | **$220M** |
| Loudoun | 4.15 | $20.8M | $2.01M | $87M | $10.0M | **$97M** |
| Fairfax | 4.57 | $22.9M | $2.81M | $95M | $14.0M | **$109M** |
| Henrico | 2.60 | $13.0M | $2.13M | $54M | $10.6M | **$65M** |
| Frederick MD | 0.00 | $0 | $1.13M (county-only) | $0 | $5.6M | **$6M** |

- PWC at $7.00 is **$60M/100 MW above Loudoun over 5 yrs**; at $10.00 the gap is $123M.
- Henrico becomes the cheapest in-state alternative at $40-155M cumulative savings.
- Maryland's gap is dominated by the absence of county PP tax (~$100M/100MW vs. PWC even at $4.50). Offset by Dominion-vs-PJM-east interconnect-queue penalties and weaker fiber concentration.
- DCRSUT lapse is a **uniform shift across VA** (~$100-150M/100MW over 5 yrs); does NOT reorder VA cells, but flips VA-vs-MD decisively in MD's favor.

## 7. JLARC fiscal/regional/grid summary

State-level fiscal: $135.9M FY23 → $928M FY24 → $1.6-1.9B FY25 forgone state SUT; ~$2.7B cumulative. Regional: 80% of VA DC industry in Loudoun + PWC + Fairfax; Loudoun ~50%. Grid: Dominion DC peak doubling 2017-2020 and again 2020-2024; 9 GW in 10 yrs (+25% on total system peak); PJM capacity-auction record prices; +150% generation AND +150% out-of-state imports needed for half of unconstrained demand. Local-vs-state structural tension: industry produces large *local* PP-tax revenue (Loudoun, PWC) but minimal direct *state* revenue under the exemption — making localities the principal fiscal beneficiaries and the principal political stakeholders.

## Sources

- Code of Virginia § 58.1-609.3(18); § 58.1-3506(A)(43) — law.lis.virginia.gov
- VEDP DCRSUT page — vedp.org/incentive/data-center-retail-sales-use-tax-exemption
- JLARC Report 598, *Data Centers in Virginia* (Dec 2024) — jlarc.virginia.gov/landing-2024-data-centers-in-virginia.asp
- *Virginia Tax Exemptions for Data Centers* — RD40 (2 Jan 2026) — rga.lis.virginia.gov/Published/2026/RD40/PDF
- LIS 2026 bills: HB155, HB503, HB1393, SB253; LIS 2025 budget: HB1600, SB800
- Virginia Mercury, Cardinal News, VPM, WHRO, Inside Climate News (multiple 2026 articles)
- Loudoun County: loudoun.gov/1570, /1922, /6188; FY27 adopted budget
- PWC FY27 adopted budget; PWC 2024 Data Center Industry Tax Revenue Report
- City of Manassas Commissioner of the Revenue
- Stafford treasurer; gostaffordva.com (2019)
- Fauquier County current tax rates page
- Henrico County FY26 budget; henricocitizen.com; businessfacilities.com (2017)
- Chesterfield Fits (grpva.com)
- Tax Foundation, *State Taxation of Data Centers*
- DLA Piper Virginia Tax Alert (Mar 2026)
- MultiState Insider Virginia DC Legislation roundup (30 Mar 2026)
- Bisnow / Data Center Frontier / Data Center Knowledge industry coverage (2024-2026)
