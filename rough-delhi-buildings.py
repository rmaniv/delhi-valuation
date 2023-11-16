import pandas as pd
buildings = pd.DataFrame()

# - divide 391_buildings.csv (look up README.md) into 2 files
# - split 391_buildings.csv into 2 files to be able to work on them with a computer with 16GB of RAM.
# - split them into files with ~100,000 buildings each for faster processing

chunksize = 10 ** 6
file = 1
for chunk in pd.read_csv('391_buildings_part1.csv', chunksize=chunksize):
    file_name = 'buildings/buildings_' + str(file) + '.csv'
    chunk.to_csv(file_name)
    print('File ', file, ' done.')
    file += 1
for chunk in pd.read_csv('391_buildings_part2.csv', chunksize=chunksize):
    file_name = 'buildings/buildings_' + str(file) + '.csv'
    chunk.to_csv(file_name)
    print('File ', file, ' done.')
    file += 1

# remove the first 2 useless columns

for i in range(1, 75, 1):
    file_name = 'buildings/buildings_' + str(i) + '.csv'
    df = pd.read_csv(file_name)
    df = df.drop(df.columns[0], axis=1)
    df = df.drop(df.columns[0], axis=1)

# extract buildings falling roughly in Delhi based on manually selected coordinates

delhi_ = pd.DataFrame()
for i in range(1, 75, 1):
    
    file_name = 'buildings/buildings_' + str(i) + '.csv'
    df = pd.read_csv(file_name)
    
    latitude_mask = (df['latitude'] > 28.377060) & (df['latitude'] < 28.938108)
    longitude_mask = (df['longitude'] > 76.722650) & (df['longitude'] < 77.466205)
    
    coordinate_mask = latitude_mask & longitude_mask
    
    filtered_df = df[coordinate_mask]
    
    delhi_ = pd.concat([delhi_, filtered_df])

# save those buildings in rough_delhi_buildings.csv

delhi_.to_csv('rough_delhi_buildings.csv')
