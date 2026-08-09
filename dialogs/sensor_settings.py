from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLabel,
    QPushButton,
    QDialogButtonBox,
    QDoubleSpinBox,
    QRadioButton,
    QHBoxLayout,
)
from models.sensor import Sensor


class SensorSettingsDialog(QDialog):
    """
    Dialog for editing one sensor.
    """

    def __init__(self, sensor: Sensor, parent=None):
        super().__init__(parent)
        self.sensor = sensor
        self.setWindowTitle(f"Sensor Settings - {sensor.name}")
        self.setMinimumWidth(350)

        layout = QVBoxLayout(self)
        form = QFormLayout()
        # Heading
        self.headingSpin = QDoubleSpinBox()
        self.headingSpin.setRange(0, 360)
        self.headingSpin.setSuffix(" °")
        self.headingSpin.setDecimals(1)
        if sensor.heading is not None:
            self.headingSpin.setValue(sensor.heading)
        form.addRow("Heading", self.headingSpin)
        # FOV
        self.fovSpin = QDoubleSpinBox()
        self.fovSpin.setRange(1, 360)
        self.fovSpin.setSuffix(" °")
        self.fovSpin.setDecimals(1)
        if sensor.fov is not None:
            self.fovSpin.setValue(sensor.fov)
        form.addRow("FOV", self.fovSpin)
        # Detection Range
        self.rangeSpin = QDoubleSpinBox()
        self.rangeSpin.setRange(1, 100000)
        self.rangeSpin.setSuffix(" m")
        self.rangeSpin.setDecimals(1)
        if sensor.detection_range is not None:
            self.rangeSpin.setValue(sensor.detection_range)
        form.addRow("Detection Range", self.rangeSpin)
        # Mode
        modeLayout = QHBoxLayout()
        self.manualRadio = QRadioButton("Manual")
        self.agcRadio = QRadioButton("AGC")
        if sensor.mode == "AGC":
            self.agcRadio.setChecked(True)
        else:
            self.manualRadio.setChecked(True)
        modeLayout.addWidget(self.manualRadio)
        modeLayout.addWidget(self.agcRadio)
        form.addRow("Mode", modeLayout)

        layout.addLayout(form)
        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Apply | QDialogButtonBox.Cancel)
        buttons.button(QDialogButtonBox.Apply).clicked.connect(self.apply_changes)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    # Apply
    def apply_changes(self):
        self.sensor.heading = self.headingSpin.value()
        self.sensor.fov = self.fovSpin.value()
        self.sensor.detection_range = self.rangeSpin.value()
        print("Sensor Updated:")
        print("Heading:", self.sensor.heading)
        print("FOV:", self.sensor.fov)
        print("Range:", self.sensor.detection_range)
        self.accept()
