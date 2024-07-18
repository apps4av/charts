import glob
import os
import urllib.request
import re
from subprocess import check_call

from bs4 import BeautifulSoup
import zipfile
from tqdm import tqdm

import cycle
import projection


def is_in(area, lon, lat):
    x_u, y_u, x_l, y_l = area
    if lat <= y_u and lat >= y_l and lon >= x_u and lon <= x_l:
        return True
    return False


def list_crawl(url, match):
    charts = []
    html_page = urllib.request.urlopen(url)
    soup = BeautifulSoup(html_page, "html.parser")
    for link in tqdm(soup.findAll('a'), desc="Scanning website links"):
        link_x = link.get('href')
        if link_x is None:
            continue
        if re.search(match, link_x):
            charts.append(link_x)
    list_set = set(charts)  # unique
    return list(list_set)


def download(url):
    name = url.split("/")[-1]
    # check if exists
    if not os.path.isfile(name):
        urllib.request.urlretrieve(url, name)
    if name.endswith(".zip"):  # if a zipfile, unzip first
        with zipfile.ZipFile(name, 'r') as zip_ref:
            zip_ref.extractall(".")


def download_list(charts):
    for cc in tqdm(range(len(charts)), desc="Downloading/unzipping"):
        download(charts[cc])


def make_main_vrt(vrt_list, chart_type):
    name = chart_type + ".vrt"
    try:
        os.remove(name)
    except FileNotFoundError as e:
        pass

    all_vrts = "".join([" '" + vrt + "' " for vrt in vrt_list])
    check_call(["gdalbuildvrt -r cubicspline -srcnodata 51 -vrtnodata 51 -resolution highest -overwrite " + name + all_vrts], shell=True)


def make_vrt(name, rgb, chart_type):
    no_extension_name = os.path.splitext(name)[0]
    try:
        os.remove(no_extension_name + ".vrt")
        os.remove(no_extension_name + "rgb.vrt")
    except FileNotFoundError as e:
        pass

    # used for VFR charts
    if rgb:
        check_call(["gdal_translate -of vrt -r cubicspline -expand rgb '" + name + "' '" + no_extension_name + "rgb.vrt'"], shell=True)
        check_call(["gdalwarp -of vrt -r cubicspline -dstnodata 51 -t_srs 'EPSG:3857' -cutline '" + chart_type + "/" + no_extension_name + ".geojson' " + "-crop_to_cutline '" + no_extension_name + "rgb.vrt' '" + no_extension_name + ".vrt'"], shell=True)
    # used for IFR charts
    else:
        check_call(["gdalwarp -of vrt -r cubic -dstnodata 51 -t_srs 'EPSG:3857' -cutline '" + chart_type + "/" + no_extension_name + ".geojson' " + "-crop_to_cutline '" + name + "' '" + no_extension_name + ".vrt'"], shell=True)

    return no_extension_name + ".vrt"


def make_vrt_list(charts, rgb, chart_type):
    ret = []
    for cc in tqdm(range(len(charts)), desc="Making VRT files"):
        ret.append(make_vrt(charts[cc], rgb, chart_type))
    return ret


def get_files(match):
    list_files = glob.glob("*.geojson", root_dir=match)
    return [gg.replace(".geojson", ".tif") for gg in list_files]


def zip_charts(list_of_all_tiles, chart):
    # US geo regions
    regions = ["AK", "PAC", "NW", "SW", "NC", "EC", "SC", "NE", "SE"]
    region_coordinates = [
        (-180, 71, -126, 51),   # AK
        (-162, 24, -152, 18),   # PAC
        (-125, 50, -103, 40),   # NW
        (-125, 40, -103, 15),   # SW
        (-105, 50, -90,  37),   # NC
        (-95,  50, -80,  37),   # EC
        (-110, 37, -90,  15),   # SC
        (-80,  50, -60,  37),   # NE
        (-90,  37, -60,  15),   # SE
    ]
    zip_files = []
    manifest_files = []

    for region in regions:
        try:
            os.remove(region + "_" + chart + ".zip")
            os.remove(region + "_" + chart)
        except FileNotFoundError as e:
            pass

    for region in regions:
        zip_files.append(zipfile.ZipFile(region + "_" + chart + ".zip", "w"))
        manifest_files.append(open(region + "_" + chart, "w+"))

    for ff in manifest_files:
        ff.write(cycle.get_cycle() + "\n")

    for tile in tqdm(list_of_all_tiles, desc="Zipping up tiles in Areas"):
        tokens = tile.split("/")
        y_tile = int(tokens[len(tokens) - 1].split(".")[0])
        x_tile = int(tokens[len(tokens) - 2])
        z_tile = int(tokens[len(tokens) - 3])
        lon_tile, lat_tile, lon1_tile, lat1_tile = projection.findBounds(x_tile, y_tile, z_tile)

        # include zoom 7 and below in every chart
        for count in range(len(regions)):
            if is_in(region_coordinates[count], lon_tile, lat_tile) or z_tile <= 7:
                zip_files[count].write(tile)
                manifest_files[count].write(tile + "\n")

    for ff in manifest_files:
        ff.close()

    for count in range(len(regions)):
        zip_files[count].write(regions[count] + "_" + chart)
        zip_files[count].close()


def make_tiles(index, max_zoom, chart_type):
    check_call(["rm -rf tiles/" + index], shell=True)
    call = "gdal2tiles.py -t " + chart_type + " --tilesize=512 --tiledriver=WEBP --webp-quality=60 --exclude --webviewer=all -c MUAVLLC --no-kml --resume --processes 8 -z 0-" + max_zoom + " -r near " + chart_type + ".vrt tiles/" + index
    print(f'Making tiles with call: {call}')
    check_call([call], shell=True)
