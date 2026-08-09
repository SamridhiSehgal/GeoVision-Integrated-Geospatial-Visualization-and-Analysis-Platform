import pandas as pd
from providers.dem_provider import DEMProvider
from models.sensor import Sensor
from models.target import Target
class ExcelProvider:
    REQUIRED_COLUMNS = ["Name", "Lat", "Lon"]
    def __init__(self, dem_path="terrain/gt30e060n40_UTM.tif"):
        self.dem = DEMProvider(dem_path)
        self.sensors = []
        self.targets = []
    def load_excel(self, filename):
        df = pd.read_excel(filename)
        for column in self.REQUIRED_COLUMNS:
            if column not in df.columns:
                raise Exception(f"Missing required column: {column}")
        self.sensors.clear()
        self.targets.clear()
        for _, row in df.iterrows():
            name = str(row["Name"]).strip()
            lat = float(row["Lat"])
            lon = float(row["Lon"])
            elevation = self.dem.get_elevation(lat, lon)
            if elevation is None:
                print(f"No DEM elevation for {name}")
            heading = (
                float(row["Heading"])
                if "Heading" in df.columns and pd.notna(row["Heading"])
                else None
            )
            fov = (
                float(row["FOV"])
                if "FOV" in df.columns and pd.notna(row["FOV"])
                else None
            )
            detection_range = (
                float(row["Detection_Range"])
                if "Detection_Range" in df.columns and pd.notna(row["Detection_Range"])
                else None
            )
            mode = (
                str(row["Mode"])
                if "Mode" in df.columns and pd.notna(row["Mode"])
                else None
            )
            if name.upper().startswith("S"):
                sensor = Sensor(
                    name=name,
                    latitude=lat,
                    longitude=lon,
                    elevation=elevation,
                    heading=heading,
                    fov=fov,
                    detection_range=detection_range,
                    mode=mode,
                )
                self.sensors.append(sensor)
            else:
                target = Target(
                    name=name, latitude=lat, longitude=lon, elevation=elevation
                )
                self.targets.append(target)
        print(f"{len(self.sensors)} Sensors Loaded")
        print(f"{len(self.targets)} Targets Loaded")
        return self.sensors, self.targets
