import pandas as pd
import os
pd.set_option('display.float_format', '{:,.2f}'.format)
pd.set_option('display.max_columns', None)

csv_folder = "/Users/rsatwik/csv"
sold = pd.read_csv(os.path.join(csv_folder, "sold_week4_5.csv"), low_memory = False)
listing = pd.read_csv(os.path.join(csv_folder, "listing_week4_5.csv"),low_memory = False)

#metrics

sold["price_ratio"] = sold["ClosePrice"] / sold["OriginalListPrice"]
sold["price_per_sqft"] = sold["ClosePrice"] / sold["LivingArea"]
sold["close_to_original_list_ratio"] = sold["ClosePrice"] / sold["OriginalListPrice"]
sold["CloseDate"] = pd.to_datetime(sold["CloseDate"])
sold["PurchaseContractDate"] = pd.to_datetime(sold["PurchaseContractDate"])
sold["ListingContractDate"] = pd.to_datetime(sold["ListingContractDate"])
#time converstion
sold["Year"] = sold["CloseDate"].dt.year
sold["Month"] = sold["CloseDate"].dt.month
sold["YrMo"] = sold["CloseDate"].dt.to_period("M")

#days collection

sold["listing_to_contract_days"] = (sold["PurchaseContractDate"] - sold["ListingContractDate"]).dt.days
sold["contract_to_close_days"] = (sold["CloseDate"] - sold["PurchaseContractDate"]).dt.days

print(sold[["ClosePrice", "OriginalListPrice", "price_ratio", "price_per_sqft", 
            "listing_to_contract_days", "contract_to_close_days"]].head())

listing["ListingContractDate"] = pd.to_datetime(listing["ListingContractDate"])

listing["Year"] = listing["ListingContractDate"].dt.year
listing["Month"] = listing["ListingContractDate"].dt.month
listing["YrMo"] = listing["ListingContractDate"].dt.to_period("M")

#Segment analysis

print("Segment Analysis by PropertySubType:")
print(sold.groupby("PropertySubType")[["ClosePrice", "price_per_sqft", "DaysOnMarket"]].median())

# segment analysis by CountyOrParish
print("\nSegment Analysis by CountyOrParish:")
print(sold.groupby("CountyOrParish")[["ClosePrice", "price_per_sqft", "DaysOnMarket"]].median())

# segment analysis by ListOfficeName
print("\nTop 10 List Offices by Median Close Price:")
print(sold.groupby("ListOfficeName")[["ClosePrice"]].median().sort_values("ClosePrice", ascending=False).head(10))

# segment analysis by BuyerOfficeName
print("\nTop 10 Buyer Offices by Median Close Price:")
print(sold.groupby("BuyerOfficeName")[["ClosePrice"]].median().sort_values("ClosePrice", ascending=False).head(10))

print("Listing Segment Analysis by PropertySubType:")
print(listing.groupby("PropertySubType")[["ListPrice", "DaysOnMarket"]].median())

print("\nListing Segment Analysis by CountyOrParish:")
print(listing.groupby("CountyOrParish")[["ListPrice", "DaysOnMarket"]].median())

sold.to_csv(os.path.join(csv_folder, "sold_week6.csv"), index=False)
listing.to_csv(os.path.join(csv_folder, "listing_week6.csv"), index=False)














