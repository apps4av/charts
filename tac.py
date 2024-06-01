import common
import glob

# Chart specific code

# download
all_charts = common.list_crawl("https://www.faa.gov/air_traffic/flight_info/aeronav/digital_products/vfr/", "^http.*_TAC.zip$")
common.download_list(all_charts)
all_files = common.get_files("*TAC.tif")

# make tiles
vrts = common.make_vrt_list(all_files)
common.make_main_vrt("TAC", vrts)
common.make_tiles("TAC", "1", "11")

# zip
all_tiles = glob.glob("tiles/1/**/*.webp", recursive=True)
common.zip_files(all_tiles, "TAC")
