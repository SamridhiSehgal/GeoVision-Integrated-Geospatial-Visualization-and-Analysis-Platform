from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QSizePolicy,
)

from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import QUrl, Signal, Qt


class VideoWidget(QWidget):

    removeCamera = Signal(object)
    enlargeCamera = Signal(object)

    def __init__(self, camera_name, video_path):

        super().__init__()

        self.video_path = video_path
        self.camera_name = camera_name

        self.player = QMediaPlayer(self)

        self.video_display = QVideoWidget()

        self.player.setVideoOutput(self.video_display)
        self.video_display.setAspectRatioMode(Qt.KeepAspectRatio)

        self.video_display.setMinimumSize(500, 300)

        self.video_display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Camera title

        self.camera_label = QLabel(camera_name)

        self.status = QLabel("● READY")

        self.status.setStyleSheet("color:green;font-weight:bold;")

        title = QHBoxLayout()

        title.addWidget(self.camera_label)

        title.addStretch()

        title.addWidget(self.status)

        # Buttons

        self.play_btn = QPushButton("▶")
        self.pause_btn = QPushButton("⏸")
        self.stop_btn = QPushButton("⏹")
        self.remove_btn = QPushButton("✖")

        self.play_btn.clicked.connect(self.play_video)

        self.pause_btn.clicked.connect(self.pause_video)

        self.stop_btn.clicked.connect(self.stop_video)

        self.remove_btn.clicked.connect(lambda: self.removeCamera.emit(self))

        buttons = QHBoxLayout()

        buttons.addWidget(self.play_btn)
        buttons.addWidget(self.pause_btn)
        buttons.addWidget(self.stop_btn)
        buttons.addWidget(self.remove_btn)

        layout = QVBoxLayout()

        layout.addLayout(title)

        layout.addWidget(self.video_display, 1)

        layout.addLayout(buttons)

        self.setLayout(layout)

    # double click camera

    def mouseDoubleClickEvent(self, event):

        self.enlargeCamera.emit(self)

        event.accept()

    def play_video(self):

        self.player.setSource(QUrl.fromLocalFile(self.video_path))

        self.player.play()

        self.status.setText("● PLAYING")

    def pause_video(self):

        self.player.pause()

        self.status.setText("● PAUSED")

    def stop_video(self):

        self.player.stop()

        self.status.setText("● STOPPED")
