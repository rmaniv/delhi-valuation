import pandas as pd
lots = pd.DataFrame()

chunksize = 10 ** 6
file = 1
for chunk in pd.read_csv('test1.csv', chunksize=chunksize):
    file_name = 'lots/lots_' + str(file) + '.csv'
    chunk.to_csv(file_name)
    print('File ', file, ' done.')
    file += 1
for chunk in pd.read_csv('test2.csv', chunksize=chunksize):
    file_name = 'lots/lots_' + str(file) + '.csv'
    chunk.to_csv(file_name)
    print('File ', file, ' done.')
    file += 1

for i in range(1, 75, 1):
    file_name = 'lots/lots_' + str(i) + '.csv'
    df = pd.read_csv(file_name)
    df.drop(['Unnamed: 0.1'], axis=1)

delhi_ = pd.DataFrame()
for i in range(1, 75, 1):
    
    file_name = 'lots/lots_' + str(i) + '.csv'
    df = pd.read_csv(file_name)
    
    latitude_mask = (df['latitude'] > 28.377060) & (df['latitude'] < 28.938108)
    longitude_mask = (df['longitude'] > 76.722650) & (df['longitude'] < 77.466205)
    
    coordinate_mask = latitude_mask & longitude_mask
    
    filtered_df = df[coordinate_mask]
    
    delhi_ = pd.concat([delhi_, filtered_df])

delhi_.to_csv('rough_delhi_lots.csv')
