# Virginia Housing and Debt Posts: Methods and Data Notes

Dennis Yerby, PhD · [@thedocshango.bsky.social](https://bsky.app/profile/thedocshango.bsky.social) · Updated November 17, 2026

This repository documents four data posts on Virginia housing costs and household debt. Each post uses public data for all 133 Virginia counties and independent cities. Figures describe localities, not individual households.

## Posts covered

| # | Post | Measure | Headline figure |
|---|------|---------|-----------------|
| 1 | Home price vs. income | Median home value ÷ median household income, then ÷ median homeowner income | Median locality: 3.4x (all households), 2.9x (owners) |
| 2 | Property tax burden | Estimated annual tax on a median-valued home ÷ median homeowner income | Median locality: 1.7% |
| 3 | Landlord/tenant court filings | 2025 filings ÷ renter households | 7.6 per 100 renter households |
| 4 | Garnishment court filings | 2025 filings ÷ households | 67 per 1,000 households |

## Data sources

- **Census ACS 5-year estimates** ([api.census.gov](https://api.census.gov)). Post 1 uses 2019–2023 (tables B25077, B19013, B25119). Posts 2–4 use 2020–2024 (B25077, B25119, B25003, B01003).
- **Virginia Department of Taxation, 2025 Assessment/Sales Ratio Study, Table 3.** Nominal and effective real estate tax rates by locality. [PDF](https://tax.am.virginia.gov/sites/default/files/inline-files/2025%20ASRS%20Report.pdf)
- **Virginia Judicial System, General District Court Filings report** (October 2026 edition). Monthly filings by locality and case category; I use the 2025 totals. [PDF](https://www.vacourts.gov/static/courtadmin/aoc/djs/programs/cpss/csi/stats/gdc_filings.pdf)
- **Map boundaries:** Bokeh sample data (2010-vintage county shapes). Bedford city, merged into Bedford County in 2013, is shown as no data.

## How each measure is built

- **Home price ÷ income:** ACS median home value ÷ ACS median household income (or median income of owner-occupied households, table B25119). It is a ratio of two medians, not a mortgage-affordability measure. Home values are owner estimates.
- **Property tax burden:** 2025 effective tax rate (nominal rate × the locality's median assessment/sales ratio) × median home value ÷ 100, then ÷ median owner income. This is a typical-bill estimate, not an actual bill.
- **Landlord/tenant filings:** 2025 General District Court Landlord/Tenant filings ÷ ACS renter-occupied households × 100. This category includes evictions (unlawful detainers) but may include other landlord/tenant cases.
- **Garnishments:** 2025 General District Court Garnishment filings ÷ ACS households × 1,000.

## Choices that affect the results

- **Shared courts.** 133 localities map to 123 court units. Harrisonburg/Rockingham, Lexington/Rockbridge and Williamsburg/James City are shown as combined in the court report. I also treated Manassas and Manassas Park with Prince William, Poquoson with York, Norton with Wise, Covington with Alleghany, and Fairfax City and Falls Church with Fairfax County. Those last groupings are my inference from the report (zero or very low counts in the smaller locality); I have not confirmed them with the courts.
- **"Less certain" flags.** Hollow dots and hatched areas mark estimates I would not rank precisely: income margins of error above 20%, assessment ratios that moved more than 15 points between 2024 and 2025, court units with fewer than 25 (eviction) or 50 (garnishment) filings, and court units where expunged cases are missing.
- **Year mismatches.** Post 1 uses 2019–2023 data. Posts 2–4 use 2020–2024 ACS with 2025 tax and court data.

## What these numbers do not show

- **Filings are not evictions or garnishments.** A filing is a case started. Many end in payment plans, dismissals or settlements. The same household can appear in several filings.
- **Expunged cases are excluded.** The court report omits deleted and expunged cases. The 2025 unlawful detainer expungement report lists large counts for Richmond city, Henrico, Virginia Beach, Chesapeake and Loudoun, which likely means their filing counts are understated. I saw only part of that list, so other localities may be affected too.
- **Garnishment geography.** A garnishment can be filed where the judgment was entered, not necessarily where the debtor lives ([Va. Code Title 8.01, Ch. 18, Art. 7](https://law.lis.virginia.gov/vacodefull/title8.01/chapter18/article7/)). The report does not separate wage garnishments from other garnishments, or say what type of debt is involved.
- **Property tax scope.** Rates exclude town taxes, personal property (vehicle) taxes, and local exemptions or relief programs.
- **Margins of error.** Small localities have wide ACS margins of error, often 10–15% on income. Differences of a few tenths between neighbors are not meaningful.
- **Causes.** None of these charts explains why a place ranks high or low.

## Repository layout

```
data/acs/      ACS pulls from the Census API (2023 and 2024 5-year)
data/tax/      Table 3 parsed from the Virginia Tax PDF, plus the merged tax-burden file
data/courts/   Court report parsed to CSV, court-unit rates for evictions and garnishments
charts/        Final chart and map images, numbered in posting order
code/          Python scripts that parse the PDFs and draw the charts
```

## Reproducing the work

ACS data was pulled with the Census API in R (`jsonlite`; a free API key is required). The Virginia Tax and court PDFs were parsed in Python (`pdfplumber`), and charts and maps were drawn in Python (`matplotlib`; map shapes from `bokeh.sampledata`). The scripts were written in a working folder, so they point to file paths that you will need to change to run them on your own machine. The source PDFs are not included here; use the links above.

Questions or corrections are welcome as GitHub issues.
