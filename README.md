# IDX Exchange – CRMLS Data Extraction Project
## Overview
This repository contains my internship project work for IDX Exchange. The project focuses on extracting CRMLS real estate listing and sold-property data from the CoreLogic Trestle API and exporting the results into CSV files for analysis.
The scripts are designed to pull monthly datasets by modifying the date filters within each script. Data is retrieved through authenticated API requests and written to CSV format for downstream analysis and reporting.


## Repository Contents

### Scripts

* `crmls_sold.py`
  * Extracts sold-property records for a specified month.
  * Filters records based on `CloseDate`.
  * Exports data to a CSV file.

* `crmls_listed.py`
  * Extracts property listing records for a specified month.
  * Filters records based on `ListingContractDate`.
  * Exports data to a CSV file.

* `week1_dataset_aggregation.py`
  * Loads all monthly sold and listing CSV files from January 2024 through May 2026 (29 months).
  * Handles both standard (`CRMLSSold202401.csv`) and `_filled` (`CRMLSSold202401_filled.csv`) filename formats.
  * Concatenates all monthly files into two unified datasets — one for sold transactions and one for listings.
  * Filters both datasets to residential properties only (`PropertyType == 'Residential'`).
  * Prints row counts before and after concatenation and before and after the residential filter for validation.
  * Saves the combined datasets as:
    * `combined_sold_residential.csv`
    * `combined_listings_residential.csv`

* `week2_3_eda.py`
  * Loads the combined sold and listing datasets produced by `week1_dataset_aggregation.py`.
  * Performs exploratory data analysis (EDA) across both datasets.
  * Step 1 — prints row and column counts for both datasets.
  * Step 2 — prints all column data types to identify mistyped fields (e.g. dates stored as strings).
  * Step 3 — calculates missing value counts and percentages per column, flags columns with more than 90% missing values, and drops flagged columns from both datasets.
  * Step 4 — produces a numeric distribution summary (count, mean, std, min, percentiles, max) for key fields: `ClosePrice`, `ListPrice`, `OriginalListPrice`, `LivingArea`, `LotSizeAcres`, `BedroomsTotal`, `BathroomsTotalInteger`, `DaysOnMarket`, and `YearBuilt`.
  * Prints unique property types found in each dataset.
  * Fetches the national 30-year fixed mortgage rate (MORTGAGE30US) directly from the FRED API.
  * Resamples the weekly mortgage rate data to monthly averages.
  * Creates a `year_month` join key from `CloseDate` (sold) and `ListingContractDate` (listing).
  * Merges the monthly mortgage rates onto both datasets using the `year_month` key.
  * Validates the merge by checking for any null mortgage rate values after joining.
  * Saves the cleaned and enriched datasets as:
    * `sold_eda.csv`
    * `listing_eda.csv`
    * `sold_with_mortgage.csv`
    * `listing_with_mortgage.csv`


## Requirements

### Python Version
* Python 3.x

### Dependencies
Install required packages:
```bash
pip install requests pandas
```


## Running the Scripts

### Generating Monthly Sold Data
The sold data script exports all properties that closed within a specified month.

To generate a file for a different month, update the date range in the filter statement:
```python
'$filter': f"MlsStatus eq 'Closed' and CloseDate ge {datetime(2026, 1, 1).isoformat(timespec='milliseconds')}Z and CloseDate lt {datetime(2026, 2, 1).isoformat(timespec='milliseconds')}Z",
```
The first date represents the beginning of the target month and the second date represents the beginning of the following month.

Also update the output filename:
```python
csv_file = 'CRMLSSold202601.csv'
```

For example, to generate April 2026 sold data:
```python
csv_file = 'CRMLSSold202604.csv'
```

Run the script:
```bash
python crmls_sold.py
```


### Generating Monthly Listing Data
The listing data script exports all listings whose `ListingContractDate` falls within the specified month.

Update the date range:
```python
'$filter': f"ListingContractDate ge {datetime(2026, 1, 1).isoformat(timespec='milliseconds')}Z and ListingContractDate lt {datetime(2026, 2, 1).isoformat(timespec='milliseconds')}Z",
```

Change the start and end dates to match the month you want to extract.

