"""
 Created on 1 Sep 2019
"""
import pandas as pd
import utm.conversion as convert
import numpy as np
from shapely.geometry import Point


def transform_gps_to_utm(df, in_point_col, lat_col, long_col, inplace=True):
    """Transform UTM x, y , grid to Latitude and Longitude
    
    Params:
        df (pandas.DataFrame): with Longitude and Latitude coordinates
        in_point_col (str): Column name of new Shapely point of x, y coordinate
        lat_col (str): Name of the column to output latitude
        long_col (str): Name of the column to output longitude
        inplace (bool): True- replace existing, 
                        False- create new one 
                        
    Returns: 
        df
    """

    def _convert(x):
        """Helper for single convertions"""
        easting = x[0].x
        northing = x[0].y
        zone_number, zone_letter = x[1].replace(',',';').split(';',1)
        return convert.to_latlon(easting, 
                                 northing, 
                                 int(zone_number), 
                                 zone_letter)
    
    # if lat and long column names already exists and inplace is False
    if not inplace and lat_col in df.columns:
        lat_col = '{}_new'.format(lat_col)
        long_col = '{}_new'.format(long_col)
    
    df[lat_col], df[long_col] = zip(*df[[in_point_col, "grid"]].
                                    apply(lambda x: _convert(x), axis=1))

    return df

class TestTransformGpsToUtm():
    """Group of tests for GPS to UTM transorm"""
    def df_in(self):
        df = pd.DataFrame({'lat': [50.38621, 50.38615, 50.386124,
                                   50.386116, 50.3861, 50.386097,
                                   50.386086, 50.38608, 50.38608,
                                   50.38608 ],
                           'long': [-4.148402, -4.148387, -4.148371,
                                    -4.148364, -4.148351, -4.148345,
                                    -4.148343, -4.148328, -4.148317,
                                    -4.148302],
                           'A': np.random.randn(10),
                           'EN': [Point(418359.60059718, 5582203.060540936),
                                  Point(418360.5639061191, 5582196.372802922),
                                  Point(418361.6566844113, 5582193.464354321),
                                  Point(418362.140570124, 5582192.567167133),
                                  Point(418363.0372532262, 5582190.773890653),
                                  Point(418363.4586353551, 5582190.433740599),
                                  Point(418363.5819265808, 5582189.208478752),
                                  Point(418364.6379578019, 5582188.524885572),
                                  Point(418365.4199352756, 5582188.512810587),
                                  Point(418366.486268195, 5582188.496344883)],
                           'grid': ['30;U', '30;U', '30;U', '30;U', '30;U',
                                    '30;U', '30;U', '30;U', '30;U', '30;U']
                           })
        return df
 
    def test_df(self):
        """Test DataFrame usual case"""
        df = self.df_in()
        df1 = transform_gps_to_utm(df, "EN", "lat1", "long1")
        col_expected = ['lat', 'long', 'A',  'lat1', 'long1', 'grid', 'EN']
        assert all([a in df1.columns for a in col_expected])
#         assert df['lat'].equals(df1['lat1'])

 
    def test_df_x_y_out(self):
        df = self.df_in()
        """Test DAtaFrame with additionally x_easting, y_northig output"""
        df1 = transform_gps_to_utm(df, "EN", "lat1", "long1")
        col_expected = ['lat', 'long', 'A', 'lat1', 'long1', 'grid', 'EN']
        assert all([a in df1.columns for a in col_expected])
