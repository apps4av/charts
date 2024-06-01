import math

# To get tile info. Ported from Avare
SIZE = 512
SIZE_INV = 1.0 / SIZE
ORIGIN_SHIFT = 2 * math.pi * 6378137.0 / 2.0
INITIAL_RESOLUTION = 2 * math.pi * 6378137.0 / SIZE
PI_180 = math.pi / 180.0
PI_2 = math.pi / 2.0
PI_360 = math.pi / 360.0
PI_180INV = 1.0 / PI_180
ORIGIN_SHIFT_180 = ORIGIN_SHIFT / 180.0
ORIGIN_SHIFT_180INV = 1.0 / ORIGIN_SHIFT_180

# Make a zoom table for resolution so we don't have to compute it often
zoomTable = [
    INITIAL_RESOLUTION / math.pow(2, i) for i in range(20)
]

# Make a zoom table for resolution so we don't have to compute it often
zoomTableInv = [
    1.0 / zoomTable[i] for i in range(20)
]


# Misc. calls
def getResolution(zoom):
    return zoomTable[int(zoom)]


def getInvResolution(zoom):
    return zoomTableInv[int(zoom)]


def latToMeters(lat):
    my = math.log(math.tan((90.0 + lat) * PI_360)) * PI_180INV
    return my * ORIGIN_SHIFT_180


def lonToMeters(lon):
    return lon * ORIGIN_SHIFT_180


def metersToLat(my):
    lat = my * ORIGIN_SHIFT_180INV
    lat = PI_180INV * (2.0 * math.atan(math.exp(lat * PI_180)) - PI_2)
    return lat


def metersToLon(mx):
    return mx * ORIGIN_SHIFT_180INV


def xPixelsToMeters(zoom, px):
    return px * getResolution(zoom) - ORIGIN_SHIFT


def yPixelsToMeters(zoom, py):
    return py * getResolution(zoom) - ORIGIN_SHIFT


def xMetersToPixels(zoom, mx):
    return (mx + ORIGIN_SHIFT) * getInvResolution(zoom)


def yMetersToPixels(zoom, my):
    return (my + ORIGIN_SHIFT) * getInvResolution(zoom)


def xPixelsToTile(px):
    return int(math.ceil(px * SIZE_INV) - 1)


def yPixelsToTile(py):
    return int(math.ceil(py * SIZE_INV) - 1)


def xMetersToTile(zoom, mx):
    px = xMetersToPixels(zoom, mx)
    return xPixelsToTile(px)


def yMetersToTile(zoom, my):
    py = yMetersToPixels(zoom, my)
    return yPixelsToTile(py)


def findBounds(x, y, zoom):
    lonU = metersToLon(xPixelsToMeters(zoom, x * SIZE))
    lonL = metersToLon(xPixelsToMeters(zoom, (x + 1) * SIZE))
    latU = metersToLat(yPixelsToMeters(zoom, y * SIZE))
    latL = metersToLat(yPixelsToMeters(zoom, (y + 1) * SIZE))
    return lonU, latU, lonL, latL
