import sqlite3
import io
from PIL import Image


class MBTilesTexture:

    def __init__(self, mbtiles_path):

        self.path = mbtiles_path

        self.conn = sqlite3.connect(self.path)

        self.metadata = self.read_metadata()

        print("\nLoaded MBTiles:")
        print(self.path)

        print("\nMetadata:")
        for k, v in self.metadata.items():
            print(k, "=", v)

    # ----------------------------------
    # Read metadata
    # ----------------------------------

    def read_metadata(self):

        cur = self.conn.cursor()

        data = {}

        try:

            cur.execute("""
                SELECT name,value
                FROM metadata
                """)

            for name, value in cur.fetchall():

                data[name] = value

        except:

            pass

        return data

    # ----------------------------------
    # Detect zoom automatically
    # ----------------------------------

    def get_zoom(self):

        cur = self.conn.cursor()

        cur.execute("""
            SELECT MAX(zoom_level)
            FROM tiles
            """)

        return cur.fetchone()[0]

    # ----------------------------------
    # Get available tiles
    # ----------------------------------

    def get_tile_range(self, zoom):

        cur = self.conn.cursor()

        cur.execute(
            """
            SELECT

            MIN(tile_column),
            MAX(tile_column),

            MIN(tile_row),
            MAX(tile_row)

            FROM tiles

            WHERE zoom_level=?

            """,
            (zoom,),
        )

        return cur.fetchone()

    # ----------------------------------
    # Read tile
    # ----------------------------------

    def read_tile(self, z, x, y):

        cur = self.conn.cursor()

        scheme = self.metadata.get("scheme", "tms")

        # Convert if TMS
        if scheme.lower() != "xyz":

            y = (2**z - 1) - y

        cur.execute(
            """
            SELECT tile_data

            FROM tiles

            WHERE zoom_level=?

            AND tile_column=?

            AND tile_row=?

            """,
            (z, x, y),
        )

        result = cur.fetchone()

        if result is None:

            return None

        return Image.open(io.BytesIO(result[0])).convert("RGB")

    # ----------------------------------
    # Create texture
    # ----------------------------------

    def create_texture(self, output):

        zoom = self.get_zoom()

        print("\nUsing zoom:", zoom)

        x1, x2, y1, y2 = self.get_tile_range(zoom)

        print("Tile range:", x1, x2, y1, y2)

        first = self.read_tile(zoom, x1, y1)

        if first is None:

            raise Exception("Cannot read first tile")

        tile_size = first.size[0]

        width = (x2 - x1 + 1) * tile_size

        height = (y2 - y1 + 1) * tile_size

        texture = Image.new("RGB", (width, height), (255, 255, 255))

        loaded = 0

        for x in range(x1, x2 + 1):

            for y in range(y1, y2 + 1):

                tile = self.read_tile(zoom, x, y)

                if tile is None:

                    continue

                texture.paste(tile, ((x - x1) * tile_size, (y - y1) * tile_size))

                loaded += 1

                # Limit texture size for PyVista
                max_size = 8192

                texture.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)

            texture.save(output)

        print("\nTexture created:", output)

        print("Tiles loaded:", loaded)


# =====================================
# ONLY CHANGE THIS LINE IN FUTURE
# =====================================

MBTILES_FILE = "maps/OUTPUT_FILE.mbtiles"


if __name__ == "__main__":

    reader = MBTilesTexture(MBTILES_FILE)

    reader.create_texture("terrain/texture.png")
