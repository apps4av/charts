import common
import glob

import cycle


# Chart specific code

# download
start_date = cycle.get_version_start(cycle.get_cycle_download())  # to download which cycle
all_charts = common.list_crawl("https://www.faa.gov/air_traffic/flight_info/aeronav/digital_products/ifr/", "^http.*" + start_date + "/enr_a0.*.zip$")
all_charts_2 = common.list_crawl("https://www.faa.gov/air_traffic/flight_info/aeronav/digital_products/ifr/", "^http.*" + start_date + "/enr_akl.*.zip$")
for nn in all_charts_2:
    all_charts.append(nn)
common.download_list(all_charts)
all_files = common.get_files("ENR_A")
# make tiles
vrts = common.make_vrt_list(all_files, False, "ENR_A")
common.make_main_vrt(vrts,"ENR_A")
common.make_tiles("5", "11", "ENR_A")

# zip
all_tiles = glob.glob("tiles/5/**/*.webp", recursive=True)
common.zip_files(all_tiles, "ENR_A")
