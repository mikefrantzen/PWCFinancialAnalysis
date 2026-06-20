# Approved-but-not-yet-built data centers and the mid-2026 DCOZOD vote

_Compiled June 2026. Primary and reputable secondary sources cited per row. MW and
gross-sq-ft are frequently absent from county filings; analyst estimates are flagged._

## 1. Why this matters to the model

The county's FY27 adopted budget projects **$549.7M of data-center tax revenue
(~28% of general-fund tax revenue)** for FY27 (PWC FY27 adoption release). That
figure does not rest only on the *operating* fleet (44 completed buildings as of
1/1/2024, TY2024 DC Revenue Report). A large and growing share of it rests on two
things the Board does **not** control by inertia:

1. an **approved-but-not-yet-built pipeline** that has to actually break ground and
   capitalize equipment before it shows up on the Computer & Peripherals (C&P) and
   real-property tax rolls; and
2. an **overlay (DCOZOD) and entitlement regime** reliable enough that operators
   keep committing CAPEX here rather than in Loudoun, WV, or elsewhere.

The April 2026 non-appeal of the Digital Gateway voidance already removed the
single largest future block (~22M sq ft / gigawatt-scale, three voided rezonings).
The mid-2026 DCOZOD vote (below) puts the *reliability of the rest of the pipeline*
on the table.

## 2. Approved-but-not-yet-built inventory (added to the model this stage)

These six projects are **entitled / approved** (rezoning and/or SUP granted) but
**not yet under construction** as of mid-2026. Four of them — Parsons, Stack
Gainesville, Wellington Glen, Iron Mountain VA 8/9 — were **missing from the prior
`dc_inventory.csv`** and are added here as `approved-not-built`. Devlin and the
Wellington/Devlin 44-ac satellite were already carried.

| Project | Operator / applicant | Acres; overlay | Approval & vote | Size (county / est.) | Build status |
|---|---|---|---|---|---|
| Devlin Technology Park | AWS (rezoning by Stanley Martin) | ~269; brought INTO overlay | Rezoned Nov 2023 (5-3); Va. Ct. App. **affirmed Sept 16 2025** | 4.2M sq ft / 7–9 bldgs [county]; MW not published | Land acquired ($700M, Nov 2025); **not started** |
| Parsons Business Park | AWS | ~91; INSIDE overlay | Base rezoning 2019; proffer to 85 ft ~Mar 2024 (5-1) | MW/sq ft est. (~180 MW IT, ~1.2M sq ft) | Land acquired ($218M, Apr 2024); **not started** |
| Stack Gainesville (Wellington Rd) | Stack Infrastructure | 3.28 + 37.4; INSIDE overlay | Rezoned ag→PBD Sept 24 2024 (6-1) | ~815k sq ft, 2 DCs ≤80 ft [press]; ~90 MW IT est. | **Not started** |
| Wellington Glen | AWS (applicant STC Capital) | 49.5; INSIDE overlay | Rezoned Apr 1 2025 (5-3; PC recommended denial 4-2) | 475k sq ft (cut from 983k), ≤75 ft [county]; ~55 MW IT est. | **Not started** |
| Iron Mountain VA 8/9 | Iron Mountain | ~19; INSIDE overlay | Rezoned office-flex/ag→M-2 Jul 30 2025 (unanimous) | **48 MW** [county], ≤75 ft | **Not started** (extends operating campus) |
| Hornbaker Road | Mortenson (contract purchaser) | ~40; OUTSIDE overlay | Rezoned A-1/PBD→M-2 + SUP Mar 3–4 2026 (4-3) | 571k sq ft, ≤80 ft; ~100 MW from 300 MW Pegasus substation [county] | **Not started** |

Only Hornbaker (~100 MW) and Iron Mountain (48 MW) have county-tied MW figures; the
Amazon land-bank sites publish acreage and dollars but not MW. MW/sq-ft for the rest
are analyst estimates scaled from acreage/footprint at hyperscale density and are
flagged as such in `dc_inventory.csv`.

**Model effect.** Adding the four missing approved-not-built sites raises the
no-restart per-DC County **C&P** baseline by roughly **$34M (FY28) → $84M (FY29) →
$93M (FY31)** per year — about **$300M cumulative FY27–FY31** of County C&P revenue
that depends on this approved pipeline actually being built (real-property tax on the
same buildings is additive and larger). See `private_analysis/data/per_dc_summary.csv`
(no_restart scenario) before/after.

