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

