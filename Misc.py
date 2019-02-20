# Name:                                             Renacin Matadeen
# Date:                                               02/20/2019
# Title                                         Understanding GeoPandas
#
# ----------------------------------------------------------------------------------------------------------------------
import geopandas as gpd
# ----------------------------------------------------------------------------------------------------------------------

# Import Shapefile
shp_path = r"/Users/renacinmatadeen/Downloads/Schools/Schools.shp"
shp_data = gpd.read_file(shp_path)

# Print Columns & General Info
print(shp_data.info(), "\n")

# Print CRS
print(shp_data.crs, "\n")

# Print Specific Column
print(shp_data["TYPE"])
