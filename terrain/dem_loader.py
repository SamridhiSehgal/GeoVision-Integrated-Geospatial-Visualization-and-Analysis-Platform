from dataclasses import dataclass

import numpy as np
import rasterio


@dataclass
class Terrain:

    elevation: np.ndarray
    resolution: tuple
    transform: object
    crs: object
    nodata: float


class DEMLoader:

    def __init__(self, dem_path):

        self.dem_path = dem_path

    # ---------------------------------------------------------

    def load(self):

        with rasterio.open(self.dem_path) as src:

            elevation = src.read(1).astype(np.float32)

            nodata = src.nodata

            if nodata is not None:

                elevation[elevation == nodata] = np.nan

            elevation = np.nan_to_num(elevation, nan=np.nanmean(elevation))

            terrain = Terrain(
                elevation=elevation,
                resolution=(abs(src.transform.a), abs(src.transform.e)),
                transform=src.transform,
                crs=src.crs,
                nodata=nodata,
            )

            return terrain
