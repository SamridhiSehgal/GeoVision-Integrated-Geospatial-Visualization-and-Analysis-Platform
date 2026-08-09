from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QStackedWidget,
)

from widgets.map_widget import MapWidget
from widgets.terrain_widget import TerrainWidget


class MapContainer(QWidget):

    def __init__(self):

        super().__init__()

        self.terrain_loaded = False

        self.current_sensors = []
        self.current_targets = []

        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(0, 0, 0, 0)

        # ---------------- Toolbar ----------------

        toolbar = QHBoxLayout()

        self.btn2d = QPushButton("2D Map")

        self.btn3d = QPushButton("3D Terrain")

        toolbar.addWidget(self.btn2d)

        toolbar.addWidget(self.btn3d)

        toolbar.addStretch()

        main_layout.addLayout(toolbar)

        # ---------------- Views ----------------

        self.stack = QStackedWidget()

        self.map2d = MapWidget()

        self.map3d = TerrainWidget()

        self.map2d.fovChanged.connect(self.map3d.plot_fov)

        self.stack.addWidget(self.map2d)

        self.stack.addWidget(self.map3d)

        main_layout.addWidget(self.stack)

        self.btn2d.clicked.connect(self.show_2d)

        self.btn3d.clicked.connect(self.show_3d)

    # ===================================================

    def show_2d(self):

        self.stack.setCurrentIndex(0)

        self.map2d.show_sensors(self.current_sensors)

        self.map2d.show_targets(self.current_targets)

    # ===================================================

    def show_3d(self):

        if not self.terrain_loaded:

            self.map3d.load_dem("terrain/gt30e060n40_UTM.tif")

            self.terrain_loaded = True

        self.stack.setCurrentIndex(1)
        # Show first FOV if already loaded

        if hasattr(self, "current_fov"):

            self.map3d.plot_fov(self.current_fov)

        if self.current_sensors:

            self.map3d.show_sensors(self.current_sensors)

        if self.current_targets:

            self.map3d.show_targets(self.current_targets)

        if hasattr(self, "current_trajectory"):

            self.map3d.show_trajectory(self.current_trajectory)

        if hasattr(self, "current_fov_frames"):

            self.map3d.start_fov_animation(self.current_fov_frames)

    # ===================================================

    def show_data(
        self,
        sensors,
        targets,
    ):

        self.current_sensors = sensors

        self.current_targets = targets

        # ---------- 2D ----------

        self.map2d.show_sensors(sensors)

        self.map2d.show_targets(targets)

        # ---------- 3D ----------

        # If 3D already loaded,
        # update immediately

        if self.terrain_loaded:

            self.map3d.show_sensors(sensors)

            self.map3d.show_targets(targets)

    # ===================================================

    def show_trajectory(self, trajectory):
        self.current_trajectory = trajectory

        # 2D trajectory
        self.map2d.show_trajectory(trajectory)

        # 3D trajectory
        if self.terrain_loaded:

            self.map3d.show_trajectory(trajectory)

        else:

            print("3D terrain not loaded, trajectory waiting")

    def move_target(
        self,
        name,
        latitude,
        longitude,
        altitude,
    ):

        if self.terrain_loaded:

            self.map3d.move_target(name, latitude, longitude, altitude)

    # ===================================================

    def current_view(self):

        if self.stack.currentIndex() == 0:

            return "2D"

        return "3D"

    def reset_animation(self):

        if self.terrain_loaded:

            self.map3d.reset_animation()

    # ==========================================================
    # ==========================================================
    # SHOW FOV
    # ==========================================================

    # ==========================================================
    # SHOW FOV ANIMATION
    # ==========================================================

    def show_fov(self, frames):

        print("MAP CONTAINER FOV:", len(frames))

        self.current_fov_frames = frames
        self.current_fov = frames[0]

        # 2D FOV animation
        self.map2d.start_fov_animation(frames)

        # Start 3D only if terrain is already loaded
        if self.terrain_loaded:

            self.map3d.start_fov_animation(frames)

    def plot_fov(self, frame):

        self.current_fov = frame

        if self.terrain_loaded:

            self.map3d.plot_fov(frame)

        else:

            print("3D terrain not loaded")
