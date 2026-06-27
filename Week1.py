import pandas as pd
import os

# ── CONFIG ──────────────────────────────────────────────────────────────────
csv_folder = "/Users/rsatwik/csv"

months = [
    "202401","202402","202403","202404","202405","202406",
    "202407","202408","202409","202410","202411","202412",
    "202501","202502","202503","202504","202505","202506",
    "202507","202508","202509","202510","202511","202512",
    "202601","202602","202603","202604","202605",
]

# ── LOAD & CONCATENATE ───────────────────────────────────────────────────────
sold_frames = []
listing_frames = []

for ym in months:
    # Try both naming conventions
    sold_path        = os.path.join(csv_folder, f"CRMLSSold{ym}.csv")
    sold_path_filled = os.path.join(csv_folder, f"CRMLSSold{ym}_filled.csv")
    listing_path        = os.path.join(csv_folder, f"CRMLSListing{ym}.csv")
    listing_path_filled = os.path.join(csv_folder, f"CRMLSListing{ym}_filled.csv")

    if os.path.exists(sold_path):
        sold_frames.append(pd.read_csv(sold_path, low_memory=False))
    elif os.path.exists(sold_path_filled):
        sold_frames.append(pd.read_csv(sold_path_filled, low_memory=False))
    else:
        print(f"WARNING: Missing file {sold_path}")

    if os.path.exists(listing_path):
        listing_frames.append(pd.read_csv(listing_path, low_memory=False))
    elif os.path.exists(listing_path_filled):
        listing_frames.append(pd.read_csv(listing_path_filled, low_memory=False))
    else:
        print(f"WARNING: Missing file {listing_path}")

sold     = pd.concat(sold_frames,    ignore_index=True)
listings = pd.concat(listing_frames, ignore_index=True)

# Row counts BEFORE filter
print(f"Sold rows before filter:     {len(sold):,}")
print(f"Listings rows before filter: {len(listings):,}")

# ── FILTER TO RESIDENTIAL ────────────────────────────────────────────────────
sold     = sold[sold["PropertyType"] == "Residential"]
listings = listings[listings["PropertyType"] == "Residential"]

# Row counts AFTER filter
print(f"Sold rows after filter:     {len(sold):,}")
print(f"Listings rows after filter: {len(listings):,}")

# ── SAVE ─────────────────────────────────────────────────────────────────────
sold.to_csv(os.path.join(csv_folder, "combined_sold_residential.csv"), index=False)
listings.to_csv(os.path.join(csv_folder, "combined_listings_residential.csv"), index=False)

print("Done. Files saved.")