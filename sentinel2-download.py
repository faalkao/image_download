# Download sentinel 2, level 2A, within 2018-2019, created by Duong
# Mainlaind Vietnam lon:lat 102-110:8-24

# Installing some required library
# pip3 install sentinelsat
# pip3 install numpy

import numpy as np
import datetime
import json
from geojson import Polygon
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
import os.path, os, glob, multiprocessing
# Make clean
p = multiprocessing.Pool(4)
for i in {'*.csv', '*.incomplete', '*.geojson'}:
    list(p.map(os.remove, glob.glob(i)))
# List selected areas or AOI
# print('Range of latitude and longitude you want.')
# print('(The range of latitude is -90 to 90, and longitude is -180 to 180.)')
# lonmin = float(input('The minimum of longitude is: '))
# lonmax = float(input('The maximum of longitude is: '))
# latmin = float(input('The minimum of latitude is: '))
# latmax = float(input('The maximum of latitude is: '))
# area = [[lonmax, latmin], [lonmin, latmin], [lonmin, latmax], [lonmax, latmax], [lonmax, latmin]]
list_areas = [[[106.0, 23.0], [104.0, 23.0], [104.0, 24.0], [106.0, 24.0], [106.0, 23.0]],
             [[107.0, 22.0], [102.0, 22.0], [102.0, 23.0], [107.0, 23.0], [107.0, 22.0]],
             [[109.0, 21.0], [102.0, 21.0], [102.0, 22.0], [109.0, 22.0], [109.0, 21.0]],
             [[108.0, 20.0], [103.0, 20.0], [103.0, 21.0], [108.0, 21.0], [108.0, 20.0]],
             [[107.0, 19.0], [103.0, 19.0], [103.0, 20.0], [107.0, 20.0], [107.0, 19.0]],
             [[107.0, 18.0], [104.0, 18.0], [104.0, 19.0], [107.0, 19.0], [107.0, 18.0]],
             [[108.0, 17.0], [105.0, 17.0], [105.0, 18.0], [108.0, 18.0], [108.0, 17.0]],
             [[109.0, 16.0], [106.0, 16.0], [106.0, 17.0], [109.0, 17.0], [109.0, 16.0]],
             [[109.0, 15.0], [107.0, 15.0], [107.0, 16.0], [109.0, 16.0], [109.0, 15.0]],
             [[110.0, 14.0], [107.0, 14.0], [107.0, 15.0], [110.0, 15.0], [110.0, 14.0]],
             [[110.0, 13.0], [107.0, 13.0], [107.0, 14.0], [110.0, 14.0], [110.0, 13.0]],
             [[110.0, 12.0], [106.0, 12.0], [106.0, 13.0], [110.0, 13.0], [110.0, 12.0]],
             [[110.0, 11.0], [105.0, 11.0], [105.0, 12.0], [110.0, 12.0], [110.0, 11.0]],
             [[109.0, 10.0], [103.0, 10.0], [103.0, 11.0], [109.0, 11.0], [109.0, 10.0]],
             [[108.0, 9.0], [104.0, 9.0], [104.0, 10.0], [108.0, 10.0], [108.0, 9.0]],
             [[107.0, 8.0], [104.0, 8.0], [104.0, 9.0], [107.0, 9.0], [107.0, 8.0]]]

for area in list_areas:
    polygon = Polygon([area])

    # Create a geojson for the area
    dt_info = datetime.datetime.now()
    dt = dt_info.strftime('%Y_%m%d_%H%M_sentinel')
    object_name = dt
    with open(object_name + '.geojson', 'w') as f:
        json.dump(polygon, f)
    footprint_geojson = geojson_to_wkt(read_geojson(str(object_name) + '.geojson'))

    # print('Type your username and password of Sentinel Hub.')
    user = 'pcduong8088'
    password = 'Duong87324'
    api = SentinelAPI(user, password, 'https://scihub.copernicus.eu/dhus')

    # print('Type the range of date, platfom name, processing level, and the cloud cover percentage.')
    sd = '20180101'
    # print('Start data: ', sd)
    ed = '20191231'
    # print('End data: ', ed)
    p_name = 'Sentinel-2'
    # print('Platform name: ', p_name)
    p_level = 'Level-2A'
    # print('Processing level: ', p_level)
    min_ccp = 0.0
    # print('Min of cloud cover percentage: ', min_ccp)
    max_ccp = 5.0
    # print('Max of cloud cover percentage: ', max_ccp)

    print('=====searching data for ', area, ' please wait===== ')
    products = api.query(footprint_geojson, date=(sd, ed), platformname=p_name,
                         processinglevel=p_level, cloudcoverpercentage=(min_ccp, max_ccp))

    print('==> The number of data matching conditions is ' + str(len(products)))
    products_gdf = api.to_geodataframe(products)

    print('Download the information data as .csv file')
    products_gdf.to_csv(object_name + '.csv')
    print('Finish to download the csv of ', area)

    print('Download all of TIFF data')
    products_uuid = products_gdf['uuid']

    for i in range(0, len(products_uuid)):
        # print(str(products_gdf['ingestiondate'][i]))
        # api.download(products_gdf.iloc[i]["uuid"])
        title = products_gdf.iloc[i]["title"] + '.zip'
        if not os.path.isfile(title):
            try:
                print('there is not: ', title)
                api.download(products_gdf.iloc[i]["uuid"])
            except:
                pass
        else:
            pass
    print(''' ======finish all!====== ''', area)
