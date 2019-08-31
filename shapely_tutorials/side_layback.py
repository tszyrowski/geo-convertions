"""
 Created on 30 Aug 2019
 
 The module experiments with adding layback to the side of the path
"""

import numpy as np
from shapely.geometry import Point, mapping, shape
from bokeh.io import output_file
from bokeh.plotting import figure, show
from bokeh.palettes import Category10 as colPalette
from shapely.geometry.linestring import LineString
from bokeh.models.sources import ColumnDataSource

print(type(colPalette))

output_file('shapely_plots.html',            title="shapely plots")

cities = [{'lat': '50.37', 'lon': '-4.13', 'name': 'Plymouth'},
          {'lat': '51.50', 'lon': '-2.72', 'name': 'Bristol'}, 
          {'lat': '50.88', 'lon': '-1.38', 'name': 'Southampton'},
          {'lat': '51.50', 'lon': '0.0', 'name': 'London'}]

x1 = np.arange(0, np.pi*2, 0.5)*-1
x2 = np.arange(0, np.pi*2, 0.1)*-1

ys = np.sin(x1)+51
yc = np.cos(x2)+51


def make_geom_points(points):
    geom = []
    for d in points:
        geom.append(Point(float(d['lon']), float(d['lat'])))
    return geom

def make_geom_sin(x, y):
    geom = []
    for d in range(len(x)):
        geom.append(Point(x[d], y[d]))
    return  geom

def make_line(x, y):
    print("in x of lenght:{} :{}".format(len(x), x),"\nin y of length {}:{}".format(len(y),y))
    line = LineString(zip(x,y))
    for point in line.coords:
        print(point)
    return line

def vis_geom_points(geom):
    fig = figure(title="Basic plot")
    N=0
    cmap = [ "red",'blue',"black","orange","green","brown"]
    for g in geom:
        x = [pont.x for pont in g]
        y = [pont.y for pont in g]
        fig.circle(x=x, y=y,color=cmap[N], legend=str(N))
        N += 1
    line = make_line(x2, yc)
    x, y = zip(*line.coords)
    fig.line(x, y,color=cmap[N], legend=str(N))

    
    N+=1
    line_p1 = line.parallel_offset(0.3, 'right', resolution=100)#, resolution, join_style, mitre_limit)
    xp1, yp1 = zip(*line_p1.coords)
    fig.line(xp1, yp1,color=cmap[N], legend=str(N))
    fig.circle(xp1, yp1, color="yellow")
    
    N+=1
    line_p2 = line.parallel_offset(0.3, 'left')#, resolution, join_style, mitre_limit)
    xp2, yp2 = zip(*line_p2.coords)
    fig.line(xp2, yp2,color=cmap[N], legend=str(N))
    fig.circle(xp2, yp2, color="yellow")
    
    return fig

def vis_closed_line():
    """showing parallel lne to closed line"""
    N=0
    cmap = [ "red",'blue',"orange","black","green","brown"]
    
    xx = np.arange(0, np.pi*2, 0.5)
    y1 = np.sin(xx)
    y2 = np.sin(xx)*(-1)
#     y2[-1]=y1[-1]
    print(len(xx), len(y1), len(y2))
    x = np.concatenate([xx, xx[::-1]])
    y = np.concatenate([y1, y2])
    
    fig = figure(title="closed plot")
    fig.line(x,y, color=cmap[N], legend=str(N))
    fig.circle(x, y, color="yellow")
    
    line = line = make_line(x, y)
    print('line.is_simple: {} line.line.is_closed: {}, line.is_valid: {}'.format(line.is_simple, 
                                                              line.is_closed,
                                                              line.is_valid))
    N+=1
    line_p1 = line.parallel_offset(0.3, 'right', resolution=100)#, resolution, join_style, mitre_limit)
    for single_line in line_p1.geoms:
        print(single_line)
        xp1, yp1 = zip(*single_line.coords)
        fig.line(xp1, yp1,color=cmap[N], legend=str(N))
        fig.circle(xp1, yp1, color="yellow")
      
    N+=1
    line_p1 = line.parallel_offset(0.3, 'left', resolution=100)#, resolution, join_style, mitre_limit)
    for single_line in line_p1.geoms:
        print(single_line)
        xp1, yp1 = zip(*single_line.coords)
        fig.line(xp1, yp1,color=cmap[N], legend=str(N))
        fig.circle(xp1, yp1, color="yellow")
    
    return fig

def main_vis(fig):
    show(fig)

if __name__ == '__main__':
#     geom1 = make_geom_points(points = cities)
#     geom2 = make_geom_sin(x1, ys)
#     geom3 = make_geom_sin(x2, yc)
#     geom4 = make_line(x2, yc)
#     print('geom4 length: ', geom4.length)
#     print(geom4)
# #     for g_p in geom1:
# #         print(g_p.geom_type)
#     print(geom1[0].distance(geom1[1]))
    
#     for point in geom1:
#         print(point)
    
#     fig = vis_geom_points([geom1, geom2, geom3])
    fig = vis_closed_line()
    main_vis(fig)