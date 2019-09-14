"""
 based on shapely docs:
 https://shapely.readthedocs.io/en/stable/manual.html
"""

from matplotlib import pyplot
from shapely.geometry import Point
from shapely.ops import cascaded_union
from descartes import PolygonPatch

BLUE = 'blue'
GRAY = 'gray'

polygons = [Point(i, 0).buffer(0.7) for i in range(5)]

fig = pyplot.figure(1, dpi=90)

# 1
ax = fig.add_subplot(121)

for ob in polygons:
    p = PolygonPatch(ob, fc=GRAY, ec=GRAY, alpha=0.5, zorder=1)
    ax.add_patch(p)

ax.set_title('a) polygons')

xrange = [-2, 6]
yrange = [-2, 2]
ax.set_xlim(*xrange)
ax.set_ylim(*yrange)
ax.set_aspect(1)

#2
ax = fig.add_subplot(122)

u = cascaded_union(polygons)
patch2b = PolygonPatch(u, fc=BLUE, ec=BLUE, alpha=0.5, zorder=2)
ax.add_patch(patch2b)

ax.set_title('b) union')

xrange = [-2, 6]
yrange = [-2, 2]
ax.set_xlim(*xrange)
ax.set_ylim(*yrange)
ax.set_aspect(1)

pyplot.show()

