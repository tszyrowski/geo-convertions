"""
 based on shapely docs:
 https://shapely.readthedocs.io/en/stable/manual.html
"""

from shapely.geometry import MultiPoint
from shapely.ops import triangulate

from matplotlib import pyplot
from descartes.patch import PolygonPatch
BLUE = 'blue'
GRAY = 'gray'

points = MultiPoint([(0, 0), (1, 1), (0, 2), (2, 2), (3, 1), (1, 0)])
triangles = triangulate(points)

fig = pyplot.figure(1, dpi=90)
fig.set_frameon(True)
ax = fig.add_subplot(111)

for triangle in triangles:
    patch = PolygonPatch(triangle, facecolor=BLUE, edgecolor=BLUE, alpha=0.5, zorder=2)
    ax.add_patch(patch)

for point in points:
    pyplot.plot(point.x, point.y, 'o', color=GRAY)

pyplot.xlim(-0.5, 3.5)
pyplot.ylim(-0.5, 2.5)
pyplot.show()
