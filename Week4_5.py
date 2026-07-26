import pandas as pd
import os
import geopandas as gpd
from shapely.geometry import Point
csv_folder = "/Users/rsatwik/csv"
sold = pd.read_csv(os.path.join(csv_folder, "sold_with_mortgage.csv"), low_memory = False)
listing = pd.read_csv(os.path.join(csv_folder, "listing_with_mortgage.csv"),low_memory = False)
#converting to datetime format
key_fields = ["CloseDate", "PurchaseContractDate", "ListingContractDate", "ContractStatusChangeDate"]
for col in key_fields:
    sold[col] = pd.to_datetime(sold[col])
    listing[col] =pd.to_datetime(listing[col])
print("Latitude missing:", sold["Latitude"].isnull().sum())
print("Longitude missing:", sold["Longitude"].isnull().sum())
print("latfilled missing:", sold["latfilled"].isnull().sum())
print("lonfilled missing:", sold["lonfilled"].isnull().sum())
#Unnecessary and duplicate columns
# BuyerAgentAOR + ListAgentAOR + BuyerOfficeAOR
#ListingKey + ListingKeyNumeric
#StreetNumberNumeric
#OriginatingSystemName, OriginatingSystemSubName
#Latfilled, lonfilled
#BuyerAgencyCompensationType, BuyerAgencyCompensation
col_to_drop = ["BuyerAgentAOR", "ListAgentAOR", "BuyerOfficeAOR",
    "ListingKeyNumeric",
    "StreetNumberNumeric",
    "OriginatingSystemName", "OriginatingSystemSubName",
    "BuyerAgencyCompensationType", "BuyerAgencyCompensation",
    "latfilled", "lonfilled"]
col_to_drop2 = []
for col in col_to_drop:
    if col in sold:
        col_to_drop2.append(col)

sold = sold.drop(columns =  col_to_drop2)

list_cols_to_drop2 = []
for col in col_to_drop:
    if col in listing:
        list_cols_to_drop2.append(col)
listing = listing.drop(columns = list_cols_to_drop2)

listing_dupes = [col for col in listing.columns if col.endswith(".1")]
for col in listing_dupes:
    original = col.replace(".1", "")
    if original in listing.columns:
        same = listing[col].equals(listing[original])
        print(f"{original} vs {col}: same values = {same}")
    else:
        print(f"{col}: no original column found")
listing = listing.drop(columns=listing_dupes)

# Handling Missing Values
key_fields = ["ListOfficeName", "BuyerOfficeName", "ListAgentFullName", 
                "BuyerAgentFirstName", "BuyerAgentLastName",
                "Latitude", "Longitude", "PropertySubType", "MLSAreaMajor"]
for value in key_fields:
    if value in sold.columns:
        missing = sold[value].isnull().sum()
        pct =  round(missing/len(sold)*100,2)
        print("sold" + value +": ", pct)
for value in key_fields:
    if value in listing.columns:
        missing = listing[value].isnull().sum()
        pct =  round(missing/len(listing)*100,2)
        print(print("listing"+ value +": ", pct))
clean = ["LivingArea", "City", "BathroomsTotalInteger", "YearBuilt"]

sold = sold.dropna(subset= clean)
listing = listing.dropna(subset = clean)

#Ensure numeric fields are properly typed
int_fields = ["BedroomsTotal", "BathroomsTotalInteger", "YearBuilt"]

for col in int_fields:
    if col in sold.columns:
        sold[col] = sold[col].astype("Int64")
    if col in listing.columns:
        listing[col] = listing[col].astype("Int64")

# confirm the change
print("Sold after conversion:")
for col in int_fields:
    print(col + ": " + str(sold[col].dtype))

print("\nListing after conversion:")
for col in int_fields:
    print(col + ": " + str(listing[col].dtype))
#flag numeric values
sold["flag_invalid_close_price"] = sold["ClosePrice"] <= 0
sold["flag_invalid_living_area"] = sold["LivingArea"] <= 0
sold["flag_negative_dom"] = sold["DaysOnMarket"] < 0
sold["flag_negative_bedrooms"] = sold["BedroomsTotal"] < 0
sold["flag_negative_bathrooms"] = sold["BathroomsTotalInteger"] < 0

