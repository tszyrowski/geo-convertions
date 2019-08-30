"""
 Created on 30 Aug 2019
 
 The module experiments with adding layback to the side of the path
"""


from shapely.geometry import Point, mapping, shape
from bokeh.io import output_file
from bokeh.plotting import figure, show

output_file('shapely_plots.html',            title="shapely plots")

cities = [{'lat': '50.37', 'lon': '-4.13', 'name': 'Plymouth'},
          {'lat': '51.50', 'lon': '-2.72', 'name': 'Bristol'}, 
          {'lat': '50.88', 'lon': '-1.38', 'name': 'Southampton'},
          {'lat': '51.50', 'lon': '0.0', 'name': 'London'}]

def make_geom_points(points):
    geom = []
    for d in points:
        geom.append(Point(float(d['lon']), float(d['lat'])))
    return geom

def vis_geom_points(geom):
    fig = figure(title="Basic plot")
    x = [pont.x for pont in geom]
    y = [pont.y for pont in geom]
    print(x, y)
    fig.circle(x=x, y=y)
    show(fig)

if __name__ == '__main__':
    geom = make_geom_points(points = cities)
    for g_p in geom:
        print(g_p.geom_type)
    print(geom[0].distance(geom[1]))
    
    for point in geom:
        print(point)
    
    vis_geom_points(geom)