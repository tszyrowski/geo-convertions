"""
 Created on 6 Sep 2019
 
 set of plotting utilities for shapely geometries, mainly points and linestrings
"""
from shapely.geometry import Point, LineString, MultiLineString
from bokeh.plotting import figure
from bokeh.io import show

cmp = ('aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure', 'beige',
       'bisque', 'black', 'blanchedalmond', 'blue', 'blueviolet', 'brown',
       'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral',
       'cornflowerblue', 'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan',
       'darkgoldenrod', 'darkgray', 'darkgreen', 'darkgrey', 'darkkhaki',
       'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred',
       'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray',
       'darkslategrey', 'darkturquoise', 'darkviolet', 'deeppink',
       'deepskyblue', 'dimgray', 'dimgrey', 'dodgerblue', 'firebrick',
       'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro', 'ghostwhite',
       'gold', 'goldenrod', 'gray', 'green', 'greenyellow', 'grey', 'honeydew',
       'hotpink', 'indianred', 'indigo', 'ivory', 'khaki', 'lavender',
       'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral',
       'lightcyan', 'lightgoldenrodyellow', 'lightgray', 'lightgreen',
       'lightgrey', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue',
       'lightslategray', 'lightslategrey', 'lightsteelblue', 'lightyellow',
       'lime', 'limegreen', 'linen', 'magenta', 'maroon', 'mediumaquamarine',
       'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen',
       'mediumslateblue', 'mediumspringgreen', 'mediumturquoise',
       'mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose', 'moccasin',
       'navajowhite', 'navy', 'oldlace', 'olive', 'olivedrab', 'orange',
       'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise',
       'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink', 'plum',
       'powderblue', 'purple', 'red', 'rosybrown', 'royalblue', 'saddlebrown',
       'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver',
       'skyblue', 'slateblue', 'slategray', 'slategrey', 'snow', 'springgreen',
       'steelblue', 'tan', 'teal', 'thistle', 'tomato', 'turquoise', 'violet',
       'wheat', 'white', 'whitesmoke', 'yellow', 'yellowgreen')

def plot_points(points, fig=None, color=None):
    """Function takes array of shapely points, create to list of x, y and plots points on a figure."""
    #TODO: check for different input for point (list of coords, single point ..)
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
        col = 0
        if not color:
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