import glob
import os
import urllib.request
import re
from bs4 import BeautifulSoup
import zipfile
from tqdm import tqdm


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


def make_vrt(name):
    no_extension_name = name.split(".")[0]
    try:
        os.remove(no_extension_name + ".vrt")
        os.remove(no_extension_name + "rgb.vrt")
    except FileNotFoundError as e:
        pass

    os.system("gdal_translate -of vrt -r cubicspline -expand rgb '" + name + "' '" + no_extension_name + "rgb.vrt'")
    os.system("gdalwarp -of vrt -r cubicspline -dstnodata 51 -t_srs 'EPSG:3857' -cutline '" + no_extension_name + ".geojson' " + "-crop_to_cutline '" + no_extension_name + "rgb.vrt' '" + no_extension_name + ".vrt'")


def make_vrt_list(charts):
    for cc in tqdm(range(len(charts)), desc="Making VRT files"):
        make_vrt(charts[cc])


def get_files(match):
    return glob.glob(match)


all_charts = list_crawl("https://www.faa.gov/air_traffic/flight_info/aeronav/digital_products/vfr/", "^http.*_TAC.zip$")
download_list(all_charts)
all_files = get_files("*TAC.tif")
make_vrt_list(all_files)
os.system("gdalbuildvrt -r cubicspline -srcnodata 51 -vrtnodata 51 -resolution highest $@ -overwrite TAC.vrt *TAC.vrt")
os.system("gdal2tiles.py -t TAC --tilesize=512 --tiledriver=WEBP --webp-quality=60 --exclude --webviewer=all -c MUAVLLC --no-kml --resume --processes 8 -z 0-11 -r near tac.vrt tiles/1")
