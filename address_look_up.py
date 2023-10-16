import pandas as pd
import requests
import time

# Load the CSV file
df = pd.read_csv('more_accurate_delhi_lots.csv')

# Define a function to reverse geocode using Nominatim API and append all addresses
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

addresses = []

user_agent_base = "DelhiLots"
user_agent_counter = 1

count = 0
# Reverse geocode each row in the DataFrame
for index, row in df.iterrows():
    if index % 100 == 0:  # Change user agent every 100 requests
        user_agent = user_agent_base + str(user_agent_counter)
        user_agent_counter += 1

    address = reverse_geocode_nominatim(row['latitude'], row['longitude'], user_agent)
    if count % 1000 == 0:
        print(count)
    count += 1
    if address:
        addresses.append(address)
    time.sleep(0.001)  # Respect Nominatim's rate limit

# Convert list of addresses to a DataFrame
df_addresses = pd.DataFrame(addresses, columns=["Address"])

# Drop rows that don't contain the word "Delhi"
df_addresses = df_addresses[df_addresses['Address'].str.contains('Delhi', case=False, na=False)]

# Save the filtered DataFrame to CSV
df_addresses.to_csv('all_addresses.csv', index=False)
