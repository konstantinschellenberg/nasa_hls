import os
import glob
from osgeo import gdal
import subprocess

from .download_tiles import path_auxil
from .utils import BAND_NAMES

gdal.UseExceptions()


def make_mosaic2(srcdir=None, dstdir=None, bands=None, product="S30", shape = None):

    options = gdal.BuildVRTOptions(separate=True)
    
    # get all hdf-files
    hdf_files_list = list(glob.glob(srcdir + '*.hdf'))
    #print(hdf_files_list)

    # make list of all dates in directory
    dates_doy = []
    for line in hdf_files_list:
        l = line.split(".")[3][4:]
        dates_doy.append(l)

    #print(dates_doy)

    # make a function that gets the unique entries from a list
    # these will be the keys afterwards
    def unique_dates(liste):
        unique_dates = []
        for x in liste:
            if x not in unique_dates:
                unique_dates.append(x)
        return unique_dates

    # make the list of unique dates
    unique_doy = unique_dates(dates_doy)

    # create dictionary with keys being the unique dates
    # not yet specify the value-type
    dataframe_dict = {date: None for date in unique_doy}

    # add rows of orignial dataframe as values
    for key in dataframe_dict.keys():
        foo = []
        # now go over all the files
        for line in hdf_files_list:
            # get the doy
            line_date = line.split(".")[3][4:]
            # wenn doy in der line == dem key, dann schreib es in die liste foo
            if key == line_date:
                foo.append(line)
        # nachdem du über alle files gegangen bist, schreib an den key mit dem doy die aktuelle foo-liste,
        # die nach diesem Durchgang wieder neu aufgesetzt wird
        dataframe_dict[key] = foo

    # print(dataframe_dict["311"], "\n\n")
    # for key, item in dataframe_dict.items():
    # print(key, item, "\n")

    # check if band is specified
    if bands is None:
        bands = list(BAND_NAMES[product].keys())
        long_band_names = []
        for long_band_name in bands:
            band = BAND_NAMES[product][long_band_name]
            long_band_names.append(band)
    else:
        long_band_names = bands

    if not os.path.exists(path_auxil + "mosaic/bands/"):
        os.makedirs(os.path.join(path_auxil + "mosaic/bands/"))


    ##################
    #Check if Sentinel or Landsat
    ##################
    if product == "L30":

        for key in dataframe_dict.keys():
            for band in long_band_names:
                hdf_list = dataframe_dict[key]
                hdf_file_bands = []
                for hdf_file in hdf_list:
                    filename = 'HDF4_EOS:EOS_GRID:"{0}":Grid:{1}'.format(hdf_file, band)
                    hdf_file_bands.append(filename)

                # print("\n".join(hdf_file_bands))
                # make mosaics for each band for each date
                vrt_path = os.path.join(path_auxil + "mosaic/bands/" + key + band + ".vrt")
                build_vrt = gdal.BuildVRT(vrt_path, hdf_file_bands, options = options)
                build_vrt = None
        
        #depricated??!
        #dates_dict = {date: None for date in unique_doy}

        # list of vrts
        print("the unique days are: \n", unique_doy, "\n")
        print("now all the vrts\n")
        # PROBLEM: Glob doesn't take the bands in sequence... So sorting later needed to restore band order
        vrts = list(glob.glob(path_auxil + "mosaic/bands/" + "*.vrt"))
        print(vrts)

        # make list of list of bands for each day
        days = []
        for i in unique_doy:
            print(i)
            days_unique = []
            for j in vrts:
                print(j.split(".")[2][-9:-6])
                print(j.split(".")[2][-9:])
                if len(j) == 57: #risky
                    if j.split(".")[2][-9:-6] == i:
                        days_unique.append(j)
                if len(j) != 57:
                    if j.split(".")[2][-5:-2] == i:
                        days_unique.append(j)

                
            days.append(days_unique)
        
        print("this is days[0]", "\n", days[0])
        # get band character in every string for sorting
        def getBand(foo):
            """
            param: foo (string)
            """
            return foo.split(".")[2][-2:]

        # sort band-vrts for each day
        for i in days:
            i.sort(key = getBand)

        
        #make final vrts and tifs
        if not os.path.exists(path_auxil + "mosaic/days/"):
            os.makedirs(os.path.join(path_auxil + "mosaic/days/"))
        vrt_days = os.path.join(path_auxil + "mosaic/days/")

        for i in days:
            #print("\n\n\n", "this is i" , "\n", i)
            vrt_path = os.path.join(vrt_days + i[0][-13:-10] + "final.vrt")
            #print(vrt_path)
            single_vrt = gdal.BuildVRT(vrt_path, i, options = options)
            tiff_path = os.path.join(dstdir + i[0][-13:-10] + ".tiff")
            tif = gdal.Translate(tiff_path, single_vrt)
    
    #if product = Sentinel
    elif product == "S30":
        print("i'm in, sentinel!!")

        #key is the doy, values are lists of all the hdf-files for that date
        # {"001":[HLS...hdf, HLS...hdf.. ]}
        #for day
        for key in dataframe_dict.keys():
            #long_band_names
            #['B01', 'B02', 'B03', 'B04', 'B05', 'B07', 'B08', 'B8A', 'B10', 'B11', 'B12', 'QA']
            print(long_band_names)
            #for band
            for band in long_band_names:
                #get the hdf files for that date in a list
                hdf_list = dataframe_dict[key]
                
                
                #go over all the bandsand mosaic the bands
                hdf_file_bands = []
                for hdf_file in hdf_list:
                    filename = 'HDF4_EOS:EOS_GRID:"{0}":Grid:{1}'.format(hdf_file, band)
                    hdf_file_bands.append(filename)
                
                
        
                # print("\n".join(hdf_file_bands))
                # make mosaics for each band for each date
                vrt_path = os.path.join(path_auxil + "mosaic/bands/" + key + band + ".vrt")
                build_vrt = gdal.BuildVRT(vrt_path, hdf_file_bands, options = options)
                build_vrt = None
        
        #depricated??!
        #dates_dict = {date: None for date in unique_doy}

        # list of vrts
        print("\nthe unique days are: \n", unique_doy, "\n")
        #print("now all the vrts\n")
        # PROBLEM: Glob doesn't take the bands in sequence... So sorting later needed to restore band order
        vrts = list(glob.glob(path_auxil + "mosaic/bands/" + "*.vrt"))
        #print(vrts)
        

        # make list of list of bands for each day
        days = []
        for i in unique_doy:
            #print(i)
            days_unique = []
            for j in vrts:
                #print(j.split(".")[2][-5:-2])
                if len(j) == 54: #risky
                    #print("this is j:\n", j)
                    if j.split(".")[2][-6:-3] == i:
                        days_unique.append(j)
                if len(j) != 54:
                    if j.split(".")[2][-5:-2] == i:
                        days_unique.append(j)

                
            days.append(days_unique)
        
        print("this is days[0]", "\n", days[0])
       

        # get band character in every string for sorting
        def getBand(foo):
            """
            param: foo (string)
            """
            return foo.split(".")[2][-5:] #TODO: might be different for Sentinel

        # sort band-vrts for each day
        for i in days:
            i.sort(key = getBand)

        
        #make final vrts and tifs
        if not os.path.exists(path_auxil + "mosaic/days/"):
            os.makedirs(os.path.join(path_auxil + "mosaic/days/"))
        vrt_days = os.path.join(path_auxil + "mosaic/days/")

        for i in days:
            print("\n\n\n", "this is i" , "\n", i, "\n\n")
            i.append(i.pop(0)) # der Geniestreich meines Lebens...
            print("\n\n\n", "this is i" , "\n", i, "\n")
            #i[0] just to get the date info from any string
            if "QA" in i[0]:
                vrt_path = os.path.join(vrt_days + i[0][-9:-6] + "final.vrt") # for debugging just keep this line and outcomment the next three
                single_vrt = gdal.BuildVRT(vrt_path, i, options = options)
                tiff_path = os.path.join(dstdir + i[0][-9:-6] + ".tiff")
                tif = gdal.Translate(tiff_path, single_vrt)
            else:
                print("in else")
                vrt_path = os.path.join(vrt_days + i[0][-10:-7] + "final.vrt")
                #print(vrt_path)
                single_vrt = gdal.BuildVRT(vrt_path, i, options = options)
                tiff_path = os.path.join(dstdir + i[0][-10:-7] + ".tiff")
                cmd= "gdalwarp -srcnodata '-1000 -255' -cutline {shape} {vrt_path} {tiff_path}".format(shape = shape, vrt_path = vrt_path, tiff_path = tiff_path)        
                subprocess.call(cmd, shell=True)
                #tif = gdal.Translate(tiff_path, single_vrt)

