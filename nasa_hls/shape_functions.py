import zipfile
import requests
import geopandas as gp
import io
from geopandas.tools import sjoin


def download_test_tiles():

    url = "https://hls.gsfc.nasa.gov/wp-content/uploads/2018/10/hls_s2_tiles.zip"
    local_path = "ignored/test_tiles/"

    print(f"Downloading shapefile from url {url}...")
    request = requests.get(url)
    zip = zipfile.ZipFile(io.BytesIO(request.content))
    print("DONE")
    zip.extractall(path=local_path)

    path_to_test_tiles = local_path + "hls_s2_tiles.shp"

    return path_to_test_tiles


path_to_user_poly = input("enter the complete path to the shapefile of your working area")
path_to_user_poly = "/home/aleko-kon/projects/geo419/nasa-hls/ignored/user_shape/dummy_region.shp"

user_poly = gp.GeoDataFrame.from_file(path_to_user_poly)
test_tiles = gp.GeoDataFrame.from_file(download_test_tiles())
intersections= gp.sjoin(user_poly, test_tiles, how="inner", op='intersects')
intersections
