import shapely
import numpy as np
from bokeh.plotting import figure
from bokeh.io.showing import show
from shapely.geometry.point import Point
from shapely.geometry.linestring import LineString
from shapely.geometry.multilinestring import MultiLineString

def create_input_points():
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
        
#     in_path_points = shapely.lin
    
    return fig

def make_points():
    
    x0 = np.arange(0, np.pi*2, 0.5)
    y1 = np.sin(x0)
    y2 = np.sin(x0)*(-1)
    
    # lines crossing each other
    xx = np.concatenate([x0, x0[::-1]])
    yy = np.concatenate([y1, y2])
    
    # simple line
#     xx = x0
#     yy = y1
    
    points = [Point(x, y) for (x, y) in zip(xx, yy)]
    return points
    

def plot_points(points, fig=None):
    """Function takes array of shapely points, create to list of x, y and plots points on a figure."""
    
    if not fig:
        fig = figure(title="points plot")
    x = [point.x for point in points]
    y = [point.y for point in points]
    fig.circle(x,y, color="orange")
    return fig

def plot_line(line_ob, fig=None):
    """Function takes shapely.linestring extract coordinates and plot on a figure."""

    if not fig:
        fig = figure(title="linestring plot")  
    cmp = ['blue', 'red', 'green', 'gray', 'yellow']  
    col = 0
    def _plot_line(ob, fig):
        x, y = ob.xy
        x = x.tolist()
        y = y.tolist()
        print('x=', x,'\ny=', y)
        fig.line(x, y, color=cmp[col])
    if type(line_ob) is LineString:
        _plot_line(line_ob, fig)
    elif type(line_ob) is MultiLineString:
        for ob in line_ob:
            _plot_line(ob, fig)
    return fig 


def shift_points(points, distance = 1, side='left', resolution=16, join_style=3, mitre_limit=5.0):
    """Takes array of points, create linestring, shift the linestring and return shifted"""
    line = LineString(points)
    shift_line = line.parallel_offset(distance, side)
    print('shift_line=\n', shift_line)
    return shift_line
    
def main_vis(fig):
    show(fig)

if __name__ == '__main__':
    points = make_points()
#     fig = create_input_points()
    fig = plot_points(points)#, fig=fig)
#     fig = plot_line(LineString(points), fig)
    fig = plot_line(shift_points(points), fig)
    main_vis(fig)