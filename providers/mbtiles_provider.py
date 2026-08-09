import sqlite3
class MBTilesProvider:
    """
    Universal Raster MBTiles Provider

    Supports:
        • tiles
        • map + images

    Formats:
        • png
        • jpg
        • jpeg
        • webp

    Tile schemes:
        • TMS
        • XYZ (automatic fallback)
    """
    def __init__(self, mbtiles_path):
        self.mbtiles_path = mbtiles_path
        self.conn = sqlite3.connect(self.mbtiles_path)
        self.cursor = self.conn.cursor()
        self.tables = self.get_tables()
        self.schema = self.detect_schema()
        self.metadata = self.read_metadata()
        self.format = self.metadata.get("format", "png").lower()
        self.content_type = self.get_content_type()
        print("\n========== MBTILES ==========")
        print("File      :", self.mbtiles_path)
        print("Schema    :", self.schema)
        print("Format    :", self.format)
        print("Min Zoom  :", self.metadata.get("minzoom", "Unknown"))
        print("Max Zoom  :", self.metadata.get("maxzoom", "Unknown"))
        print("=============================\n")
    # ---------------------------------------------------
    # TABLES
    # ---------------------------------------------------
    def get_tables(self):
        self.cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='table'
        """)
        return [row[0] for row in self.cursor.fetchall()]
    # -------------------------------------------------
    # SCHEMA
    # ---------------------------------------------------
    def detect_schema(self):
        if "tiles" in self.tables:
            return "tiles"
        if "map" in self.tables and "images" in self.tables:
            return "map_images"
        raise Exception("Unsupported MBTiles schema")
    # ---------------------------------------------------
    # METADATA
    # ---------------------------------------------------
    def read_metadata(self):
        metadata = {}
        if "metadata" not in self.tables:
            return metadata
        try:
            self.cursor.execute("""
                SELECT name,value
                FROM metadata
            """)
            for key, value in self.cursor.fetchall():
                metadata[key] = value
        except:
            pass
        return metadata
    # ---------------------------------------------------
    # CONTENT TYPE
    # ---------------------------------------------------
    def get_content_type(self):
        if self.format == "png":
            return "image/png"
        if self.format in ["jpg", "jpeg"]:
            return "image/jpeg"
        if self.format == "webp":
            return "image/webp"
        if self.format == "pbf":
            return "application/x-protobuf"
        return "application/octet-stream"
    # ---------------------------------------------------
    # INTERNAL DATABASE QUERIES
    # ---------------------------------------------------
    def _query_tiles(self, z, x, row):
        self.cursor.execute(
            """
            SELECT tile_data
            FROM tiles
            WHERE zoom_level=?
            AND tile_column=?
            AND tile_row=?
        """,
            (z, x, row),
        )
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None
    def _query_map_images(self, z, x, row):
        self.cursor.execute(
            """
            SELECT tile_id
            FROM map
            WHERE zoom_level=?
            AND tile_column=?
            AND tile_row=?
        """,
            (z, x, row),
        )
        tile = self.cursor.fetchone()
        if tile is None:
            return None
        tile_id = tile[0]
        self.cursor.execute(
            """
            SELECT tile_data
            FROM images
            WHERE tile_id=?
        """,
            (tile_id,),
        )
        image = self.cursor.fetchone()
        if image:
            return image[0]
        return None
    # ---------------------------------------------------
    # PUBLIC TILE API
    # ---------------------------------------------------
    def get_tile(self, z, x, y):
        # Try TMS first
        tms_y = (2**z - 1) - y
        if self.schema == "tiles":
            tile = self._query_tiles(z, x, tms_y)
            if tile:
                return tilec 
            # XYZ fallback
            return self._query_tiles(z, x, y)
        elif self.schema == "map_images":
            tile = self._query_map_images(z, x, tms_y)
            if tile:
                return tile
            # XYZ fallback
            return self._query_map_images(z, x, y)
        return None
    # ---------------------------------------------------
    # INFORMATION
    # ---------------------------------------------------
    def print_info(self):
        print("\nMBTiles Information\n")
        print("Schema :", self.schema)
        print("Format :", self.format)
        print()
        for key, value in self.metadata.items():
            print(f"{key:<12}: {value}")
    # ---------------------------------------------------
    # CLsdOSE
    # --------------------------------------------------
    def close(self):
        self.conn.close()
