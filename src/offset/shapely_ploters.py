"""
 Created on 6 Sep 2019
 
 set of plotting utilities for shapely geometries, mainly points and linestrings
"""
from shapely.geometry import Point, LineString, MultiLineString
from bokeh.plotting import figure
from bokeh.io import show

def plot_points(points, fig=None, color=None):
    """Function takes array of shapely points, create to list of x, y and plots points on a figure."""
    if not color:
        color="orange"
    if not fig:
        fig = figure(title="points plot")
    x = [point.x for point in points]
    y = [point.y for point in points]
    fig.circle(x,y, color=color)
    return fig

def plot_line(line_ob, fig=None, color=None):
    """Function takes shapely.linestring extract coordinates and plot on a figure."""

    if not fig:
        fig = figure(title="linestring plot")

    def _plot_line(ob, fig, color):
        if not color:
            col = 0
            cmp = ['blue', 'red', 'green', 'gray', 'yellow']  
            color = cmp[col]
        x, y = ob.xy
        x = x.tolist()
        y = y.tolist()
        fig.line(x, y, color=color)
    if type(line_ob) is LineString:
        _plot_line(line_ob, fig, color)
    elif type(line_ob) is MultiLineString:
        if not color:
            col = 0
            cmp = ['blue', 'red', 'green', 'gray', 'yellow']  
            color = cmp[col]
        for ob in line_ob:
            _plot_line(ob, fig, color)
            col += 1
    return fig 


if __name__ == '__main__':
    l1 = LineString([(1,-1), (-1, -1), (1, 1), (1, 0), (-1, 0), (-1,1), (1,0)])
    l2 = LineString([(2, 0), (2, -1), (-1, -1), (1, 1), (-1, 1), (.5, -.5), (2,-2)])
    ml1 = MultiLineString([((0, 0), (-1, -2)), ((-1, 0), (0, -2))])
    ml2 = MultiLineString([((2, 0), (1, -2)), ((1, 0), (2, -2))])
    points = (Point(0,0), Point(1,1))
    
    fig = figure(title="plotting utilietes")
    
    fig = plot_line(l1, fig)
    fig = plot_line(l2, fig, 'red')
    fig = plot_line(ml1, fig, 'green')
    fig = plot_line(ml2, fig)
    fig = plot_points(points, fig)
    
    show(fig)