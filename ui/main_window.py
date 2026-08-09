from pathlib import Path

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QLabel,
    QFrame,
    QSplitter,
    QScrollArea,
    QSizePolicy,
)
from PySide6.QtCore import Qt

from widgets.video_panel import VideoPanel
from trajectory.trajectory_player import TrajectoryPlayer
from providers.excel_provider import ExcelProvider
from widgets.sensor_panel import SensorPanel
from widgets.map_container import MapContainer
from providers.mission_data import MissionData
from providers.trajectory_provider import TrajectoryProvider
from providers.fov_provider import FOVProvider


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # =====================================================
        # WINDOW
        # =====================================================

        self.setWindowTitle(
            "GeoFusion-Integrated-Geospatial-Visualization-and-Analysis-Platform"
        )

        self.resize(1600, 950)
        self.setMinimumSize(1200, 750)

        # =====================================================
        # DATA
        # =====================================================

        self.excel_provider = ExcelProvider()

        self.mission_data = MissionData()
        self.trajectory_provider = TrajectoryProvider()
        self.fov_provider = FOVProvider()

        self.fov_frames = []

        self.trajectory_player = TrajectoryPlayer()
        self.trajectory_player.positionChanged.connect(self.update_target_position)

        self.sensors = []
        self.targets = []
        self.trajectory = []
        self.map_data = []

        # =====================================================
        # CENTRAL WIDGET
        # =====================================================

        central = QWidget()
        central.setObjectName("centralWidget")
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)

        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(8)

        # =====================================================
        # HEADER
        # =====================================================

        header = self.create_header()
        main_layout.addWidget(header)

        # =====================================================
        # CONTROL BAR
        # =====================================================

        control_bar = self.create_control_bar()
        main_layout.addWidget(control_bar)

        # =====================================================
        # MAIN VERTICAL SPLITTER
        # =====================================================

        main_splitter = QSplitter(Qt.Vertical)

        # =====================================================
        # TOP SECTION
        # =====================================================

        top_splitter = QSplitter(Qt.Horizontal)

        # =====================================================
        # LEFT - DATA SOURCES
        # =====================================================

        source_container = self.create_section("DATA SOURCES")

        source_layout = source_container.layout()

        self.sensor_panel = SensorPanel()

        self.sensor_panel.sensorChanged.connect(self.sensor_updated)

        self.sensor_panel.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding,
        )

        source_layout.addWidget(self.sensor_panel)

        # =====================================================
        # CENTER - VIDEO MONITORING
        # =====================================================

        video_container = self.create_section("VIDEO VIEWER")

        video_layout = video_container.layout()

        self.video_panel = VideoPanel()

        self.video_panel.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding,
        )

        video_layout.addWidget(self.video_panel)

        # =====================================================
        # RIGHT - DATA SUMMARY
        # =====================================================

        information_container = self.create_information_panel()

        # =====================================================
        # TOP SECTIONS
        # =====================================================

        top_splitter.addWidget(source_container)
        top_splitter.addWidget(video_container)
        top_splitter.addWidget(information_container)

        top_splitter.setStretchFactor(0, 2)
        top_splitter.setStretchFactor(1, 5)
        top_splitter.setStretchFactor(2, 2)

        top_splitter.setSizes([320, 850, 360])

        # =====================================================
        # BOTTOM SECTION
        # =====================================================

        bottom_splitter = QSplitter(Qt.Horizontal)

        # =====================================================
        # SPATIAL VISUALIZATION
        # =====================================================

        map_container_frame = self.create_section("SPATIAL VISUALIZATION")

        map_layout = map_container_frame.layout()

        # -----------------------------------------------------
        # MAP TOOLBAR
        # -----------------------------------------------------

        map_toolbar = QHBoxLayout()

        map_title = QLabel("2D MAP / 3D TERRAIN")
        map_title.setObjectName("mapTitle")

        map_toolbar.addWidget(map_title)
        map_toolbar.addStretch()

        map_status = QLabel("Data • Objects • Path • View Geometry")
        map_status.setObjectName("mapStatus")

        map_toolbar.addWidget(map_status)

        map_layout.addLayout(map_toolbar)

        # =====================================================
        # MAP CONTAINER
        # =====================================================

        self.mapContainer = MapContainer()

        self.mapContainer.map2d.fovChanged.connect(self.update_3d_fov)

        self.mapContainer.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding,
        )

        map_layout.addWidget(
            self.mapContainer,
            1,
        )

        # =====================================================
        # ACTIVITY LOG
        # =====================================================

        event_container = self.create_event_panel()

        # =====================================================
        # BOTTOM SPLITTER
        # =====================================================

        bottom_splitter.addWidget(map_container_frame)
        bottom_splitter.addWidget(event_container)

        bottom_splitter.setStretchFactor(0, 5)
        bottom_splitter.setStretchFactor(1, 2)

        bottom_splitter.setSizes([1050, 400])

        # =====================================================
        # MAIN SPLITTER
        # =====================================================

        main_splitter.addWidget(top_splitter)
        main_splitter.addWidget(bottom_splitter)

        main_splitter.setStretchFactor(0, 5)
        main_splitter.setStretchFactor(1, 4)

        main_splitter.setSizes([520, 430])

        main_layout.addWidget(
            main_splitter,
            1,
        )

        # =====================================================
        # STYLE
        # =====================================================

        self.apply_style()

    # =========================================================
    # HEADER
    # =========================================================

    def create_header(self):

        frame = QFrame()
        frame.setObjectName("headerFrame")

        layout = QHBoxLayout(frame)

        layout.setContentsMargins(12, 6, 12, 6)

        # -----------------------------------------------------
        # Logo
        # -----------------------------------------------------

        logo = QLabel("◈")
        logo.setObjectName("logoLabel")

        layout.addWidget(logo)

        # -----------------------------------------------------
        # Title
        # -----------------------------------------------------

        title_layout = QVBoxLayout()

        title = QLabel("GEOVISTA")
        title.setObjectName("titleLabel")

        subtitle = QLabel("Offline Geospatial Visualization")
        subtitle.setObjectName("subtitleLabel")

        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)

        layout.addLayout(title_layout)

        layout.addStretch()

        # -----------------------------------------------------
        # Offline
        # -----------------------------------------------------

        local = QLabel("OFFLINE")
        local.setObjectName("offlineLabel")

        layout.addWidget(local)

        # -----------------------------------------------------
        # Ready
        # -----------------------------------------------------

        ready = QLabel("● READY")
        ready.setObjectName("readyLabel")

        layout.addWidget(ready)

        return frame

    # =========================================================
    # CONTROL BAR
    # =========================================================

    def create_control_bar(self):

        frame = QFrame()
        frame.setObjectName("controlFrame")

        layout = QHBoxLayout(frame)

        layout.setContentsMargins(8, 5, 8, 5)

        # -----------------------------------------------------
        # Load Data
        # -----------------------------------------------------

        self.loadButton = QPushButton("Load Data")
        self.loadButton.setObjectName("loadButton")

        self.loadButton.clicked.connect(self.load_excel)

        layout.addWidget(self.loadButton)

        # -----------------------------------------------------
        # Load Path
        # -----------------------------------------------------

        self.loadTrajectoryButton = QPushButton("Load Path")
        self.loadTrajectoryButton.setObjectName("pathButton")

        self.loadTrajectoryButton.clicked.connect(self.load_trajectory)

        layout.addWidget(self.loadTrajectoryButton)

        # -----------------------------------------------------
        # Load View Data
        # -----------------------------------------------------

        self.loadFOVButton = QPushButton("Load View Data")
        self.loadFOVButton.setObjectName("viewButton")

        self.loadFOVButton.clicked.connect(self.load_fov)

        layout.addWidget(self.loadFOVButton)

        layout.addStretch()

        # -----------------------------------------------------
        # Status
        # -----------------------------------------------------

        self.data_status = QLabel("No data loaded")
        self.data_status.setObjectName("dataStatus")

        layout.addWidget(self.data_status)

        return frame

    # =========================================================
    # GENERIC SECTION
    # =========================================================

    def create_section(self, title):

        frame = QFrame()
        frame.setObjectName("sectionFrame")

        layout = QVBoxLayout(frame)

        layout.setContentsMargins(
            7,
            7,
            7,
            7,
        )

        layout.setSpacing(5)

        title_label = QLabel(title)
        title_label.setObjectName("sectionTitle")

        layout.addWidget(title_label)

        return frame

    # =========================================================
    # DATA SUMMARY
    # =========================================================

    def create_information_panel(self):

        outer = self.create_section("DATA SUMMARY")

        main_layout = outer.layout()

        scroll = QScrollArea()

        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        content = QWidget()
        content.setObjectName("summaryContent")

        layout = QVBoxLayout(content)

        layout.setContentsMargins(
            4,
            4,
            4,
            4,
        )

        # -----------------------------------------------------
        # Data Status
        # -----------------------------------------------------

        status_title = QLabel("DATA STATUS")
        status_title.setObjectName("infoHeading")

        layout.addWidget(status_title)

        self.sensor_count = QLabel("Data Sources : 0")
        self.sensor_count.setObjectName("infoLabel")

        self.target_count = QLabel("Objects      : 0")
        self.target_count.setObjectName("infoLabel")

        self.trajectory_status = QLabel("Path         : Not Loaded")
        self.trajectory_status.setObjectName("statusYellow")

        self.fov_status = QLabel("View Data    : Not Loaded")
        self.fov_status.setObjectName("statusYellow")

        self.dem_status = QLabel("Terrain Data : Available")
        self.dem_status.setObjectName("statusGreen")

        for label in [
            self.sensor_count,
            self.target_count,
            self.trajectory_status,
            self.fov_status,
            self.dem_status,
        ]:
            layout.addWidget(label)

        # -----------------------------------------------------
        # Object Information
        # -----------------------------------------------------

        object_title = QLabel("OBJECT INFORMATION")
        object_title.setObjectName("infoHeading")

        layout.addWidget(object_title)

        self.target_info_layout = QVBoxLayout()

        layout.addLayout(self.target_info_layout)

        layout.addStretch()

        scroll.setWidget(content)

        main_layout.addWidget(
            scroll,
            1,
        )

        return outer

    # =========================================================
    # ACTIVITY LOG
    # =========================================================

    def create_event_panel(self):

        outer = self.create_section("ACTIVITY")

        layout = outer.layout()

        self.event_log = QLabel("Application initialized.\n" "Waiting for data...")

        self.event_log.setObjectName("eventLog")

        self.event_log.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.event_log.setWordWrap(True)

        layout.addWidget(
            self.event_log,
            1,
        )

        return outer

    # =========================================================
    # ACTIVITY UPDATE
    # =========================================================

    def add_event(self, message):

        current = self.event_log.text()

        if current.startswith("Application initialized."):
            current = ""

        self.event_log.setText(f"• {message}\n{current}")

    # =========================================================
    # OBJECT INFORMATION
    # =========================================================

    def update_target_information(self):

        while self.target_info_layout.count():

            item = self.target_info_layout.takeAt(0)

            widget = item.widget()

            if widget:
                widget.deleteLater()

        for target in self.targets:

            card = QFrame()
            card.setObjectName("objectCard")

            layout = QVBoxLayout(card)

            layout.setContentsMargins(
                7,
                7,
                7,
                7,
            )

            name = QLabel(str(target.name))
            name.setObjectName("objectName")

            layout.addWidget(name)

            lat = QLabel(f"Latitude  : " f"{target.latitude:.6f}")

            lon = QLabel(f"Longitude : " f"{target.longitude:.6f}")

            alt = QLabel(f"Elevation : " f"{target.elevation}")

            for label in [
                lat,
                lon,
                alt,
            ]:

                label.setObjectName("objectDetail")

                layout.addWidget(label)

            self.target_info_layout.addWidget(card)

    # =========================================================
    # LOAD DATA
    # =========================================================

    def load_excel(self):

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select Data File",
            "",
            "Excel Files (*.xlsx *.xls)",
        )

        if not filename:
            return

        try:

            sensors, targets = self.excel_provider.load_excel(filename)

            self.mission_data.update(sensors, targets)

            self.sensors = sensors
            self.targets = targets

            self.sensor_panel.set_sensors(self.mission_data.get_sensors())

            self.map_data.clear()

            for sensor in self.mission_data.get_sensors():

                self.map_data.append(
                    {
                        "name": sensor.name,
                        "lat": sensor.latitude,
                        "lon": sensor.longitude,
                        "elevation": sensor.elevation,
                        "color": "blue",
                    }
                )

            for target in self.mission_data.get_targets():

                self.map_data.append(
                    {
                        "name": target.name,
                        "lat": target.latitude,
                        "lon": target.longitude,
                        "elevation": target.elevation,
                        "color": "red",
                    }
                )

            self.mapContainer.show_data(
                self.mission_data.get_sensors(),
                self.mission_data.get_targets(),
            )

            self.sensor_count.setText(f"Data Sources : {len(sensors)}")

            self.target_count.setText(f"Objects      : {len(targets)}")

            self.update_target_information()

            self.data_status.setText(
                f"{len(sensors)} Sources • " f"{len(targets)} Objects Loaded"
            )

            self.add_event(
                f"{len(sensors)} data sources and " f"{len(targets)} objects loaded"
            )

            QMessageBox.information(
                self,
                "Data Loaded",
                f"{len(sensors)} Data Sources Loaded\n"
                f"{len(targets)} Objects Loaded",
            )

        except Exception as e:

            QMessageBox.critical(self, "Loading Error", str(e))

            self.add_event(f"Data loading failed: {e}")

    # =========================================================
    # LOAD PATH DATA
    # =========================================================

    def load_trajectory(self):

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select Path Data",
            "",
            "Excel Files (*.xlsx *.xls)",
        )

        if not filename:
            return

        try:

            self.trajectory = self.trajectory_provider.load_trajectory(filename)

            self.mapContainer.show_trajectory(self.trajectory)

            self.trajectory_player.load(self.trajectory)

            self.trajectory_player.play(10)

            self.trajectory_status.setText(
                f"Path : Loaded " f"({len(self.trajectory)} points)"
            )

            self.trajectory_status.setObjectName("statusGreen")

            self.trajectory_status.style().unpolish(self.trajectory_status)
            self.trajectory_status.style().polish(self.trajectory_status)

            self.add_event(f"Path data loaded: " f"{len(self.trajectory)} points")

            QMessageBox.information(
                self,
                "Path Data Loaded",
                f"{len(self.trajectory)} " f"path points loaded",
            )

            print("Path First Point:", self.trajectory[0])

            print("TOTAL POINTS:", len(self.trajectory))

        except Exception as e:

            QMessageBox.critical(self, "Path Data Error", str(e))

            self.add_event(f"Path data error: {e}")

    # =========================================================
    # SOURCE UPDATED
    # =========================================================

    def sensor_updated(self, sensor):

        print(
            "Source settings changed:",
            sensor.name,
            sensor.heading,
            sensor.fov,
            sensor.detection_range,
        )

        self.mapContainer.map2d.show_sensors(self.sensors)

        self.add_event(f"Source settings updated: " f"{sensor.name}")

    # =========================================================
    # OBJECT POSITION
    # =========================================================

    def update_target_position(self, point):

        self.mapContainer.map2d.move_target(
            point.latitude,
            point.longitude,
        )

        self.mapContainer.move_target(
            "",
            point.latitude,
            point.longitude,
            point.alt,
        )

        print(
            "Object position:",
            point.latitude,
            point.longitude,
            point.alt,
        )

    # =========================================================
    # LOAD VIEW DATA
    # =========================================================

    def load_fov(self):

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select View Data",
            "",
            "Excel Files (*.xlsx *.xls)",
        )

        if not filename:
            return

        try:

            self.fov_frames = self.fov_provider.load_excel(filename)

            print("VIEW DATA COUNT:", len(self.fov_frames))

            if self.fov_frames:

                print("FIRST VIEW DATA:", self.fov_frames[0])

                self.mapContainer.show_fov(self.fov_frames)

            self.fov_status.setText(f"View Data : " f"{len(self.fov_frames)} Loaded")

            self.fov_status.setObjectName("statusGreen")

            self.fov_status.style().unpolish(self.fov_status)
            self.fov_status.style().polish(self.fov_status)

            self.add_event(f"View data loaded: " f"{len(self.fov_frames)} frames")

            QMessageBox.information(
                self,
                "View Data Loaded",
                f"{len(self.fov_frames)} " f"frames loaded",
            )

        except Exception as e:

            QMessageBox.critical(self, "View Data Error", str(e))

            self.add_event(f"View data loading error: {e}")

    # =========================================================
    # UPDATE 3D VIEW
    # =========================================================

    def update_3d_fov(self, frame):

        self.mapContainer.plot_fov(frame)

    # =========================================================
    # STATIC VIEW
    # =========================================================

    def plot_static_fov(self, sensor):

        data = {
            "name": sensor.name,
            "lat": sensor.latitude,
            "lon": sensor.longitude,
            "heading": sensor.heading,
            "fov": sensor.fov,
            "range": sensor.detection_range,
        }

        # Reserved for map visualization.

    # =========================================================
    # APPLICATION STYLE
    # =========================================================

    def apply_style(self):

        style_path = Path(__file__).resolve().parent / "styles" / "main_window.qss"

        try:

            with open(style_path, "r", encoding="utf-8") as file:

                self.setStyleSheet(file.read())

        except Exception as e:

            print("Could not load stylesheet:", e)
