import rasterio


class CoordinateConverter:

    def __init__(self, transform):

        self.transform = transform

    def latlon_to_xy(self, lon, lat):

        x, y = rasterio.transform.xy(self.transform, lat, lon)

        return x, y
