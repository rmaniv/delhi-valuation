import pandas as pd
import requests
import time

df = pd.read_csv('more_accurate_delhi_lots.csv')

df['Address'] = ''

# reverse geocode using Nominatim API and append all addresses
def reverse_geocode_nominatim(lat, lng, user_agent):
    base_url = "https://nominatim.openstreetmap.org/reverse"
    params = {
        "lat": lat,
        "lon": lng,
        "format": "json"
    }
    headers = {
        "User-Agent": user_agent
    }
    response = requests.get(base_url, headers=headers, params=params)
    
    try:
        data = response.json()
        return data['display_name']
    except Exception as e:
        print(f"Error processing response: {e}")
        return None

user_agent_base = "DelhiLots"
user_agent_counter = 1

for index, row in df.iterrows():

    if index % 100 == 0:  # Change user agent every 100 requests
        user_agent = user_agent_base + str(user_agent_counter)
        user_agent_counter += 1

    address = reverse_geocode_nominatim(row['latitude'], row['longitude'], user_agent)
    
    # Update the 'Address' column for the current row
    df.at[index, 'Address'] = address
    print(df.at[index, 'Address'])
    
    time.sleep(1)

# filter out rows without "Delhi" in the address
df = df[df['Address'].str.contains('Delhi', case=False, na=False)]

df.to_csv('more_accurate_delhi_lots_with_addresses.csv', index=False)
