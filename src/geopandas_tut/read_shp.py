"""
Created on 20 Sep 2019
"""
import geopandas as gpd
filepath1 = r"C:\Users\tszyrowski\SubseaCables\sct_job_projects\Sylt_02_08_2019\wetransfer-ee352a\Sylt single channel_DR\Sylt single channel\AC1_SEG_A_R104_TO_BMH_LINE.shp"
filepath2 = r"C:\Users\tszyrowski\SubseaCables\sct_job_projects\Sylt_02_08_2019\wetransfer-ee352a\Sylt single channel_DR\Sylt single channel\AC1_SEG_A_R104_TO_BMH.shp"
shapefile = gpd.read_file(filepath2)
print(shapefile)

import fiona
shape = fiona.open(filepath2)
print(shape.__dir__())

#first feature of the shapefile
# first = shape.next()

# print(shape) # (GeoJSON format)
