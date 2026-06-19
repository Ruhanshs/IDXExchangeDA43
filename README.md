# IDX Exchange – CRMLS Data Extraction Project

## Overview

This repository contains my internship project work for IDX Exchange. The project focuses on extracting CRMLS real estate listing and sold-property data from the CoreLogic Trestle API and exporting the results into CSV files for analysis.

The scripts are designed to pull monthly datasets by modifying the date filters within each script. Data is retrieved through authenticated API requests and written to CSV format for downstream analysis and reporting.

---

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

---

## Requirements

### Python Version

* Python 3.x

### Dependencies

Install required packages:

```bash
pip install requests
```

---

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

---

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

---

## Output

The scripts generate monthly CSV files containing CRMLS real estate data.

Example outputs:

```text
CRMLSSold202601.csv
CRMLSSold202602.csv
CRMLSSold202603.csv

CRMLSListing202601.csv
CRMLSListing202602.csv
CRMLSListing202603.csv
```

---

## Notes

* Use the first day of the target month as the start date.
* Use the first day of the following month as the end date.
* Ensure the CSV filename matches the month being extracted.
* Large datasets are automatically retrieved using API pagination.
* Verify that the extracted file corresponds to the intended month before distribution.

---

## Internship Project

This repository is maintained throughout my IDX Exchange internship to document project progress, track individual contributions, and facilitate collaboration and feedback from teammates.
