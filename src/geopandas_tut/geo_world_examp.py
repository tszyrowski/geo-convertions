"""
 Created on 31 Aug 2019
"""
import geopandas
import matplotlib.pyplot as plt

world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
print(world.crs)
# fig = plt.figure(1, dpi=90)
# ax = fig.add_subplot(111)

world = world[(world.name != "Antarctica") & (world.name != "Fr. S. Antarctic Lands")]
print(world.head())
world = world.to_crs({'init': 'epsg:3395'}) # world.to_crs(epsg=3395) would also work
print(world.head())
print(world.crs)
fig = plt.figure(1, dpi=90)
ax = fig.add_subplot(111)
world.plot(ax=ax)
plt.show()