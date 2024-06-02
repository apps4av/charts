import common
import glob

import cycle


# Chart specific code

# download add second entry for caribbean charts
start_date = cycle.get_version_start(cycle.get_cycle_download())  # to download which cycle
all_charts = common.list_crawl("https://www.faa.gov/air_traffic/flight_info/aeronav/digital_products/vfr/", "^http.*" + start_date + "/sectional-files/.*.zip$")
all_charts_2 = common.list_crawl("https://www.faa.gov/air_traffic/flight_info/aeronav/digital_products/vfr/", "^http.*" + start_date + "/Caribbean/.*.zip$")
for nn in all_charts_2:
    all_charts.append(nn)
common.download_list(all_charts)
all_files = common.get_files("SEC")

# make tiles
vrts = common.make_vrt_list(all_files, True, "SEC")
common.make_main_vrt(vrts, "SEC")
common.make_tiles("0", "10", "SEC")

# zip
all_tiles = glob.glob("tiles/0/**/*.webp", recursive=True)
common.zip_files(all_tiles, "SEC")
