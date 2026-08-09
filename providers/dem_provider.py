import rasterio
import numpy as np
from pyproj import Transformer
class DEMProvider:

    def __init__(self, dem_path):

        self.dataset = rasterio.open(dem_path)
        self.band = self.dataset.read(1)
        self.nodata = self.dataset.nodata

        print("DEM CRS:", self.dataset.crs)

        self.transformer = Transformer.from_crs(
            "EPSG:4326", self.dataset.crs, always_xy=True
        )

    # Get elevation
    def get_elevation(self, latitude, longitude):

        try:

            # Convert Lat/Lon -> DEM CRS
            x, y = self.transformer.transform(longitude, latitude)

            row, col = self.dataset.index(x, y)

            if (
                row < 0
                or col < 0
                or row >= self.band.shape[0]
                or col >= self.band.shape[1]
            ):
                return None

            elevation = self.band[row, col]

            if self.nodata is not None and elevation == self.nodata:
                return None

            if np.isnan(elevation):
                return None

            return float(elevation)

        except Exception as e:
            print("DEM Error:", e)
            return None

    def get_crs(self):
        return self.dataset.crs

    def get_bounds(self):
        return self.dataset.bounds

    def get_resolution(self):
        return self.dataset.res

    def close(self):
        self.dataset.close()
