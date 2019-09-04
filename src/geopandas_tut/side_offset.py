"""
 Created on 1 Sep 2019
 
 Apply side offset projection to path in dataframe
 
 1. Read data frame
 2. Make x, y as easting northing
 3. Extract Shapely linestring from x, y
 4. Shift linestring right
 5. Apply projection of x, y to linestring
 6. Store new points into columns
 7. convert x, y to lat long
 8. Check outside (qgis that lat long path is shifted
"""
import geopandas_tut.read_andro_sens as ras
from geopandas_tut.transform_gps_to_utm import transform_gps_to_utm
import shapely.geometry
from shapely.geometry import Point, LineString
from shapely.ops import nearest_points, split
import matplotlib.pyplot as plt


def layback_offset(points_arr, side_distance=0, back_dist=0):
    """Project points sideway
    
    Args:
        points_arr (pd.series, numpy.ndarray): points to project
        side_distance (float): distance to the right (positive) or 
                                        to the left (negative)
                                        in metres
        back_dist (float): distance of layback to the back (positive)
                                               forward (negative)
    Returns:
        proj_arr: array of points projected
    """


    if side_distance >= 0:
        side = 'right'      # positive distance is projected to the right, 
    else: side = 'left'     # negative distance is projected to the left
    # Create line object with offset from point
    linestr = createLineGeom(points_arr)
    off_line = linestr.parallel_offset(abs(side_distance), side, join_style=1)
    # Project points into offset_line
    norm = True
    side_arr = [off_line.interpolate(off_line.project(point, normalized=norm),
                                     normalized=norm) for point in points_arr]
    #===========================================================================
#     # # TODO: Work out reversal of the coordinates. 
#     # https://github.com/Toblerity/Shapely/issues/284
#     # Part of a loop
#     new_line = generated_line.parallel_offset(distance=distance_in_m, side=side)
#     
#     if side == "right":
#         new_line = LineString([(x, y) for x, y in zip(reversed(new_line.coords.xy[0]), reversed(new_line.coords.xy[1]))])
#         generated_line = new_line
#     else:
#         generated_line = new_line
    #===========================================================================
    
    proj_arr = []
    for point in side_arr:
        norm = True
        # create to lines
        split_parts = split(off_line, point)
        first_part = split_parts[0]
        p = first_part.interpolate(back_dist)
        proj_arr.append(p)
#     proj_arr = [off_line.interpolate(back_dist,
#                                      normalized=norm) for point in side_arr]
    return proj_arr

def createLineGeom(Points):
    if all(isinstance(x, shapely.geometry.Point) for x in Points):
        return LineString(Points)
    else:
        raise 'pointList must contain shapely point object(s)'
    
def plot_line(ax, ob, color='gray'):
    """Plots geometry even if it is multiline"""
    parts = hasattr(ob, 'geoms') and ob or [ob]
    for part in parts:
        x, y = part.xy
        ax.plot(x, y, color=color, linewidth=3, solid_capstyle='round', zorder=1)

def scatter_line(ax, ob, marker='o', color='orange', zorder=2):
    """Plots geometry even if it is multiline"""
    parts = hasattr(ob, 'geoms') and ob or [ob]
    for part in parts:
        x, y = part.xy
#         print(len(x), len(y), type(part))
        ax.scatter(x, y, color=color, zorder=zorder)

def scatter_points(ax, arr, marker='*', color='black', zorder=2):
    xx = []
    yy = []
    for point in arr:
        x, y = point.xy
        xx.append(x)
        yy.append(y)
        ax.scatter(x, y, color=color, zorder=zorder)
        
    
def plot_line_coords(ax, x, y, color='#999999', zorder=2):
    ax.plot(x, y, 'o', color=color, zorder=zorder)
    
if __name__ == '__main__':
    """
    # Below is real df
    
    file = './data/sensor_path.csv'
    gdf = ras.read_from_wkt(file)
    print(gdf.columns,'\nwith {} rows'.format(len(gdf.index)), '\n', gdf.head())
    gdf = transform_gps_to_utm(gdf, 'lat', 'long', out_point_col='east_nor_xy', inplace=True, x_y_out=True)
    print(gdf.columns,'\nwith {} rows'.format(len(gdf.index)), '\n', gdf.head())
    
    # create linestring from points
    linestr = createLineGeom(gdf['east_nor_xy'])
    
    
    # 
    offset_r = layback_offset(gdf['east_nor_xy'], 3)
    print('offset_r', len(offset_r), offset_r)
    
    offset_l = layback_offset(gdf['east_nor_xy'], -3, 30)
    print('offset_l', len(offset_l), offset_l)
    
#     gdf['offset_line'] = 
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plot_line(ax, linestr)
    scatter_line(ax, linestr)
#     plot_line(ax, offset_r, color='blue')
    scatter_points(ax, offset_r, marker='x', color='blue')
#     plot_line(ax, offset_l, color='red')
    scatter_points(ax, offset_l, marker='x', color='red')
    """
    
    # Simple points
    
    points = ([Point(0, 2), Point(1,2), Point(2,2), Point(3,2), Point(4,2), Point(5,2)])
    linestr = createLineGeom(points)
    
    
    # 
    offset_r = layback_offset(points, 1, .5)
    print('offset_r', len(offset_r), offset_r)
    
#     offset_l = layback_offset(points, -2, .5)
#     print('offset_l', len(offset_l), offset_l)
    
#     gdf['offset_line'] = 
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plot_line(ax, linestr)
    scatter_line(ax, linestr)
#     plot_line(ax, offset_r, color='blue')
    scatter_points(ax, offset_r, marker='x', color='blue')
#     plot_line(ax, offset_l, color='red')
#     scatter_points(ax, offset_l, marker='x', color='red')

    plt.show()

class TestLayback_offset():
    
    def test_offset_left(self):
        points = ([Point(0, 2), Point(1,2), Point(2,2), Point(3,2), Point(4,2), Point(5,2)])
        offset = layback_offset(points, -3)
        expected = ([Point(0, 5), Point(1,5), Point(2,5), Point(3,5), Point(4,5), Point(5,5)])
        assert all(offset[x] == expected[x] for x in range(len(expected)))
        
    def test_offset_right(self):
        points = ([Point(0, 2), Point(1,2), Point(2,2), Point(3,2), Point(4,2), Point(5,2)])
        offset = layback_offset(points, 3)
        expected = ([Point(0, -1), Point(1,-1), Point(2,-1), Point(3,-1), Point(4,-1), Point(5,-1)])
        assert all(offset[x] == expected[x] for x in range(len(expected)))
                   
