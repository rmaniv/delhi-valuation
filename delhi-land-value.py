import pandas as pd

circle_rate_df = pd.read_csv('circle-rate.csv')

df = pd.read_csv('more_accurate_delhi_buildings_with_addresses.csv')

df['land_value'] = 0
df['circle_rate_area'] = ''
df['circle_rate_land_rate'] = 0

for index, row in df.iterrows():
    
    address_words = set(row['Address'].split())

    # find the matching area in circle_rate_df based on the address words
    matching_area = None
    for area in circle_rate_df['Area']:
        if area in address_words:
            matching_area = area
            break

    if matching_area:
        land_rate = circle_rate_df[circle_rate_df['Area'] == matching_area].iloc[0]['Land']
        
        df.at[index, 'circle_rate_area'] = matching_area
        df.at[index, 'circle_rate_land_rate'] = land_rate
        # calculate land value
        df.at[index, 'land_value'] = land_rate * row['area_in_meters']

# total land value of all buildings
total_land_value = df['land_value'].sum()
print(f"Total land value under all buildings: {total_land_value}")

df.to_csv('more_accurate_delhi_buildings_with_land_values.csv', index=False)
