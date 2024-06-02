import common
import glob

import cycle


# Chart specific code

# download flyways in TACs
start_date = cycle.get_version_start(cycle.get_cycle_download())  # to download which cycle
all_charts = common.list_crawl("https://www.faa.gov/air_traffic/flight_info/aeronav/digital_products/vfr/", "^http.*" + start_date + ".*_TAC.zip$")
common.download_list(all_charts)
all_files = common.get_files("*FLY.tif")
# make tiles
vrts = common.make_vrt_list(all_files, "FLY")
common.make_main_vrt(vrts,"FLY")
common.make_tiles("13", "11", "FLY")

# zip
all_tiles = glob.glob("tiles/13/**/*.webp", recursive=True)
common.zip_files(all_tiles, "FLY")
