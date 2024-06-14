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
for nn in all_charts_3:
    all_charts.append(nn)
common.download_list(all_charts)
all_files = common.get_files("ENR_H")
# P charts to get overwritten, ZKZK: Fix this by fixing geojson of P01
all_files.sort(reverse=True)
# make tiles
vrts = common.make_vrt_list(all_files, False, "ENR_H")
common.make_main_vrt(vrts,"ENR_H")
common.make_tiles("4", "9", "ENR_H")

# zip
all_tiles = glob.glob("tiles/4/**/*.webp", recursive=True)
common.zip_charts(all_tiles, "ENR_H")
