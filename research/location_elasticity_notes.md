---
title: Location Elasticity of Data-Center CAPEX to a PWC C&P Rate Hike
author: research sub-agent
date: 2026-04-25
purpose: Inform PWC Stage 6 rate-hike scenario ($4.50 -> $6-$10 / $100)
status: draft, sources cited inline
horizon: FY27-FY31
---

## 1. How hyperscalers prioritize buildout location

Power has displaced everything else as the binding constraint. JLL's 2025/2026 Global Data Center Outlooks rank "speed to power" #1, ahead of community support, latency, and construction cost; tax is secondary because it is dominated by the time-value of MW. [JLL 2025](https://www.jll.com/content/dam/legacy/jll-com/documents/pdf/research/global/jll-data-center-outlook-2025.pdf), [CBRE H1 2025](https://www.cbre.com/insights/reports/north-america-data-center-trends-h1-2025).

Practitioner ordering, converging across JLL, CBRE, NAIOP and Hanwha in 2025:
1. Power: capacity, speed-to-energization, redundant feeds, queue position. [Hanwha](https://www.hanwhadatacenters.com/blog/power-availability-the-new-1-in-data-center-site-selection/)
2. Network proximity / fiber and customer latency.
3. Permitting & regulatory predictability ("speed to permit"). [Datacenters.com](https://www.datacenters.com/news/power-water-and-permits-the-new-pillars-of-data-center-site-selection)
4. Community / political support (newly elevated in 2024-2026).
5. Land cost & contiguous parcels.
6. Tax environment (state sales-tax exemption is large; BPP/C&P rate is meaningful but secondary).
7. Water (cooling) and climate/disaster.
8. Construction & operating workforce.

The 2025 framing: "good" vs "great" sites differ "in months shaved off utility timelines, not cents per square foot." [Tax Notes 12/2025](https://www.taxnotes.com/special-reports/tax-preference-items-and-incentives/energy-new-currency-powerful-tax-incentives-data-center-site-selection/2025/12/29/7tf5b). Tax matters, but rate deltas must be weighed against 24-48 month delay risk elsewhere.

## 2. The "Data Center Alley" concentration

Northern Virginia (Loudoun + PWC + Fairfax + Manassas) is the world's largest market by a wide margin: 5.6 GW operational vs 1.5 GW for #2 Dallas-Fort Worth (JLL year-end 2024); H1 2025 absorption of 2.2 GW had ~647 MW (29%) in NoVa. [JLL H1 2025](https://www.jll.com/en-us/newsroom/data-center-availability-crisis-deepens-as-vacancy-hits-historic-low). NoVa equates to ~13-14% of global live capacity and ~25% of the Americas. [Mordor](https://www.mordorintelligence.com/industry-reports/northern-virginia-data-center-market), [WTOP 6/2025](https://wtop.com/business-finance/2025/06/northern-virginia-data-centers-have-topped-4900-megawatts-what-does-that-mean/). Loudoun alone hosts ~160 facilities across ~31 M sq ft and ~46 M sq ft constructed/permitted as of Feb 2025. [DCD](https://www.datacenterdynamics.com/en/news/loudoun-county-data-center-market-share-drops-as-new-virginia-jurisdictions-rise/).

The concentration is significantly self-reinforcing: MAE-East/Ashburn carries historical fiber peering, the largest customers have on-net cross-connects, and PJM/Dominion substations have years of queue position. NVTC and JLL describe this as a network-effect moat for new builds. But the moat depends on Dominion power; once the local grid is full (Ashburn now is), incremental MW must site elsewhere regardless of local tax -- which is why Culpeper, Stafford, Spotsylvania, Berkeley County WV, and Chesterfield have absorbed marginal CAPEX since 2024.

## 3. Peer-county / out-of-state rate landscape (2025-26)

| Jurisdiction | DC C&P / BPP rate ($/$100) | Notes |
|---|---|---|
| **PWC** | **$4.50** advertised FY27; FY26 enacted $4.15 | [Potomac Local 3/2025](https://www.potomaclocal.com/2025/03/06/prince-william-county-proposes-data-center-tax-increase-amid-budget-talks/), [WTOP 4/2025](https://wtop.com/prince-william-county/2025/04/prince-william-supervisors-near-final-approval-for-tax-hike-on-data-centers-homeowners/) |
| Loudoun | $4.20; "DE" depreciation schedule lengthened TY2026 | [Loudoun BPP](https://www.loudoun.gov/6301/Business-Personal-Property-Tax-Assessmen), [DMA](https://dmainc.com/news-and-insights/virginia-loudoun-county-property-tax-updates/) |
| Fairfax | $4.57 (general computer-equipment class) | [Fairfax EDA](https://fairfaxcountyeda.org/wp-content/uploads/091225Taxes.pdf) |
| Henrico (White Oak) | $0.40 historically; raised to $2.60 in 2025 | [Richmonder](https://www.richmonder.org/henrico-became-a-data-center-hub-seemingly-overnight-how-did-it-happen-and-what-are-the-impacts/) |
| Stafford | $1.25 dedicated DC class (vs $5.49 general BPP) | [DCD](https://www.datacenterdynamics.com/en/news/stafford-county-virginia-proposes-tax-cuts-data-centers/) |
| Spotsylvania, Fredericksburg, Caroline, King George | $1.25 (Fredericksburg-region uniform compact) | [Spotsy](https://www.spotsylvania.va.us/586/Tax-Rates) |
| Culpeper County | County BPP ~$2.05; Town offers negotiated incentive deals | [InsideNoVa Culpeper](https://www.insidenova.com/culpeper/culpeper-town-council-secures-data-center-revenue-agreements-one-worth-millions/) |
| Frederick County VA | General BPP ~$4.86; no dedicated DC class confirmed for 2026 |
| Maryland (Frederick/Howard/Montgomery) | State 10-yr sales/use exemption available; county DC class rates not located in primary | [MD Commerce](https://commerce.maryland.gov/fund/data-center-maryland-sales-and-use-tax-exemption-incentive-program) |
| West Virginia (Berkeley/Jefferson) | 2023 microgrid law: 50% to state PIT-reduction, **30% to host county**, 10% per-capita statewide, 10% misc. | [WTOV9](https://wtov9.com/news/local/west-virginia-counties-begin-seeing-tax-revenue-from-data-centers-after-2023-law) |
| Texas (DFW/Austin) | No state property tax; sales/use exemption (HB 1223); JETI replaces Ch. 313; ~$1B/yr forgone | [Comptroller](https://comptroller.texas.gov/taxes/data-centers/), [TX Tribune 4/2026](https://www.texastribune.org/2026/04/08/texas-data-centers-sales-tax-break-billion-dollars/) |
| Arizona (Phoenix) | TPT/use-tax exemption 10-20 yrs; min $50 M Maricopa/Pima; runs through 12/31/2033 | [AZ Commerce](https://www.azcommerce.com/incentives/computer-data-center-program/) |
| Iowa | Permanent computer-equipment exemption for qualified DCs (>$200 M); $150 M/yr program | [Iowa DOR](https://revenue.iowa.gov/taxes/tax-guidance/sales-use-excise-tax/data-centers) |
| Oregon | No state sales tax; Strategic Investment Program / Enterprise Zone abates property tax 15 yrs | [DCD](https://www.datacenterdynamics.com/en/analysis/us-tax-breaks-state-by-state/) |
| Ohio | Sales/use exemption with $100 M investment + $1.5 M payroll | [Stream](https://www.streamdatacenters.com/resource-library/glossary/ohio-state-data-center-tax-incentives/) |

**Differential at $6-$10 vs peers.** Against Loudoun ($4.20), PWC at $6 = +43% premium per $ of assessed BPP; at $10 = +138%. Against Stafford/Spotsylvania ($1.25), PWC at $6 = +380%; at $10 = +700%. The meaningful comparison for hyperscalers is **total tax cost per MW-year**: with VA depreciation retaining ~50-60% of original cost over 7 years, $6 implies ~$3.60/yr per $100 of original CAPEX, $10 implies ~$6.00. On a $1 B campus that is a $36-60 M annual delta vs Loudoun and $100-150 M vs the Fredericksburg compact -- enough to redirect new builds where alternatives exist.

## 4. Virginia sales-tax exemption (Va. Code Sec. 58.1-609.3(18))

**Status April 2026.** Exemption (since 2010) covers qualifying DC equipment; thresholds $150 M capex + 50 net new jobs at >=150% local prevailing wage; 5.3-7.0% combined state/local sales-use tax avoided. Sunset **June 30, 2035**. [VEDP](https://www.vedp.org/incentive/data-center-retail-sales-use-tax-exemption).

**JLARC Dec 2024 (Report 598).** Exemption cost VA $2.73 B FY21-FY24, ~53% of all economic-development incentive spending FY15-FY24. [JLARC pres](https://jlarc.virginia.gov/pdfs/presentations/Rpt598Pres-1.pdf), [Va. Business 12/2024](https://virginiabusiness.com/virginia-data-centers-tax-exemption-2-7-billion/). Original "but-for" was 90%; updated estimate ~50% and declining as the network/power moat carries more of the lifting. [Rpt 598](https://jlarc.virginia.gov/pdfs/reports/Rpt598-2.pdf). JLARC offered three options: extend, expire, or modify (energy/community conditions).

**2025 GA.** SB800 was the principal reform vehicle; budget amendment 4-14 #7S was committee-approved -- conditioning rather than sunset. [LIS](https://budget.lis.virginia.gov/amendment/2025/1/SB800/Introduced/CA/4-14/7S/).

**2026 GA (regular session closed; special session April 23, 2026).**
- **Senate** budget would let exemption **expire** and redirect ~$1.6 B FY25 forgone revenue to taxpayer rebates. [VPM 3/12/2026](https://www.vpm.org/generalassembly/2026-03-12/budget-data-center-tax-break-scott-lucas-spanberger-torian-rephann), [FFXnow 3/17/2026](https://www.ffxnow.com/2026/03/17/general-assemblys-data-center-tax-dispute-leaves-va-budget-unresolved/).
- **House** would **condition** exemption on environmental/energy compliance (JLARC Option 3). [Inside Climate News 2/18/2026](https://insideclimatenews.org/news/18022026/virginia-data-center-tax-exemption/).
- **Gov. Spanberger (D, sworn in Jan 2026)** opposes outright repeal and has floated a **DC consumption tax** as a substitute revenue mechanism; her amendments to House energy-cost-shift bills were criticized as weakening them. [Va. Mercury 4/22/2026](https://virginiamercury.com/2026/04/22/the-governors-amendments-to-energy-and-data-center-legislation-will-save-money-for-customers/), [Va. Mercury 4/16/2026](https://virginiamercury.com/2026/04/16/lawmakers-dominion-say-spanbergers-amendments-weaken-bill-to-shift-costs-onto-data-centers/).
- 15 ancillary DC bills (energy allocation, siting, water) **passed** in 2026; exemption fight unresolved into the special session. [MultiState 3/30/2026](https://www.multistate.us/insider/2026/3/30/virginia-lawmakers-pass-15-data-center-bills-as-tax-exemption-fight-looms), [Inside Climate News 4/24/2026](https://insideclimatenews.org/news/24042026/data-center-tax-exemption-stalls-virginia-budget/).

**Cost-stack.** On a $1 B refresh, the exemption is worth ~$53-70 M one-time; JLARC reports ~$1.0-1.6 B/yr forgone statewide FY24-FY25. If repealed/capped, operator cost-stack rises ~5-7% of equipment CAPEX **every refresh cycle** -- a step-change that compounds with any local C&P hike.

**Load-bearing for PWC's scenario:** if the exemption survives (Spanberger position), $6-$10 is a marginal-cost shift hyperscalers can absorb on sunk capital. If repealed or sharply conditioned, combined state+PWC shock could push new buildout out of the Commonwealth, not just out of the county.

## 5. Loudoun's by-right elimination -- observed CAPEX response

Loudoun BoS adopted the ZOAM eliminating by-right DC use on **March 18, 2025**; applications submitted before Feb 12, 2025 were grandfathered if >500 ft from residential. [Loudoun Now](https://www.loudounnow.com/news/by-right-data-centers-eliminated-in-loudoun-existing-applications-grandfathered/article_130515be-0478-11f0-ab4f-7771b6b47f71.html), [Holland & Knight](https://www.hklaw.com/en/insights/publications/2025/04/loudoun-county-virginia-eliminates-by-right-data-center-development).

Effects through Q1 2026:
- **Loudoun market share dropped** as new VA jurisdictions absorbed CAPEX. [DCD](https://www.datacenterdynamics.com/en/news/loudoun-county-data-center-market-share-drops-as-new-virginia-jurisdictions-rise/).
- **Land prices stayed elevated** (DC land >$4 M/acre) -- grandfathered pipeline + power scarcity outweighed regulatory chill.
- **Adjacent jurisdictions** (PWC, Culpeper, Stafford, Spotsylvania, Fauquier, Chesterfield) announced new sites/zones; Culpeper's Technology Zone (690 ac) is direct successor positioning. [Bean Kinney](https://www.beankinney.com/data-center-shake-up-new-rules-and-hotspots-in-virginia/).
- **Loudoun residential permits** -53% YoY (upstream PWC analysis; not re-verified).
- **Dominion CAPEX** unchanged/up: $50.1 B 2025-2029 plan, +16%.

The Loudoun analog suggests rate/regulatory shocks **redirect** marginal CAPEX within Virginia rather than evicting it from the Commonwealth, **as long as power and the state exemption remain intact.** PWC currently sits in the "successor" position; a punitive C&P hike would forfeit that role.

## 6. Recapitalization vs. new buildout -- elasticity differs sharply

**New buildout** is mobile on a 24-48 month horizon. Operators evaluate ~5-10 candidate sites; rate differentials of $30-150 M/yr on a $1 B campus are decisive when power timelines are comparable. JLL/CBRE place tax in tier-2 of decision criteria.

**Recapitalization** of an existing campus (5-7 yr server refresh per IBM/EY/PwC) is **highly sticky**. [IBM](https://www.ibm.com/think/insights/data-center-optimization), [EY](https://www.ey.com/en_us/data-centers/data-center-development-the-stabilized-asset-cycle). Once building, substation tap, fiber drops, cross-connects are sunk, the marginal cost of relocating in-place compute is large (facility re-stranding, SLA breach, network re-homing). Industry response to local-tax shifts: (1) slow refresh cadence, (2) direct net-new to lower-tax sister campuses, (3) lobby/litigate, and rarely (4) abandon a working campus over BPP rate. Henrico's 2017 cut $3.50 -> $0.40 attracted Meta to White Oak (greenfield); Henrico's 2025 hike to $2.60 has not produced reported in-place departures. [Business Facilities](https://businessfacilities.com/henrico-county-virginia-cuts-data-center-tax-rate/). We found no published case of a hyperscaler abandoning an operational NoVa campus over BPP rate.

**Practical elasticity estimates** (derived):
- New-build CAPEX, NoVa overlay: **-1.0 to -1.5%** per +$1/$100 of C&P differential vs Loudoun, conditional on power being available elsewhere.
- In-place refresh CAPEX: **-0.1 to -0.3%** per +$1/$100 in years 1-3 (refresh deferral), rising to **-0.5 to -1.0%** over 7+ years as customer footprints can be migrated.
- Threshold: +$2 differential (PWC $6 vs Loudoun $4.20) is absorbable; +$5 (PWC $10, especially stacked with state-exemption loss) plausibly triggers redirect of net-new and refresh slowdown across PWC's existing 200+ MW base.

## 7. VA hyperscaler announcements 2024-2026

- **Google.** $9 B through YE 2026 in VA: new Chesterfield campus + expansions in Loudoun and PWC. [CoStar](https://www.costar.com/article/394047264/google-to-invest-9-billion-in-virginia-ai-cloud-data-centers-as-space-becomes-scarce).
- **AWS.** 91 ac in Manassas (PWC) for $218 M, April 2025; expanding Loudoun/Fairfax/PWC plus Fauquier, Culpeper, King George, Spotsylvania, Stafford, Louisa, Orange, Caroline. [DCD](https://www.datacenterdynamics.com/en/news/amazon-acquires-george-washington-universitys-technology-campus-in-ashburn-virginia/).
- **Microsoft.** Expansion in Leesburg, Aldie, Manassas, Bristow. [dgtlinfra](https://dgtlinfra.com/amazon-aws-microsoft-data-centers-virginia/).
- **Meta.** Existing Henrico/White Oak; no major new PWC announcement post-Pageland in primary press.
- **Berkeley County WV.** $4 B, ~550 ac (reported Google) announced Feb 2026 -- the first multi-billion-dollar DC announcement explicitly outside Virginia in the immediate post-Pageland window. [Tri-State Alert](https://tristatealert.com/nearly-550-acre-4-billion-data-center-coming-to-falling-waters-in-berkeley-county/).

We did **not** find any operator publicly citing the April 2026 PWC non-appeal as an explicit redirect rationale. The redirect signal is implicit in the geographic dispersion of new announcements (Chesterfield, Berkeley County WV, Fredericksburg-region, Culpeper).

## Bottom line for Stage 6 modeling

1. PWC at $6 is competitive with Loudoun ($4.20) only because Loudoun is power-constrained and special-exception-only; net-new mobile CAPEX is still redirectable to Stafford/Spotsylvania ($1.25), Culpeper, Berkeley County WV, or out-of-state.
2. PWC at $10 sits **outside the NoVa peer band by 2-8x** and -- combined with erosion of the state DCRSUT exemption -- plausibly triggers redirect of marginal new-build CAPEX and slowed refresh. The exemption status is the single most load-bearing exogenous variable.
3. In-place recap is sticky but not infinitely so; realistic 5-yr elasticity is **-5% to -15%** for refresh CAPEX at +$5/$100 differential (PWC's downside under CAPEX Spillover).
4. PWC's room to raise is bounded by the **lower** of (a) the Loudoun + Henrico political-defensibility band ($4.50-$5.00) and (b) the rate at which combined state+local shock relocates net-new commitments -- literature places this near +$3-$5 vs Loudoun, contingent on the exemption fight.

**Open items where primary sources were thin or absent:** Loudoun CAPEX time series pre/post 3/18/2025 ZOAM (qualitative redirection only); Frederick County VA 2026 DC-specific class rate; MD county DC-specific personal property rates; operator statements explicitly citing the April 2026 PWC non-appeal.
