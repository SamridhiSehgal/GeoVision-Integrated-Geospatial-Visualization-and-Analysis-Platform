import sqlite3
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

MBTILES_PATH = Path("maps/OUTPUT_FILE.mbtiles")


class TileServer(BaseHTTPRequestHandler):

    def send_png(self, data):
        self.send_response(200)
        self.send_header("Content-Type", "image/webp")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        self.wfile.write(data)

    def send_json(self, data):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):

        # --------------------------
        # Metadata
        # --------------------------
        if self.path == "/metadata":

            conn = sqlite3.connect(MBTILES_PATH)

            cur = conn.cursor()

            rows = cur.execute("SELECT name,value FROM metadata").fetchall()

            conn.close()

            metadata = dict(rows)

            self.send_json(metadata)

            return

        # --------------------------
        # Tiles
        # /tiles/z/x/y.png
        # --------------------------

        if self.path.startswith("/tiles/"):

            try:

                parts = self.path.split("/")

                z = int(parts[2])
                x = int(parts[3])

                filename = parts[4]

                filename = filename.replace(".png", "")
                filename = filename.replace(".jpg", "") 
                filename = filename.replace(".jpeg", "")
                filename = filename.replace(".webp", "")
                filename = filename.replace(".tile", "")

                y = int(filename)

                # XYZ -> TMS conversion
                tms_y = (2**z) - 1 - y

                conn = sqlite3.connect(MBTILES_PATH)

                cur = conn.cursor()

                result = cur.execute(
                    """
                    SELECT tile_data
                    FROM tiles
                    WHERE zoom_level=?
                    AND tile_column=?
                    AND tile_row=?
                    """,
                    (z, x, tms_y),
                ).fetchone()

                conn.close()

                if result:

                    self.send_png(result[0])

                else:

                    self.send_error(404, "Tile not found")

            except Exception as e:

                print(e)

                self.send_error(500, str(e))

            return

        self.send_error(404)


def main():

    server = HTTPServer(("localhost", 8000), TileServer)

    print("Tile Server running : http://localhost:8000")

    try:
        server.serve_forever()

    except KeyboardInterrupt:

        print("\nServer stopped")

        server.server_close()


if __name__ == "__main__":
    main()
