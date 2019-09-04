"""
 Created on 31 Aug 2019
"""
import pandas as pd
import utm.conversion as convert
import numpy as np
from shapely.geometry import Point


def transform_gps_to_utm(df, lat_col, long_col, out_point_col,
                         inplace=True, x_y_out=False):
    """Transform Latitude and Longitude to UTM x, y , grid
    
    Params:
        df (pandas.DataFrame): with Longitude and Latitude coordinates
        lat_col (str): Name of the column with latitude
        long_col (str): Name of the column with longitude
        out_point_col (str): Column name of new Shapely point of x, y coordinate
        inplace (bool): True- replace existing, 
                        False- create new one 
        x_y_out (bool): True- create new columns for x, y. 
                        False- output only Point(x, y) column
                        
    Returns: 
        df
    """

    def _convert(x):
        """Helper for single convertions"""
        return convert.from_latlon(x[0], x[1])
    
    if not inplace:
        out_point_col = '{}_new'.format(out_point_col)
    
    x_col, y_col, grid_no_col, grid_letter = zip(*df[[lat_col, long_col]].
                                                 apply(lambda x: _convert(x), 
                                                       axis=1)) 
    
    if x_y_out:
        df['x_{}'.format(out_point_col)] = x_col
        df['y_{}'.format(out_point_col)] = y_col
    
    # update grid columns
    df['grid'] = ['{};{}'.format(no_col, let) for no_col, let in 
                  zip(grid_no_col, grid_letter)]
    
    # Create columnd with Shapely Point  in 
    df[out_point_col] = [Point(x, y) for x, y in zip(x_col, y_col)]
    
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
                            'A' : np.random.randn(10)})
        expext_x_y = [Point(418359.60059718, 5582203.060540936),
                      Point(418360.5639061191, 5582196.372802922),
                      Point(418361.6566844113, 5582193.464354321),
                      Point(418362.140570124, 5582192.567167133),
                      Point(418363.0372532262, 5582190.773890653),
                      Point(418363.4586353551, 5582190.433740599),
                      Point(418363.5819265808, 5582189.208478752),
                      Point(418364.6379578019, 5582188.524885572),
                      Point(418365.4199352756, 5582188.512810587),
                      Point(418366.486268195, 5582188.496344883)]
        return df, expext_x_y

    def test_df(self):
        """Test DataFrame usual case"""
        df, _ = self.df_in()
        df1 = transform_gps_to_utm(df, "lat", "long", "EN")
        col_expected = ['lat', 'long', 'A', 'grid', 'EN']
        assert all([a in df1.columns for a in col_expected])

    def test_df_x_y_out(self):
        df, _ = self.df_in()
        """Test DAtaFrame with additionally x_easting, y_northig output"""
        df1 = transform_gps_to_utm(df, "lat", "long", "EN", x_y_out=True)
        col_expected = ['lat', 'long', 'A', 'x_EN', 'y_EN', 'grid', 'EN']
        assert all([a in df1.columns for a in col_expected])
