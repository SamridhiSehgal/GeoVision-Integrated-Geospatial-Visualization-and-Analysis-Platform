from PySide6.QtWidgets import QWidget, QVBoxLayout

from terrain.dem_loader import DEMLoader
from terrain.terrain_renderer import TerrainRenderer


class TerrainWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.renderer = None
        self.loaded = False

    # --------------------------------------------------

    def load_dem(self, dem_path):

        if self.loaded:
            return

        print("Loading DEM...")

        loader = DEMLoader(dem_path)

        terrain = loader.load()

        print("DEM Loaded")

        self.renderer = TerrainRenderer(terrain, self)

        self.layout.addWidget(self.renderer.widget())

        self.loaded = True

        print("Terrain Ready")

    # --------------------------------------------------

    def show_sensors(self, sensors):

        if self.renderer is None:
            return

        for sensor in sensors:

            self.renderer.add_sensor(
                sensor.name,
                sensor.latitude,
                sensor.longitude,
            )

        print(f"{len(sensors)} Sensors Added")

    # --------------------------------------------------

    def show_targets(self, targets):

        if self.renderer is None:
            return

        for target in targets:

            self.renderer.add_target(
                target.name,
                target.latitude,
                target.longitude,
            )

        print(f"{len(targets)} Targets Added")

    def show_trajectory(self, trajectory):

        self.renderer.draw_trajectory(trajectory)

    def move_target(self, name, latitude, longitude, altitude):

        self.renderer.move_target(name, latitude, longitude, altitude)

    def reset_animation(self):

        self.renderer.reset_animation()

    # -----------------------------------
    # Display FOV in 3D
    # -----------------------------------

    def plot_fov(self, frame):

        if self.renderer is None:
            print("Renderer not ready")
            return

        self.renderer.plot_fov(frame)

    # ----------------------------------

    def start_fov_animation(self, frames):

        if self.renderer is None:
            print("Renderer not loaded, FOV animation waiting")
            return

        print("STARTING 3D FOV ANIMATION:", len(frames))

        self.renderer.start_fov_animation(frames)


