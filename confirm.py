import geopandas as gpd
from shapely.geometry import box
import matplotlib.pyplot as plt

# === 1. Load roads shapefile ===
roads = gpd.read_file("mongolia-251015-free.shp", layer="gis_osm_roads_free_1")

# === 2. Define Ulaanbaatar bounding box (precise coordinates) ===
ub_bbox = box(106.81, 47.88, 107.01, 47.96)

# === 3. Filter roads that intersect with Ulaanbaatar area ===
roads = roads[roads.intersects(ub_bbox)]
print("Ulaanbaatar roads:", len(roads))

# Optional: visualize just to confirm
roads.plot(color="gray", linewidth=0.5)
plt.title("Ulaanbaatar Road Network (Filtered)")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()