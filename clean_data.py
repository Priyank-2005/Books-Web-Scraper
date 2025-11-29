import pandas as pd
import re

print("Starting Data Cleaning...")

# 1. Load the raw data
# We use 'encoding="utf-8-sig"' to handle weird Windows characters like Â
try:
    df = pd.read_csv("raw_books_data.csv", encoding="utf-8-sig")
except:
    df = pd.read_csv("raw_books_data.csv", encoding="latin1")

# 2. Nuclear Clean of Price Column
# This Regex says: "Replace anything that is NOT (^) a digit (\d) or a dot (.) with nothing."
df['Price_Clean'] = df['Price'].astype(str).str.replace(r'[^\d.]', '', regex=True)

# Convert to float (now safe because only numbers exist)
df['Price_Clean'] = pd.to_numeric(df['Price_Clean'], errors='coerce')

# 3. Convert Text Ratings to Numbers
rating_map = {
    'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5
}
df['Rating_Num'] = df['Rating'].map(rating_map)

# 4. Create a "Value Score" (Rating / Price)
# Avoid division by zero issues
df = df[df['Price_Clean'] > 0] 
df['Value_Score'] = df['Rating_Num'] / df['Price_Clean']

# 5. Filter: Affordable 5-star books (Price < 20)
top_picks = df[(df['Rating_Num'] == 5) & (df['Price_Clean'] < 20)]

# 6. Save the final dataset
df.to_csv("clean_books_data.csv", index=False)
top_picks.to_csv("top_value_picks.csv", index=False)

print("Data Cleaned Successfully!")
print(f"Found {len(top_picks)} affordable 5-star books.")
print("Check the folder for 'top_value_picks.csv'.")