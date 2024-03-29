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
c = a.union(b)
patchc = PolygonPatch(c, fc='blue', ec='blue', alpha=0.5, zorder=2)
ax.add_patch(patchc)

ax.set_title('a.union(b)')

xrange = [-1, 4]
yrange = [-1, 3]
ax.set_xlim(*xrange)
ax.set_ylim(*yrange)
ax.set_aspect(1)

def plot_line(ax, ob, color='gray'):
    x, y = ob.xy
    ax.plot(x, y, color, linewidth=3, solid_capstyle='round', zorder=1)

#2
ax = fig.add_subplot(122)

plot_line(ax, a.exterior)
plot_line(ax, b.exterior)

u = a.exterior.union(b.exterior)
if u.geom_type in ['LineString', 'LinearRing', 'Point']:
    plot_line(ax, u, color='blue')
elif u.geom_type is 'MultiLineString':
    for p in u:
        plot_line(ax, p, color='blue')

ax.set_title('a.boundary.union(b.boundary)')

xrange = [-1, 4]
yrange = [-1, 3]
ax.set_xlim(*xrange)
ax.set_ylim(*yrange)
ax.set_aspect(1)

pyplot.show()

