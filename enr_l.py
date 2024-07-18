import common
import glob

import cycle


# Chart specific code

# download
start_date = cycle.get_version_start(cycle.get_cycle_download())  # to download which cycle
all_charts = common.list_crawl("https://www.faa.gov/air_traffic/flight_info/aeronav/digital_products/ifr/", "^http.*" + start_date + "/enr_l.*.zip$")
all_charts_2 = common.list_crawl("https://www.faa.gov/air_traffic/flight_info/aeronav/digital_products/ifr/", "^http.*" + start_date + "/enr_akl.*.zip$")
for nn in all_charts_2:
    all_charts.append(nn)
common.download_list(all_charts)
all_files = common.get_files("ENR_L")
# make tiles
vrts = common.make_vrt_list(all_files, False, "ENR_L")

## Order for stacking sequence
vrts.sort()

common.make_main_vrt(vrts,"ENR_L")
common.make_tiles("3", "10", "ENR_L")

# zip
all_tiles = glob.glob("tiles/3/**/*.webp", recursive=True)
common.zip_charts(all_tiles, "ENR_L")
