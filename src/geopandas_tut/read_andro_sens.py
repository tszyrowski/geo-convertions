"""
 Created on 31 Aug 2019
"""
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import shapely.wkt
import utm

def read_geo_pd_csv(file):
    """Read from andro_sensor csv file, drop a few columns and return GeoDataFrame"""
     
    df = pd.read_csv(file)
    cols_to_leave = ["LIGHT", "LOCATION Latitude : ", "LOCATION Longitude : ",
                    "ACCELEROMETER X ", "ACCELEROMETER Y", "ACCELEROMETER Z",
                    "LOCATION Accuracy", "Time since start in ms ", "YYYY-MO-DD HH-MI-SS_SSS"]
    df = df[cols_to_leave]
    df.rename(columns={"LIGHT":"light", 
                       "LOCATION Latitude : ":"lat", 
                       "LOCATION Longitude : ":"long",
                       "ACCELEROMETER X ":"accel_x",
                       "Time since start in ms ":"elapsed",
                       "YYYY-MO-DD HH-MI-SS_SSS":"timestamp"},inplace=True)
    crs = {'init': 'epsg:4326'}
    gdf = gpd.GeoDataFrame(df, 
                           crs=crs, 
                           geometry=gpd.points_from_xy(df.long, df.lat))
    return  gdf

def read_from_wkt(file):
    """Read from csv with geometry stored previously"""
    
    df = pd.read_csv(file, index_col="index")
    df['geometry'] = df['geometry'].apply(shapely.wkt.loads)
    gdf = gpd.GeoDataFrame(df, geometry='geometry')
    return gdf

def store_gdf(gdf):
    """Save GeoDataFrame to files"""
    
    gdf.to_file("./data/sensor_shp/sensor_path.shp")
    gdf.to_csv("./data/sensor_path.csv", index_label="index")

def plot_gdf(gdf):
    """Plot GeoDataFrame with geometry"""
    
    fig = plt.figure(1, dpi=90)
    ax = fig.add_subplot(111)
    gdf.plot(ax=ax)

if __name__ == '__main__':
    
#     file = './data/Sensor_record_20190830_205836_AndroSensor.csv'
#     gdf = read_geo_pd_csv(file)
    
    file = './data/sensor_path.csv'
    gdf = read_from_wkt(file)

    print('lat: ',gdf['lat'].values[:10])
    print('long: ',gdf['long'].values[:10])
    print(gdf.head())
    
#     store_gdf(gdf)
#     for col in gdf:
#         print(gdf[col].describe())
        
#     print('gdf.crs={}'.format(gdf.crs))
    fig = plt.figure(1, dpi=90)
    ax1 = fig.add_subplot(111)
    gdf.plot(ax=ax1)
    
    print('************')
    
#     gdf_utm = convert_to_utm(gdf)
    print('------------')

    
    plt.show()
    
