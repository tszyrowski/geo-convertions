"""
Created on 14 Sep 2019
"""
from shapely.geometry import LineString, Point
from bokeh.plotting import figure
from offset.shapely_ploters import plot_line, plot_points
from bokeh.io.showing import show
from offset.move_point_along import layback_point
from offset.apply_side_offset import shift_points


def create_offset_iter(points, layback, offset):
    """Create offset/layback iteratively

    Params:
        points (array[points,]): sample points taken along GPS path
        layback (float): shift in backwards direction
                        (positve - back, negative - front)
        offset (float): side offset
                        (positve - right, negative - left)
    Return:
        points_shftd (array[shapely.Point(points),]):
                new points after shift
    """
    # TODO: Correct tight inside corners.
    #       The offset still suffer crossing problem which occurs
    #       When the offset is on the inside of very tight corner.
    #       The path then crosses itself and cause fail, resulting in the error
    #       ValueError: The first input geometry is empty

    # Addjast layback direction
    if layback > 0:
        direction = 'back'
    elif layback < 0:
        direction = "front"
    else:
        layback = 0.001
        direction = "back"
    layback = abs(layback)

    # Adjust offset side
    if offset > 0:
        side = "right"
    elif offset < 0:
        side = "left"
    else:
        offset = 0.001
        side = "right"
    offset = abs(offset)

    # Initialise
    points_shftd = [points[0], ]     # Take first point without layback/offset
    slider = [points[0], ]

    # Main iterate
    for point in points[1:]:
        slider.append(point)        # take new point append sliding window
        slide_off = shift_points(slider, offset, side)
        line = LineString(slide_off)

        if line.length > layback:
            point_shftd = layback_point(line, layback, direction)
            points_shftd.append(point_shftd)
        else:
            points_shftd.append(Point(line.coords[-1]))

        # remove last point only if sliding window is longer than layback
        try:
            new_slider = slider.copy()
#             print("slide_off ", len(slide_off), slide_off)
            new_slider.pop(0)
            print("len(new_slider) ", len(new_slider))
            if LineString(new_slider).length > layback:
                print('poped')
                slider = new_slider
        except Exception as e:
            print(e)
            pass
    return points_shftd


if __name__ == '__main__':

    # -------------------------------------------------------------------------
    # VISUAL TEST 1
    line_in = LineString([(-1, 1), (-.5, 1.1), (0, 0.9), (0.5, 0.8), (1, 0.7),
                          (1.5, 0.8), (2, 1), (2.5, 1.2), (3, 1.3), (3.5, 1.1),
                          (4, 0.9), (4.5, 1), (5, 0.9), (5.5, 0.8), (6, 1)])

    points = [Point(x, y) for (x, y) in line_in.coords]
    points_shftd_right = create_offset_iter(points, layback=1.2, offset=0.7)
    points_shftd_left = create_offset_iter(points, layback=1.2, offset=-0.7)
    points_shftd_null_lay_left = create_offset_iter(points,
                                                    layback=0,
                                                    offset=-0.7)
    points_shftd_null_lay_right = create_offset_iter(points,
                                                     layback=0,
                                                     offset=0.7)
    points_shftd_null_off = create_offset_iter(points, layback=1.2, offset=0)

    print("input length: {}, right: {}, left: {}".
          format(len(points), len(points_shftd_right), len(points_shftd_left)))
    fig = figure(title="plotting offset iter VISUAL TEST 1", match_aspect=True)

    fig = plot_line(line_in, fig)
    fig = plot_points(points, fig, color="black")
    fig = plot_points(points_shftd_right, fig, color="red")
    fig = plot_points(points_shftd_left, fig, color="green")
    fig = plot_points(points_shftd_null_lay_left, fig, color="darkorange")
    fig = plot_points(points_shftd_null_lay_right, fig, color="orange")
    fig = plot_points(points_shftd_null_off, fig, color="violet")

    show(fig)
    # -------------------------------------------------------------------------
    # VISUAL TEST 2
    import numpy as np

    def make_points():
        """Create path crossing each itself."""
        x0 = np.arange(0, np.pi*2, 0.5)
        y1 = np.sin(x0)
        y2 = np.sin(x0)*(-1)
        # lines crossing each other
        xx = np.concatenate([x0, x0[::-1]])
        yy = np.concatenate([y1, y2])
        points = [Point(x, y) for (x, y) in zip(xx, yy)]
        return points

    points = make_points()
    points_shftd_right = create_offset_iter(points, layback=1.2, offset=0.7)
#     points_shftd_left = create_offset_iter(points, layback=1.2, offset=-0.7)
#     points_shftd_null_lay_left = create_offset_iter(points,
#                                                     layback=0,
#                                                     offset=-0.7)
    points_shftd_null_lay_right = create_offset_iter(points,
                                                     layback=0,
                                                     offset=0.7)
    points_shftd_null_off = create_offset_iter(points, layback=1.2, offset=0)

    print("input length: {}, right: {}, left: {}".
          format(len(points), len(points_shftd_right), len(points_shftd_left)))
    fig = figure(title="plotting offset iter VISUAL TEST 2", match_aspect=True)

    fig = plot_line(LineString(points), fig)
    fig = plot_points(points, fig, color="black")
    fig = plot_points(points_shftd_right, fig, color="red")
#     fig = plot_points(points_shftd_left, fig, color="green")
#     fig = plot_points(points_shftd_null_lay_left, fig, color="darkorange")
    fig = plot_points(points_shftd_null_lay_right, fig, color="orange")
    fig = plot_points(points_shftd_null_off, fig, color="violet")

    show(fig)