## 3. The voided / litigated block (context, not in the baseline)

- **PW Digital Gateway (Pageland Lane):** ~2,139 ac / 194 parcels; three rezonings
  (QTS North REZ2022-00032, QTS South -00033, Compass -00036) approved Dec 13 2023
  (4-3-1). **Void ab initio** (Circuit Court, Judge Irving, Aug 7 2025) for public-
  notice defects; Va. Court of Appeals **affirmed Mar 31 2026**. County (unanimous)
  and Compass dropped the appeal in April 2026; **QTS petitioned the Virginia Supreme
  Court April 30 2026** (discretionary writ stage, undecided as of mid-June 2026). No
  re-application or formal "cure" is underway. County staff had projected up to
  ~$400M/yr at full buildout; critics estimated <$150M/yr.
- **Pending / not approved (excluded):** John Marshall Commons / CTP-II (22.72 ac,
  PC tabled early 2026); Dulles South / Sanders Lane (~1,930 ac, no rezoning filed);
  Quantico Ridge (CPA initiation withdrawn May 8 2026).

## 4. The mid-2026 Board vote — DPA2026-00006 (DCOZOD zoning text amendment)

The data-center matter in motion in mid-2026 is a **board-initiated zoning text
amendment to the Data Center Opportunity Zone Overlay District (DCOZOD)**:

- **Shrinks and redraws the overlay** to only parcels meeting one of five eligibility
  pathways, and **permanently closes the overlay to future expansion**.
- **Ends by-right data-center development** for non-qualifying land — future, non-
  vested projects must obtain a discretionary **Special Use Permit (SUP)** with full
  Board approval rather than streamlined administrative review.
- **Grandfathers** operating, under-construction, and site-plan-vested projects
  (counsel flags grandfathering as incomplete — heightened entitlement risk for
  non-vested projects).

Procedural status (an initiation, not a final vote, as of June 2026):

- **Mar 3 2026** — initiated via Res. 26-125 (reported 6-0, chair abstaining), same
  meeting Hornbaker was approved.
- **Apr 23 2026** — staff briefed DORAC.
- **Jun 9 2026** — Supervisor Tom Gordy (R-Brentsville) introduced a resolution to
  **resume and advance** the ZTA toward a Planning Commission hearing.
- **Late summer 2026 (target)** — Planning Commission hearing.
- **Late 2026 / early 2027 (target)** — final Board adoption.

**What "yes" / "no" mean.** A "yes" (advancing / ultimately adopting the ZTA) shrinks
the overlay and ends by-right, routing future data centers through case-by-case SUP
approval — i.e., it makes the entitlement path slower and reversible. A "no" leaves
the 2016-era overlay and by-right administrative approval in force. A separate county
**data-center fiscal-impact study** (outside consultant + Finance Dept.) feeds the
Comprehensive Plan update and the long-running DCOZOD comprehensive review.

This vote is the operative real-world instance of the project's working hypothesis:
overlay zones are politically reversible, and the entitlement regime can move against
CAPEX between site selection and stabilization.

## 5. Verified primary figures used downstream

- TY2023 DC tax revenue **$166.4M** (+50%); TY2024 **$293.7M** (+77%): $144.2M real
  property, $123.9M C&P (PWC Data Center Industry Tax Revenue Reports).
- FY27 adopted: real-estate rate **$0.906 → $0.865**; C&P **$4.15 → $4.50**; meals
  **3% → 2%** (eff. 1/1/2027) (PWC FY27 adoption release).
- FY27 projected DC tax revenue **$549.7M (~28% of GF tax revenue)**.

> Note on the model's RE rate: the integrated five-year model and solvency report were
> re-baselined (June 2026) to the verified FY27 adopted RE rate of **$0.865** (the
> $0.906→$0.865 cut is $0.041, not the $0.056 used in earlier drafts). The cumulative
> deficit ($1,150M) and residual ($494M) are unchanged; the residential-rate option (C1)
> is correspondingly smaller — full restoration ~$235M (was $320M), half ~$117M (was $160M).
