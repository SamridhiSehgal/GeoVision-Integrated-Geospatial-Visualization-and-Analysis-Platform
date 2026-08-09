import pandas as pd


class FOVProvider:

    DEFAULT_FOV = 45.0  # <-- Change this only if mentor changes it

    REQUIRED_COLUMNS = [
        "Timestamp",
        "Sensor_Lat",
        "Sensor_Lon",
        "Sensor_Alt",
        "Target_Lat",
        "Target_Lon",
        "Target_Alt",
        "Azimuth",
        "Elevation",
        "Range_m",
    ]

    def __init__(self):
        self.frames = []

    def load_excel(self, filename):

        df = pd.read_excel(filename)

        for column in self.REQUIRED_COLUMNS:

            if column not in df.columns:
                raise Exception(f"Missing required column: {column}")

        self.frames.clear()

        for _, row in df.iterrows():

            frame = {
                "timestamp": row["Timestamp"],
                "sensor_name": (
                    str(row["Sensor_Name"]).strip()
                    if "Sensor_Name" in df.columns and pd.notna(row["Sensor_Name"])
                    else None
                ),
                "sensor_lat": float(row["Sensor_Lat"]),
                "sensor_lon": float(row["Sensor_Lon"]),
                "sensor_alt": (
                    float(row["Sensor_Alt"])
                    if "Sensor_Alt" in df.columns and pd.notna(row["Sensor_Alt"])
                    else None
                ),
                "target_name": (
                    str(row["Target_Name"]).strip()
                    if "Target_Name" in df.columns and pd.notna(row["Target_Name"])
                    else None
                ),
                "target_lat": float(row["Target_Lat"]),
                "target_lon": float(row["Target_Lon"]),
                "target_alt": (
                    float(row["Target_Alt"])
                    if "Target_Alt" in df.columns and pd.notna(row["Target_Alt"])
                    else None
                ),
                "azimuth": float(row["Azimuth"]),
                "elevation": float(row["Elevation"]),
                "range": float(row["Range_m"]),
                "fov": (
                    float(row["FOV"])
                    if "FOV" in df.columns and pd.notna(row["FOV"])
                    else self.DEFAULT_FOV
                ),
            }

            self.frames.append(frame)

        print(f"{len(self.frames)} Mission Frames Loaded")

        return self.frames
