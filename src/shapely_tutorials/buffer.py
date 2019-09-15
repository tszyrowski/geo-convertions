"""
 based on shapely docs:
 https://shapely.readthedocs.io/en/stable/manual.html
"""

from matplotlib import pyplot
from shapely.geometry import LineString
from descartes import PolygonPatch

cap_stl = 2 # parameter how the end point is presented. {1: round, 2: flat, 3:square
join_stl = 3 # parameter {1: round, 2: mitre, 3: bevel}

def plot_line(ax, ob):
    x, y = ob.xy
    ax.plot(x, y, color='gray', linewidth=3, solid_capstyle='round', zorder=1)

line = LineString([(0, 0), (1, 1), (0, 3), (2, 3), (3, 1), (3, -1),(2, -1)])

fig = pyplot.figure(1, dpi=90)

# Plot buffered line
ax = fig.add_subplot(121)
plot_line(ax, line)


dilated = line.buffer(0.5, cap_style=cap_stl, join_style=join_stl)
print('dilated type is {} and it is :{}'.format(type(dilated), dilated))
patch1 = PolygonPatch(dilated, fc='blue', ec='blue', alpha=0.5, zorder=2)
ax.add_patch(patch1)
# plot_line(ax, dilated)

ax.set_title('a) dilation, cap_style={}'.format(cap_stl))
xrange = [-2, 5]
yrange = [-2, 4]
ax.set_xlim(*xrange)
ax.set_ylim(*yrange)
ax.set_aspect(1)

# Plot negative buffer 2
ax = fig.add_subplot(122)

patch2a = PolygonPatch(dilated, fc='gray', ec='gray', alpha=0.5, zorder=1)
ax.add_patch(patch2a)

eroded = dilated.buffer(-0.3)

# GeoJSON-like data works as well

polygon = eroded.__geo_interface__
# >>> geo['type']
# 'Polygon'
# >>> geo['coordinates'][0][:2]
# ((0.50502525316941682, 0.78786796564403572), (0.5247963548222736, 0.8096820147509064))
patch2b = PolygonPatch(polygon, fc='blue', ec='blue', alpha=0.5, zorder=2)
ax.add_patch(patch2b)

ax.set_title('b) erosion, join_style={}'.format(join_stl))

xrange = [-2, 5]
yrange = [-2, 4]
ax.set_xlim(*xrange)
ax.set_ylim(*yrange)
ax.set_aspect(1)

pyplot.show()

