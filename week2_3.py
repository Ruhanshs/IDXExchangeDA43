import pandas as pd
import os
pd.set_option('display.float_format', '{:,.2f}'.format)
pd.set_option('display.max_columns', None)
csv_folder = "/Users/rsatwik/csv"
#load datasets
sold = pd.read_csv(os.path.join(csv_folder,"combined_sold_residential.csv"),low_memory=False)
listing = pd.read_csv(os.path.join(csv_folder,"combined_listings_residential.csv"),low_memory=False)  
#Rows and Columns
print("Sold Dataset")
print("Rows:", sold.shape[0])
print("Columns:", sold.shape[1])                         
print("Listing Dataset")
print("Rows:", listing.shape[0])
print("Columns:", listing.shape[1])
#column data types
print(sold.dtypes)
print(listing.dtypes)
#missing value counts and percentages
sold_missing_counts = sold.isnull().sum()
sold_missing_percent = (sold.isnull().mean()*100).round(2)
listing_missing_count = listing.isnull().sum()
listing_missing_percent = (listing.isnull().mean() * 100).round(2)
print('Sold Missing Count:', sold_missing_counts)
print('Sold Missing Perecent:', sold_missing_percent)
print("Listing Missing Count:", listing_missing_count)
print("Listing Missing Percent:", listing_missing_percent)
#Flagging Columns
sold_flagged = sold_missing_percent[sold_missing_percent > 90]
listing_flagged = listing_missing_percent[listing_missing_percent > 90]
print("Sold columns with >90% missing:")
print(sold_flagged)
print("Listing columns with >90% missing:")
print(listing_flagged)
numeric_fields = ["ClosePrice", "ListPrice", "OriginalListPrice", "LivingArea", 
                  "LotSizeAcres", "BedroomsTotal", "BathroomsTotalInteger", 
                  "DaysOnMarket", "YearBuilt"]
#Dropping Columns
cols_to_drop = []
for col in sold_flagged.index:
    cols_to_drop.append(col)
sold_cleaned = sold.drop(columns=cols_to_drop)
print("Sold columns before drop:", sold.shape[1])
print("Sold columns after drop:", sold_cleaned.shape[1])
listing_cols_to_drop = []
for col in listing_flagged.index:
    listing_cols_to_drop.append(col)

listing_cleaned = listing.drop(columns=listing_cols_to_drop)

print("Listing columns before drop:", listing.shape[1])
print("Listing columns after drop:", listing_cleaned.shape[1])
#statistic summaries
sold_numeric = []
listing_numeric =[]
for col in numeric_fields:
    if col in sold_cleaned.columns:
        sold_numeric.append(col)
for col in numeric_fields:
    if col in listing_cleaned.columns:
        listing_numeric.append(col)
print("Sold Numeric Summary:")
print(sold_cleaned[sold_numeric].describe())

print("Listing Numeric Summary:")
print(listing_cleaned[listing_numeric].describe())

# unique property types
print("Unique Property Types in Sold:")
print(sold_cleaned["PropertyType"].unique())
print("Unique Property Types in Listing:")
print(listing_cleaned["PropertyType"].unique())

# save filtered datasets
sold_cleaned.to_csv(os.path.join(csv_folder, "sold_eda.csv"), index=False)
listing_cleaned.to_csv(os.path.join(csv_folder, "listing_eda.csv"), index=False)
print("Saved sold_eda.csv and listing_eda.csv")

#FRED mortgage data
url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"

mortgage = pd.read_csv(
    url,
    parse_dates=["observation_date"]
)

mortgage.columns = [
    "date",
    "rate_30yr_fixed"
]


# Create a month key
mortgage["year_month"] = mortgage["date"].dt.to_period("M")


#Getting monthly mortgage rates
mortgage_monthly = (
    mortgage.groupby("year_month")["rate_30yr_fixed"]
    .mean()
    .reset_index()
)
#creating year_month column in sold and listing files
sold_cleaned["CloseDate"] = pd.to_datetime(sold_cleaned["CloseDate"])
sold_cleaned["year_month"] = sold_cleaned["CloseDate"].dt.to_period("M")
listing_cleaned["ListingContractDate"] = pd.to_datetime(listing_cleaned["ListingContractDate"])
listing_cleaned["year_month"] = (listing_cleaned["ListingContractDate"].dt.to_period("M"))

#merging mortgage column into sold and listing files
sold_with_rates = sold_cleaned.merge( mortgage_monthly, on="year_month", how="left")
listing_with_rates = listing_cleaned.merge( mortgage_monthly, on="year_month", how="left")
#check of null values
print("Null mortgage rates in sold:", sold_with_rates["rate_30yr_fixed"].isnull().sum())
print("Null mortgage rates in listing:", listing_with_rates["rate_30yr_fixed"].isnull().sum())

#save updated datasets
sold_with_rates.to_csv(
    os.path.join(csv_folder, "sold_with_mortgage.csv"),
    index=False
)

listing_with_rates.to_csv(
    os.path.join(csv_folder, "listing_with_mortgage.csv"),
    index=False
)