listing["flag_invalid_close_price"] = listing["ClosePrice"] <= 0
listing["flag_invalid_living_area"] = listing["LivingArea"] <= 0
listing["flag_negative_dom"] = listing["DaysOnMarket"] < 0
listing["flag_negative_bedrooms"] = listing["BedroomsTotal"] < 0
listing["flag_negative_bathrooms"] = listing["BathroomsTotalInteger"] < 0
print("Sold invalid value counts:")
print("ClosePrice <= 0:", listing["flag_invalid_close_price"].sum())
print("LivingArea <= 0:", listing["flag_invalid_living_area"].sum())
print("DaysOnMarket < 0:", listing["flag_negative_dom"].sum())
print("Negative Bedrooms:", listing["flag_negative_bedrooms"].sum())
print("Negative Bathrooms:", listing["flag_negative_bathrooms"].sum())

sold = sold[
    (sold["flag_invalid_close_price"] == False) &
    (sold["flag_invalid_living_area"] == False) &
    (sold["flag_negative_dom"] == False)]

listing = listing[
    (listing["flag_invalid_living_area"] == False) &
    (listing["flag_negative_dom"] == False)]

print("Sold rows after removing invalid:", len(sold))
print("Listing rows after removing invalid:", len(listing))

#Data Consistency Check
sold["listing_after_close_flag"] = sold["ListingContractDate"] > sold["CloseDate"]
sold["purchase_after_close_flag"]  = sold["PurchaseContractDate"] > sold["CloseDate"]   
sold["negative_timeline_flag"] = sold["PurchaseContractDate"] < sold["ListingContractDate"]  

#Geographic checks
sold["flag_missing_coords"] = sold["Latitude"].isnull() | sold["Longitude"].isnull()
sold["flag_zero_coords"] = (sold["Latitude"] == 0) | (sold["Longitude"] == 0)
sold["flag_positive_longitude"] = sold["Longitude"] > 0
print("Geographic Data Checks for Sold:")
print("Missing coordinates:", sold["flag_missing_coords"].sum())
print("Zero coordinates:", sold["flag_zero_coords"].sum())
print("Positive longitude (should be negative for CA):", sold["flag_positive_longitude"].sum())

listing["flag_missing_coords"] = listing["Latitude"].isnull() | listing["Longitude"].isnull()
listing["flag_zero_coords"] = (listing["Latitude"] == 0) | (listing["Longitude"] == 0)
listing["flag_positive_longitude"] = listing["Longitude"] > 0

print("\nGeographic Data Checks - Listing:")
print("Missing coordinates:", listing["flag_missing_coords"].sum())
print("Zero coordinates:", listing["flag_zero_coords"].sum())
print("Positive longitude (should be negative for CA):", listing["flag_positive_longitude"].sum())

#School district joining

districts = gpd.read_file(os.path.join(csv_folder, "DistrictAreas2526_-284845464123469011.geojson"))
districts = districts[districts["DistrictType"] == "Unified"]
print(("Unified school districts found:", len(districts)))

sold_geo = gpd.GeoDataFrame(sold,geometry=gpd.points_from_xy
                            (sold["Longitude"], sold["Latitude"]),crs="EPSG:4326")
listing_geo = gpd.GeoDataFrame(listing,geometry=gpd.points_from_xy
                               (listing["Longitude"], listing["Latitude"]),crs="EPSG:4326")
districts = districts.to_crs("EPSG:4326")    

sold_with_districts = gpd.sjoin(sold_geo, districts[["DistrictName", "geometry"]], 
                                 how="left", predicate="within")   
listing_with_districts = gpd.sjoin(listing_geo, districts[["DistrictName", "geometry"]], 
                                    how="left", predicate="within")
sold["DistrictName"] = sold_with_districts["DistrictName"].values
listing["DistrictName"] = listing_with_districts["DistrictName"].values
print("Sold properties with district assigned:", sold["DistrictName"].notna().sum())
print("Listing properties with district assigned:", listing["DistrictName"].notna().sum())

#Save CSV files
sold.to_csv(os.path.join(csv_folder, "sold_week4_5.csv"), index=False)
listing.to_csv(os.path.join(csv_folder, "listing_week4_5.csv"), index=False)
print("Saved sold_week4_5.csv and listing_week4_5.csv")






    
        








