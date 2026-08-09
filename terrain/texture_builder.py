
import numpy as np

from PIL import Image

from providers.mbtiles_texture import MBTilesTexture

class TextureBuilder:
    """
    Builds one large RGB image from a raster MBTiles.
    """

    def __init__(self, mbtiles_path):

        self.reader = MBTilesTexture(mbtiles_path)

    # -----------------------------------------------------

    def build(
        self,
        zoom=None,
    ):

        metadata = self.reader.get_metadata()

        if zoom is None:

            if "maxzoom" in metadata:

                zoom = int(metadata["maxzoom"])

            else:

                zoom = 0

        print("Building texture...")
        print("Zoom :", zoom)

        n = 2**zoom

        tile_size = 256

        width = n * tile_size

        height = n * tile_size

        texture = np.zeros(
            (
                height,
                width,
                3,
            ),
            dtype=np.uint8,
        )

        loaded = 0

        missing = 0

        for y in range(n):

            for x in range(n):

                tile = self.reader.get_tile(
                    zoom,
                    x,
                    y,
                )

                if tile is None:

                    missing += 1

                    continue

                tile = np.array(tile)

                r0 = y * tile_size
                r1 = r0 + tile_size

                c0 = x * tile_size
                c1 = c0 + tile_size

                texture[
                    r0:r1,
                    c0:c1,
                ] = tile

                loaded += 1

        print()

        print("Loaded Tiles :", loaded)

        print("Missing Tiles :", missing)

        print("Texture Size :", texture.shape)

        return texture

    # -----------------------------------------------------

    def save(
        self,
        filename,
        zoom=None,
    ):

        image = self.build(zoom)

        Image.fromarray(image).save(filename)

        print()

        print("Texture saved")

        print(filename)

    # -----------------------------------------------------

    def close(self):

        self.reader.close()

trajectory_loader
import pandas as pd

from .trajectory_point import TrajectoryPoint

class TrajectoryLoader:

    REQUIRED_COLUMNS = [
        "Timestamp",
        "Lat",
        "Lon",
        "Alt",
        "Vel",
        "Acc",
    ]

    def load(self, filename):

        df = pd.read_excel(filename)

        for column in self.REQUIRED_COLUMNS:

            if column not in df.columns:

                raise Exception(f"Missing column: {column}")

        points = []

        for _, row in df.iterrows():

            point = TrajectoryPoint(
                timestamp=float(row["Timestamp"]),
                latitude=float(row["Lat"]),
                longitude=float(row["Lon"]),
                alt=float(row["Alt"]),
                velocity=float(row["Vel"]),
                acceleration=float(row["Acc"]),
            )

            points.append(point)

        print("Trajectory points loaded:", len(points))

        return points

mbtiles_path)

    # -----------------------------------------------------

    def build(
        self,
        zoom=None,
    ):

        metadata = self.reader.get_metadata()

        if zoom is None:

            if "maxzoom" in metadata:

                zoom = int(metadata["maxzoom"])

            else:

                zoom = 0

        print("Building texture...")
        print("Zoom :", zoom)

        n = 2**zoom

        tile_size = 256

        width = n * tile_size

        height = n * tile_size

        texture = np.zeros(
            (
                height,
                width,
                3,
            ),
            dtype=np.uint8,
        )

        loaded = 0

        missing = 0

        for y in range(n):

            for x in range(n):

                tile = self.reader.get_tile(
                    zoom,
                    x,
                    y,
                )

                if tile is None:

                    missing += 1

                    continue

                tile = np.array(tile)

                r0 = y * tile_size
                r1 = r0 + tile_size

                c0 = x * tile_size
                c1 = c0 + tile_size

                texture[
                    r0:r1,
                    c0:c1,
                ] = tile

                loaded += 1

        print()

        print("Loaded Tiles :", loaded)

        print("Missing Tiles :", missing)

        print("Texture Size :", texture.shape)

        return texture

    # -----------------------------------------------------

    def save(
        self,
        filename,
        zoom=None,
    ):

        image = self.build(zoom)

        Image.fromarray(image).save(filename)

        print()

        print("Texture saved")

        print(filename)

    # -----------------------------------------------------

    def close(self):

        self.reader.close()
