import os
import urllib
from pathlib import Path
import geopandas as gp

path_data_win_konsti = os.path.join("D:", os.sep, "Geodaten", "#Jupiter", "GEO419", "data" + os.sep)
path_data_lin_konsti = os.path.join(os.path.expanduser('~'), 'Dokumente', 'nasa_hls', 'data' + os.sep)

path_data_lin_robin = os.path.join(os.path.expanduser('~'), 'python_projects', 'data', 'nasa_hls', 'hdf_tiles' + os.sep)

path_auxil = os.path.join(os.path.expanduser('~'), '.nasa_hls', '.auxdata' + os.sep)

def download_kml():
    """
    Download the necessary .kml-file
    :param dst: desired destination
    :return: destination of the .kml-file
    """

    path = path_auxil + "utm.kml"

    if not os.path.exists(path):
        print(f"Creating new file in", path)
        src = (
            "https://hls.gsfc.nasa.gov/wp-content/uploads/2016/03/S2A_OPER_GIP_TILPAR_MPC__"
            "20151209T095117_V20150622T000000_21000101T000000_B00.kml")
        urllib.request.urlretrieve(src, path)
    else:
        print(f"File already downloaded to", path)
    return path


def get_required_tiles_from_utm(path_to_utm_file = "/home/robin/.nasa_hls/.auxdata/utm.kml",
                                user_shape = "/home/robin/python_projects/data/nasa_hls/test_shape/dummy_region.shp"):

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

    # if not proj is crs WGS84:
    # ändere

    # convert user_polygon into Gdf
    user_polygon = gp.GeoDataFrame.from_file(path_to_user_polygon)

    # perform intersection
    intersections = gp.sjoin(user_polygon, UTM_tiles, how="inner", op='intersects')

    # write UTM-codes in lis
    tiles = intersections["Name"].tolist()
    print(tiles)

    return tiles



def make_tiles_dataset()
    """
    :param: shape, date, start_date, end_date, product
    :return: dataset(s). contains date specific tiles in the spatial extent of the input shape.
    can be ingested by download_batch. Returns list when time span is specified

    is
    1. df -> when there is only a single date
    2. list of df -> when time span is specified (iterable)
    """

    download_kml() -> pfad
    get_required_tiles_from_utm() -> list(tiles_no)
    get_available_datasets_from_tiles(products=, years=)
    extract_date(date=, start_date=, end_date=)

    return datasets # welches heruntergeladen werden soll -> download_tiles()
#
def download_tiles():
    """
    Download

    :param: datasets, dstdir

    :returns: none
    """


    get_tiles()
    dstdir = [mit der endung der tiles]

    if länge df == 1 -> download_batch()
    else:
        for i in df:
            download_batch(dstdir = dstdir)


def get_available_datasets_from_tiles(products=["S30"],
                                      years=[2018],
                                      user_shape= "/home/robin/python_projects/data/nasa_hls/test_shape/dummy_region.shp",
                                      return_list = False):

    # retrieve required tiles from the function above
    tiles = get_required_tiles_from_utm(user_shape=user_shape)
    datasets = nasa_hls.get_available_datasets(products=products, years=years, tiles=tiles, return_list=False)

    return datasets

def show_available_dates(df):
    print(type(df))
    df_sorted = df.sort_values("date")
    df_grouped = df_sorted.groupby(['date']).count()
    df_selected = df_grouped.iloc[:,0:1]

    return df_selected


def extract_date(df, date = "2018-01-01"):
    """
    date: date in the format "yyyy-mm-dd"
    df: dataframe-object returned by the "get_available_datasets_from_tiles"-function
    --------
    returns:
    dataframe with scenes from the scpecified date
    """

    # set the date column to index
    df = df.set_index("date")

    # check if specified date is in date column
    if date not in df.index:
        print("\n \n For the tiles in your shapefile is no data at this date available")
        return None
    else:
        df = df.loc[date]
        print("\n \n There are {nrows} scenes available for the specified date and location".format(nrows = df.shape[0]))

    return df



    



