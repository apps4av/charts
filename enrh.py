import common
import glob

import cycle


# Chart specific code

# download
start_date = cycle.get_version_start(cycle.get_cycle_download())  # to download which cycle
all_charts = common.list_crawl("https://www.faa.gov/air_traffic/flight_info/aeronav/digital_products/ifr/", "^http.*" + start_date + "/enr_h.*.zip$")
all_charts_2 = common.list_crawl("https://www.faa.gov/air_traffic/flight_info/aeronav/digital_products/ifr/", "^http.*" + start_date + "/enr_akh.*.zip$")
all_charts_3 = common.list_crawl("https://www.faa.gov/air_traffic/flight_info/aeronav/digital_products/ifr/", "^http.*" + start_date + "/enr_p.*.zip$")
for nn in all_charts_2:
    all_charts.append(nn)
for nn in all_charts_3: # P charts should be in the start so they can be overwritten
    all_charts.insert(0, nn)
common.download_list(all_charts)
all_files = common.get_files("ENR_*.tif")
# remove unused stuff
all_files.remove("ENR_AKH01_SEA.tif")
all_files.remove("ENR_P01_GUA.tif")
all_files.remove("ENR_H12.tif")
# P charts to get overwritten, ZKZK: Fix this by fixing geojson of P01
all_files.sort(reverse=True)
# make tiles
vrts = common.make_vrt_list(all_files, False, "ENR_H")
common.make_main_vrt(vrts,"ENR_H")
common.make_tiles("4", "9", "ENR_H")

# zip
all_tiles = glob.glob("tiles/4/**/*.webp", recursive=True)
common.zip_files(all_tiles, "ENR_H")
