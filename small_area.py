import numpy as np
import datetime
import json
from geojson import Polygon
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt

print('''

You should have already installed numpy, json, geojson, and sentinelsat.

''')

answer = input('Are you ready? [yes/no]: ')
print('')

if not answer in ('yes', 'YES', 'Yes', 'y', 'Y', ''):
    print('cancelled')
    exit

print('Tell me the range of latitude and longitude you want.')
print('(The range of latitude is -90 to 90, and longitude is -180 to 180.)')
print('')

lonmin = float(input('The minimum of longitude is: '))
lonmax = float(input('The maximum of longitude is: '))
latmin = float(input('The minimum of latitude is: '))
latmax = float(input('The maximum of latitude is: '))
print('')

area = [[lonmax, latmin],
[lonmin, latmin],
[lonmin, latmax],
[lonmax, latmax],
[lonmax, latmin]]

polygon = Polygon([area])

dt_info = datetime.datetime.now()
dt = dt_info.strftime('%Y_%m%d_%H%M_sentinel')
object_name = dt

with open(object_name + '.geojson', 'w') as f:
    json.dump(polygon, f)
footprint_geojson = geojson_to_wkt(read_geojson(str(object_name) + '.geojson'))

print('Type your username and password of Sentinel Hub.')
user = input('username: ')
password = input('password: ')
print('')

api = SentinelAPI(user, password, 'https://scihub.copernicus.eu/dhus')

print('Type the range of date, platfom name, processing level, and the cloud cover percentage.')
print('''
  Ex.----------------------------------------------------
  |  start date: 20200101                               |
  |  end date: 20201231                                 |
  |  platform name: Sentinel-2                          |
  |  processing level: Level-2A                         |
  |  minimun of cloud cover percentage [%]: 0           |
  |  maximum of cloud cover percentage [%]: 100         |
  -------------------------------------------------------
''')
sd = input('start date: ')
ed = input('end date: ')
p_name = input('platform name: ')
p_level = input('processing level: ')
min_ccp = float(input('minimum of cloud cover percentage [%]: '))
max_ccp = float(input('maximum of cloud cover percentage [%]: '))

print('''

=====searching data... please wait=====

''')

products = api.query(footprint_geojson, date = (sd, ed), platformname = p_name, processinglevel = p_level, cloudcoverpercentage = (min_ccp, max_ccp))

print('==> The number of data matching conditions is ' + str(len(products)))
print('')

products_gdf = api.to_geodataframe(products)

answer = input('Do you want to download the information data as .csv file? [yes/no]: ')
print('')

if answer in ('yes', 'YES', 'Yes', 'y', 'Y', ''):
    products_gdf.to_csv(object_name + '.csv')
    print('finish to download!')
else:
    pass

answer = input('Do you want to download all of TIFF data? [yes/no]: ')
print('')
if answer in ('yes', 'YES', 'Yes', 'y', 'Y', ''):
    products_uuid = products_gdf['uuid']
    for i in range(0, len(products_uuid)):
        print(str(products_gdf['ingestiondate'][i]))
        api.download(products_gdf.iloc[i]["uuid"])
else:
    pass

print('''

======finish all!======

''')
