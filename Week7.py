import pandas as pd
import os
pd.set_option('display.float_format', '{:,.2f}'.format)
pd.set_option('display.max_columns', None)

csv_folder = "/Users/rsatwik/csv"
sold = pd.read_csv(os.path.join(csv_folder, "sold_week6.csv"), low_memory = False)
listing = pd.read_csv(os.path.join(csv_folder, "listing_week6.csv"),low_memory = False)

def flag_outliers(df, col):
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    return (df[col] < lower) | (df[col] > upper)

fields_to_check = ["ClosePrice", "LivingArea", "DaysOnMarket"]
for col in fields_to_check:
    sold["flag_outlier_" + col] = flag_outliers(sold,col)
    print("sold " + col + " outliers: " + str(sold["flag_outlier_" + col].sum()))
for col in fields_to_check:
    listing["flag_outlier_" + col] = flag_outliers(listing, col)
    print("Listing " + col + " outliers: " + str(listing["flag_outlier_" + col].sum()))
#remove outliers
sold_clean = sold[
    (sold["flag_outlier_ClosePrice"] == False) &
    (sold["flag_outlier_LivingArea"] == False) &
    (sold["flag_outlier_DaysOnMarket"] == False)]

listing_clean = listing[
    (listing["flag_outlier_LivingArea"] == False) &
    (listing["flag_outlier_DaysOnMarket"] == False)]

#compare
print("\nBefore filtering:")
print("Rows: ", len(sold))
print(sold[fields_to_check].median())
print("\nAfter filtering:")
print("Rows:", len(sold_clean))
print(sold_clean[fields_to_check].median())

print("\nListing Before filtering:")
print("Rows:", len(listing))

print("\nListing After filtering:")
print("Rows:", len(listing_clean))

#save datasets
sold.to_csv(os.path.join(csv_folder, "sold_flagged.csv"), index=False)
sold_clean.to_csv(os.path.join(csv_folder, "sold_clean.csv"), index=False)
listing.to_csv(os.path.join(csv_folder, "listing_flagged.csv"), index=False)
listing_clean.to_csv(os.path.join(csv_folder, "listing_clean.csv"), index=False)
print("Saved listing_flagged.csv and listing_clean.csv")
print("Saved sold_flagged.csv and sold_clean.csv")

    

    

