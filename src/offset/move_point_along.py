"""
Created on 14 Sep 2019

Backword layback needs to be calculated as a shoft along the line
"""
from shapely.geometry.linestring import LineString
from offset.apply_side_offset import shift_linestring
from bokeh.plotting import figure
from bokeh.io.showing import show
from offset.shapely_ploters import plot_line, plot_points
from shapely.geometry.point import Point


def reverse_linestring(line_in):
    """Return the same linestring but in reversed order
    Params:
        line_in: shapely.linestring to be reversed
    Returns:
        line_rev: shapely.linestring
    """
    line_rev = LineString(line_in.coords[::-1])
    return line_rev

def layback_point(line_in, layback_dist, direction="back"):
    """Move a point by distance along a line.

    The point is moved backwords from the end point of the linestring if
    direction="back"
    is moved forward from the starting point of the linestring if
    direction="front"

    If length of the linestring is not shorter than layback
    Point will be moved to the end of the linestring
    In other words the point can move further than the linestring
    It has its importance on the beginning of the survey line

    Params:
        line_in: linestring along which the point will be moved
        layback_dist: amount of distance to be applied to the shift
        direction: back - backwords, front - forward
    Returns:
        point_shftd: coordinates of the point after shift
    """
    if direction.lower() == "back":
        line_in1 = reverse_linestring(line_in)
    elif direction.lower() == "front":
        line_in1 = line_in
    else: raise ValueError("direction not understood")

    point_shftd = line_in1.interpolate(layback_dist)
    return point_shftd


if __name__ == "__main__":
    
    line_in_org = LineString([(-1, 1), (-.5, 1.1), (0, 0.9), (0.5, 0.8),
                          (1, 0.7), (1.5, 0.8), (2, 1)])
    line_in = shift_linestring(line_in_org, side='left')

    point = Point(line_in.coords[-1])
    print(point)

    point_shftd1 = layback_point(line_in, layback_dist=1)
    point_shftd2 = layback_point(line_in, layback_dist=2)
    point_shftd4 = layback_point(line_in, layback_dist=4)
    print(point_shftd1)
    fig = figure(title="plotting shift")

    fig = plot_line(line_in, fig)
    fig = plot_points([point,], fig, color="red")
    fig = plot_points([point_shftd1,point_shftd2, point_shftd4],
                      fig, color="black")
    fig = plot_points([layback_point(line_in,
                                     layback_dist=2.5,
                                     direction="Front")],
                       fig, color='orange')
    fig = plot_points([layback_point(line_in,
                                     layback_dist=2.5,
                                     direction="Back")],
                      fig, color='violet')
    fig = plot_points([layback_point(line_in,
                                     layback_dist=4.5,
                                     direction="BACK")],
                      fig, color="gold")

    show(fig)
