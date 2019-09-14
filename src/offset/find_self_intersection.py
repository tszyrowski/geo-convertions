"""
 Created on 4 Sep 2019
"""
import numpy
from shapely.geometry import LineString, Point
from shapely.ops import split

complex_line = LineString([(1,-1), (-1, -1), (1, 1), (1, 0), (-1, 0), (-1,1), (1,0)])

# initial, non-result
intersection = None

# fraction of total distance at which we'll split the line
for split1 in numpy.arange(0.1, 1, 0.1):

    full_len = complex_line.length
    split_len = full_len * split1

    # endpoint = False to make sure we don't get a false-positive
    # at the split point
    first = LineString([
        complex_line.interpolate(d)
        for d in numpy.linspace(0, split_len, num=25, endpoint=False)
    ])

    second = LineString([
        complex_line.interpolate(d)
        for d in numpy.linspace(split_len, full_len, num=25)
    ])

    if first.intersects(second):
        intersection = first.intersection(second)
        break

print(intersection)

pr = Point(1,1)
# split2 = split(complex_line, complex_line)
print(complex_line.is_simple)