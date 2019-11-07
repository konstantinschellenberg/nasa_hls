from pathlib import Path
import geopandas as gp
import nasa_hls


def get_required_tiles_from_utm(path_to_utm_file="/home/aleko-kon/projects/geo419/nasa-hls/ignored/UTM_tiles.kml",
                                user_shape="/home/aleko-kon/projects/geo419/nasa-hls/ignored/user_shape/dummy_region.shp"):
    """
    :param path_to_utm_file: requires the path where the Nasa's world-covering UTM.kml file is stored.
    Do this manually by calling function 'download_utm_tiles'.

    :return: list of tile name [str of 5 digits starting with two numbers] which geographically intersect the user
    shape and the UTM tiles.
    """

    path_to_utm_file = Path(path_to_utm_file)
    Path.exists(path_to_utm_file)
    path_to_user_polygon = Path(user_shape)

    # Enable fiona driver, then read kml-file
    gp.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'
    UTM_tiles = gp.read_file(path_to_utm_file, driver='KML')

    # convert user_polygon into Gdf
    user_polygon = gp.GeoDataFrame.from_file(path_to_user_polygon)

    # perform intersection
    intersections = gp.sjoin(user_polygon, UTM_tiles, how="inner", op='intersects')

    # write UTM-codes in lis
    tiles = intersections["Name"].tolist()
    print(tiles)

    return tiles


def get_available_datasets_from_tiles(products=["S30"],
                                      years=[2018],
                                      user_shape="/home/aleko-kon/projects/geo419/nasa-hls/ignored/user_shape/dummy_region_europe.shp"):
    # retrieve required tiles from the function above
    tiles = get_required_tiles_from_utm(user_shape=user_shape)
    datasets = nasa_hls.get_available_datasets(products=products, years=years, tiles=tiles, return_list=True)

    return datasets