Also update the output filename:
```python
csv_file = 'CRMLSListing202601.csv'
```

For example, to generate April 2026 listing data:
```python
csv_file = 'CRMLSListing202604.csv'
```

Run the script:
```bash
python crmls_listed.py
```


### Running the Week 1 Aggregation Script
Before running, ensure all monthly CSV files are downloaded into your local csv folder and update the `csv_folder` path in the script:
```python
csv_folder = "/Users/your-username/csv"
```

Then run:
```bash
python week1_dataset_aggregation.py
```

Expected output:
```text
Sold rows before filter:     XXX,XXX
Listings rows before filter: XXX,XXX
Sold rows after filter:      XXX,XXX
Listings rows after filter:  XXX,XXX
Done! Files saved.
```


### Running the Weeks 2-3 EDA Script
Ensure `combined_sold_residential.csv` and `combined_listings_residential.csv` are present in your csv folder before running. Update the `csv_folder` path in the script if needed:
```python
csv_folder = "/Users/your-username/csv"
```

An internet connection is required to fetch live mortgage rate data from the FRED API.

Then run:
```bash
python week2_3_eda.py
```

Expected output:
```text
Sold Dataset
Rows: XXX,XXX
Columns: 84
Listing Dataset
Rows: XXX,XXX
Columns: 84
Sold columns with >90% missing: [column names]
Listing columns with >90% missing: [column names]
Sold columns before drop: 84
Sold columns after drop: 69
Listing columns before drop: 84
Listing columns after drop: 71
Sold Numeric Summary: [statistics table]
Listing Numeric Summary: [statistics table]
Saved sold_eda.csv and listing_eda.csv
Null mortgage rates in sold: 0
Null mortgage rates in listing: 0
Saved sold_with_mortgage.csv and listing_with_mortgage.csv
```


## Output

### Extraction Scripts
The extraction scripts generate monthly CSV files containing CRMLS real estate data.

Example outputs:
```text
CRMLSSold202601.csv
CRMLSSold202602.csv
CRMLSSold202603.csv
CRMLSListing202601.csv
CRMLSListing202602.csv
CRMLSListing202603.csv
```

### Week 1 Aggregation Script
```text
combined_sold_residential.csv      — All residential sold transactions, January 2024 through May 2026
combined_listings_residential.csv  — All residential listings, January 2024 through May 2026
```

### Weeks 2-3 EDA Script
```text
sold_eda.csv                — Sold dataset with >90% missing columns removed
listing_eda.csv             — Listing dataset with >90% missing columns removed
sold_with_mortgage.csv      — Sold dataset enriched with monthly 30-year fixed mortgage rates
listing_with_mortgage.csv   — Listing dataset enriched with monthly 30-year fixed mortgage rates
```


## Key EDA Findings (Weeks 2-3)

### Dataset Size
* Sold: 430,436 rows, 84 columns (69 after dropping high-missing columns)
* Listing: 592,023 rows, 84 columns (71 after dropping high-missing columns)

### Missing Value Summary
* 15 columns dropped from sold dataset, 13 from listing dataset, all with more than 90% missing values
* Notable dropped columns: `WaterfrontYN` (99.94%), `FireplacesTotal` (100%), `TaxYear` (100%), `ElementarySchoolDistrict` (100%)

### Numeric Field Observations
* Median close price: $825,000 (sold) — median is preferred over mean due to heavy skew from outliers
* Median days on market: 18 days — mean of 37 days is inflated by extreme outliers
* Invalid values identified for cleaning in Weeks 4-5: negative `DaysOnMarket` values, `ClosePrice` of $0, `LivingArea` of 0

### Date Consistency Issues
* 64 records where `CloseDate` is before `ListingContractDate` — flagged for cleaning in Weeks 4-5

### Mortgage Rate Enrichment
* 30-year fixed mortgage rate data fetched from FRED (MORTGAGE30US series)
* Weekly rates resampled to monthly averages and merged onto both datasets using a `year_month` key
* Zero null mortgage rate values after merge, confirming a complete join

## Internship Project
This repository is maintained throughout my IDX Exchange internship to document project progress, track individual contributions, and facilitate collaboration and feedback from teammates.
