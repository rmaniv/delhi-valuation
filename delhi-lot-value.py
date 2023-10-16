import pandas as pd

# Load both CSV files
circle_rate_df = pd.read_csv('circle-rate.csv')

# Assuming you'll load this on your local machine
df = pd.read_csv('more_accurate_delhi_lots_with_addresses.csv')

# Initialize new columns for land value, circle rate area, and circle rate land rate
df['land_value'] = 0
df['circle_rate_area'] = ''
df['circle_rate_land_rate'] = 0

# Iterate through each row in df
for index, row in df.iterrows():
    # Extract the address from the row and split it into words
    address_words = set(row['Address'].split())

    # Find the matching area in circle_rate_df based on the address words
    matching_area = None
    for area in circle_rate_df['Area']:
        if area in address_words:
            matching_area = area
            break

    # If a matching area is found, populate the respective columns and compute the land value
    if matching_area:
        land_rate = circle_rate_df[circle_rate_df['Area'] == matching_area].iloc[0]['Land']
        
        df.at[index, 'circle_rate_area'] = matching_area
        df.at[index, 'circle_rate_land_rate'] = land_rate
        df.at[index, 'land_value'] = land_rate * row['area_in_meters']

# Calculate the total land value of all lots
total_land_value = df['land_value'].sum()
print(f"Total land value of all lots: {total_land_value}")

# Save the modified DataFrame
df.to_csv('more_accurate_delhi_lots_with_land_values.csv', index=False)
