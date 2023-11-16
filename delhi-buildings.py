import pandas as pd
import json

# load boundary coordinates for Delhi
with open("new-delhi-coordinates.json", "r") as file:
    data = json.load(file)
geometry = data['features'][0]['geometry']
lat_lon_pairs = geometry['coordinates'][0]

# check if a point is inside a polygon
def is_point_inside_polygon(point, polygon):
    x, y = point
    odd_nodes = False
    j = len(polygon) - 1  # Last vertex in the polygon
    
    for i in range(len(polygon)):
        xi, yi = polygon[i]
        xj, yj = polygon[j]
        if yi < y and yj >= y or yj < y and yi >= y:
            if xi + (y - yi) / (yj - yi) * (xj - xi) < x:
                odd_nodes = not odd_nodes
        j = i

    return odd_nodes

df = pd.read_csv('rough_delhi_buildings.csv')

# check if each point is inside Delhi and store the results in a new column
df['inside_delhi'] = df.apply(lambda row: is_point_inside_polygon((row['longitude'], row['latitude']), lat_lon_pairs), axis=1)

# filter the points that are inside Delhi
delhi_points = df[df['inside_delhi']]

delhi_points.to_csv('more_accurate_delhi_buildings.csv', index=False)
