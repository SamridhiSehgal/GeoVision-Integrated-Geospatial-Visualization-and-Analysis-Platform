from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
)
from dialogs.sensor_settings import SensorSettingsDialog


class SensorPanel(QWidget):
    """
    Displays loaded sensors and allows editing them.
    """

    sensorChanged = Signal(object)

    def __init__(self):
        super().__init__()
        self.sensors = []
        self.current_sensor = None
        layout = QVBoxLayout(self)
        # Title
        title = QLabel("Sensors")
        title.setStyleSheet("""
            font-size:16px;
            font-weight:bold;
            """)
        layout.addWidget(title)
        # Sensor List
        self.sensorList = QListWidget()
        self.sensorList.currentRowChanged.connect(self.sensor_selected)
        layout.addWidget(self.sensorList)

        # Information
        self.headingLabel = QLabel("Heading : -")
        self.fovLabel = QLabel("FOV : -")
        self.rangeLabel = QLabel("Range : -")
        self.modeLabel = QLabel("Mode : -")
        self.losLabel = QLabel("LOS : -")
        layout.addWidget(self.headingLabel)
        layout.addWidget(self.fovLabel)
        layout.addWidget(self.rangeLabel)
        layout.addWidget(self.modeLabel)
        layout.addWidget(self.losLabel)
        # Settings Button

        self.settingsButton = QPushButton("Settings")
        self.settingsButton.clicked.connect(self.open_settings)
        layout.addWidget(self.settingsButton)
        layout.addStretch()

    def set_sensors(self, sensors):
        self.sensors = sensors
        self.sensorList.clear()
        for sensor in sensors:
            self.sensorList.addItem(sensor.name)
        if sensors:
            self.sensorList.setCurrentRow(0)

    def sensor_selected(self, index):
        if index < 0:
            return
        self.current_sensor = self.sensors[index]
        self.update_information()

    def update_information(self):
        s = self.current_sensor
        self.headingLabel.setText(f"Heading : {s.heading}")
        self.fovLabel.setText(f"FOV : {s.fov}")
        self.rangeLabel.setText(f"Range : {s.detection_range}")

        # self.modeLabel.setText(f"Mode : {s.mode}")
        # self.losLabel.setText(f"LOS : {s.los_status}")

    def open_settings(self):

        if self.current_sensor is None:
            return

        dialog = SensorSettingsDialog(self.current_sensor, self)

        if dialog.exec():

            self.update_information()

            # send updated sensor to main window
            self.sensorChanged.emit(self.current_sensor)
