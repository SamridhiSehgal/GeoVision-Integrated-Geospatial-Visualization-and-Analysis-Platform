"""
Reproject a DEM from its original CRS (e.g. EPSG:4326)
to an appropriate UTM CRS for 3D rendering.

The original DEM is NOT modified.
"""

from pathlib import Path

import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
from rasterio.crs import CRS


def get_utm_crs(bounds):
    """
    Determine UTM zone from DEM center.
    """

    lon = (bounds.left + bounds.right) / 2
    lat = (bounds.top + bounds.bottom) / 2

    zone = int((lon + 180) / 6) + 1

    if lat >= 0:
        epsg = 32600 + zone
    else:
        epsg = 32700 + zone

    return CRS.from_epsg(epsg)


def reproject_dem(input_file, output_file):

    with rasterio.open(input_file) as src:

        dst_crs = get_utm_crs(src.bounds)

        transform, width, height = calculate_default_transform(
            src.crs, dst_crs, src.width, src.height, *src.bounds
        )

        kwargs = src.meta.copy()

        kwargs.update(
            {"crs": dst_crs, "transform": transform, "width": width, "height": height}
        )

        with rasterio.open(output_file, "w", **kwargs) as dst:

            reproject(
                source=rasterio.band(src, 1),
                destination=rasterio.band(dst, 1),
                src_transform=src.transform,
                src_crs=src.crs,
                dst_transform=transform,
                dst_crs=dst_crs,
                resampling=Resampling.bilinear,
            )

    print("Finished!")
    print("Output:", output_file)


if __name__ == "__main__":

    input_dem = r"terrain\gt30e060n40.tif"

    output_dem = r"terrain\gt30e060n40_UTM.tif"

    reproject_dem(input_dem, output_dem)
