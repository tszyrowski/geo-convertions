"""
 from shapely docs:
 https://shapely.readthedocs.io/en/stable/manual.html
"""

from matplotlib import pyplot
from shapely.geometry import Point
from descartes import PolygonPatch


fig = pyplot.figure(1, dpi=90)

a = Point(1, 1).buffer(1.5)
b = Point(2, 1).buffer(1.5)

# 1
ax = fig.add_subplot(121)

patch1 = PolygonPatch(a, fc='gray', ec='gray', alpha=0.2, zorder=1)
ax.add_patch(patch1)
patch2 = PolygonPatch(b, fc='gray', ec='gray', alpha=0.2, zorder=1)
ax.add_patch(patch2)
c = a.intersection(b)
patchc = PolygonPatch(c, fc='blue', ec='blue', alpha=0.5, zorder=2)
ax.add_patch(patchc)

ax.set_title('a.intersection(b)')

xrange = [-1, 4]
yrange = [-1, 3]
ax.set_xlim(*xrange)
ax.set_ylim(*yrange)
ax.set_aspect(1)

#2
ax = fig.add_subplot(122)

patch1 = PolygonPatch(a, fc='gray', ec='gray', alpha=0.2, zorder=1)
ax.add_patch(patch1)
patch2 = PolygonPatch(b, fc='gray', ec='gray', alpha=0.2, zorder=1)
ax.add_patch(patch2)
c = a.symmetric_difference(b)

if c.geom_type == 'Polygon':
    patchc = PolygonPatch(c, fc='blue', ec='blue', alpha=0.5, zorder=2)
    ax.add_patch(patchc)
elif c.geom_type == 'MultiPolygon':
    for p in c:
        patchp = PolygonPatch(p, fc='blue', ec='blue', alpha=0.5, zorder=2)
        ax.add_patch(patchp)

ax.set_title('a.symmetric_difference(b)')

xrange = [-1, 4]
yrange = [-1, 3]
ax.set_xlim(*xrange)
ax.set_ylim(*yrange)
ax.set_aspect(1)

pyplot.show()

