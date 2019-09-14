"""
 Created on 4 Sep 2019
"""
from shapely.geometry import *

paths = MultiLineString([
    [ (0, -1), (0, 1), (-1, 1), (-1, 0), (3,0) ],
    [(1, -1), (1, +1)],])
display(paths)

parallels = []
for offset in [-.2, .0, .2]:
    for line in paths.geoms:
        parallels.append(line.parallel_offset(offset))       
display(GeometryCollection(parallels))