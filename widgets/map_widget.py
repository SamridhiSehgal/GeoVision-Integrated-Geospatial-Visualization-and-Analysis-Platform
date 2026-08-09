from pathlib import Path
import json
from tracemalloc import start
from PySide6.QtCore import QUrl, QTimer, Signal

from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import (
    QWebEnginePage,
    QWebEngineSettings,
)
import math

from models import sensor


class DebugPage(QWebEnginePage):

    def javaScriptConsoleMessage(self, level, message, line, source):
        print(f"JS [{line}] {message}")


class MapWidget(QWebEngineView):

    fovChanged = Signal(dict)

    def __init__(self):
        super().__init__()
        self.loadFinished.connect(self.on_loaded)
        self.setPage(DebugPage(self))

        settings = self.settings()

        settings.setAttribute(
            QWebEngineSettings.LocalContentCanAccessRemoteUrls,
            True,
        )

        settings.setAttribute(
            QWebEngineSettings.LocalContentCanAccessFileUrls,
            True,
        )

        self.load_map()
        self.mission_frames = []
        self.current_frame = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.nextMissionFrame)
        # FOV animation
        self.fov_frames = []
        self.fov_index = 0

        self.fov_timer = QTimer()
        self.fov_timer.timeout.connect(self.next_fov_frame)

    def load_map(self):

        html = Path("maps/map.html").resolve()

        self.load(QUrl.fromLocalFile(str(html)))

    def reload(self):
        """
        Called after switching back from 3D.
        """
        self.load_map()

    def show_targets(self, targets):

        target_data = []

        for t in targets:

            target_data.append(
                {
                    "name": t.name,
                    "lat": t.latitude,
                    "lon": t.longitude,
                    "elevation": t.elevation,
                    "color": "red",
                }
            )

        js = f"""
        if(typeof loadTargets === "function"){{
            loadTargets({json.dumps(target_data)});
        }}
        """

        self.page().runJavaScript(js)

    def show_sensors(self, sensors):

        sensor_data = []

        for s in sensors:

            sensor_data.append(
                {
                    "name": s.name,
                    "lat": s.latitude,
                    "lon": s.longitude,
                    "heading": float(s.heading) if s.heading is not None else 0,
                    "fov": float(s.fov) if s.fov is not None else 0,
                    "range": (
                        float(s.detection_range) if s.detection_range is not None else 0
                    ),
                }
            )

        js = f"""
        if(typeof loadSensors === "function"){{
            loadSensors({json.dumps(sensor_data)});
        }}
        """

        self.page().runJavaScript(js)

    def show_trajectory(self, trajectory):

        points = []

        for p in trajectory:

            points.append([float(p.latitude), float(p.longitude)])

        print("JS TRAJECTORY:", points)

        js = f"""
        loadTrajectory({points});
        """

        self.page().runJavaScript(js)

    def on_loaded(self, ok):

        print("MAP LOADED:", ok)

    # def update_target_position(self, point):

    #   self.mapContainer.map2d.update_target_position(point)

    # self.page().runJavaScript(js)
    def move_target(self, lat, lon):

        js = f"""
        moveTarget({lat}, {lon});
        """

        self.page().runJavaScript(js)

    def plot_fov(self, frame):

        sensor = {
            "lat": frame["sensor_lat"],
            "lon": frame["sensor_lon"],
            "heading": frame.get("azimuth", 0),
            "fov": frame.get("fov", 30),
            "range": frame.get("range", 5000),
        }

        # Draw ANIMATED FOV from FOV Excel only
        js = f"""
        if(typeof drawAnimatedFOV === "function"){{
        drawAnimatedFOV({json.dumps(sensor)});
    }}
    """

        self.page().runJavaScript(js)

        # Draw sensor + target dots
        self.show_fov_sensor_target(frame)

        # Send frame to 3D
        self.fovChanged.emit(frame)

    def updateMissionFrame(self, frame):

        sensor_lat = frame["sensor_lat"]
        sensor_lon = frame["sensor_lon"]

        target_lat = frame["target_lat"]
        target_lon = frame["target_lon"]

        # Move sensor in 2D map
        self.page().runJavaScript(f"animateMissionSensor({sensor_lat}, {sensor_lon});")

        # Move target in 2D map
        self.page().runJavaScript(f"animateMissionTarget({target_lat}, {target_lon});")

    def startMission(self, frames):

        self.mission_frames = frames
        self.current_frame = 0

        # clear previous animation
        self.page().runJavaScript("resetMissionAnimation();")

        self.timer.start(1000)

    def nextMissionFrame(self):

        if self.current_frame >= len(self.mission_frames):
            self.timer.stop()
            return

        frame = self.mission_frames[self.current_frame]

        self.updateMissionFrame(frame)

        self.plot_fov(frame)

        self.current_frame += 1

    def start_fov_animation(self, frames):

        self.fov_frames = frames
        self.fov_index = 0

        print("START FOV ANIMATION:", len(frames))

        self.fov_timer.start(1000)

    def next_fov_frame(self):

        if self.fov_index >= len(self.fov_frames):

            self.fov_timer.stop()
            print("FOV ANIMATION COMPLETE")
            return

        frame = self.fov_frames[self.fov_index]

        self.plot_fov(frame)

        self.fov_index += 1

    def show_fov_sensor_target(self, frame):

        data = {
            "sensor_lat": frame["sensor_lat"],
            "sensor_lon": frame["sensor_lon"],
            "target_lat": frame["target_lat"],
            "target_lon": frame["target_lon"],
        }

        js = f"""
        if(typeof showFOVSensorTarget === "function"){{
            showFOVSensorTarget({json.dumps(data)});
        }}
    
        """

        self.page().runJavaScript(js)

    def plot_static_fov(self, sensor):

        data = {
            "lat": sensor.latitude,
            "lon": sensor.longitude,
            "heading": sensor.heading,
            "fov": sensor.fov,
            "range": sensor.detection_range,
        }

        js = f"""
    if(typeof drawStaticFOV === "function"){{
        drawStaticFOV({json.dumps(data)});
    }}
    """

        self.page().runJavaScript(js)
