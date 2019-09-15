"""
Created on 14 Sep 2019

STEP 2

The simple linestring can be shift to the right or left.

It needs to be considered that the left shift may change direction.
"""
from shapely.geometry import LineString, Point
from bokeh.plotting import figure
from bokeh.io.showing import show
from offset.shapely_ploters import plot_line, plot_points
from shapely.ops import nearest_points


def shift_linestring(line_string, distance=1, side='left',
                     resolution=16, join_style=1, mitre_limit=5.0):
    """Shift line to the side.

    Takes simple linestring - Can NOT corss itself

    Params:
        line_string: simple linestring to be shifted
        distance: amount of applied shift (usually 1 means 1 metre to the side)
        side: "right" or "left"
        resolution: number of segments to approx a 1/4 of circle around a point
        join_style: 1 (round), 2 (mitre), and 3 (bevel)
        mitre_limit: ratio of the distance from the corner
                     to the end of the mitred offset
    Return:
        linestring: nealinestring after shift
    """
    shifted_ln = line_string.parallel_offset(distance,
                                             side,
                                             resolution,
                                             join_style,
                                             mitre_limit)
    return shifted_ln


def shift_points(points, distance=1, side='left',
                 resolution=16, join_style=1, mitre_limit=5.0):
    """Takes array of points and shift them to the side.

    Create linestring, shift the linestring,
    projects points to shifted line string,
    returnes only shifted points
    """
    line_string = LineString(points)
    shftd_ln = line_string.parallel_offset(distance,
                                             side,
                                             resolution,
                                             join_style,
                                             mitre_limit)
    shifted_points = [nearest_points(shftd_ln, point)[0] for point in points]
    return shifted_points


if __name__ == '__main__':

    line_in = LineString([(-1, 1), (-.5, 1.1), (0, 0.9), (0.5, 0.8),
                          (1, 0.7), (1.5, 0.8), (2, 1), (2.5, 1.2),
                          (3, 1.3), (3.5, 1.1), (4, 0.9), ])
    line_shft_left = shift_linestring(line_in, side='left')
    line_shft_right = shift_linestring(line_in, side='right')
    line_shft_null = shift_linestring(line_shft_left, side="right")
    line_shft_lull = shift_linestring(line_shft_null, side="right")
    print("line_shft_null with {} points \nand of length {} \nis {}".
          format(len(line_shft_null.coords),
                 line_shft_null.length,
                 line_shft_null))

    # Work with points only
    points = [Point(p) for p in line_in.coords]
    shftd_points = shift_points(points)

    fig = figure(title="plotting utilietes")

    fig = plot_line(line_in, fig)
    fig = plot_line(line_shft_left, fig, 'darkorange')
    fig = plot_line(line_shft_right, fig, 'green')
    fig = plot_line(line_shft_null, fig, 'red')
    fig = plot_line(line_shft_lull, fig, 'red')

    fig = plot_points(points, fig, color="black")
    fig = plot_points(shftd_points, fig, color="black")

    show(fig)
