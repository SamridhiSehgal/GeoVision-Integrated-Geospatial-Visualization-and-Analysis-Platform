from PySide6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QFileDialog, QLabel

from PySide6.QtCore import Signal


class VideoSourceManager(QDialog):

    # sends selected video path back
    videoAdded = Signal(str)

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Video Source Manager")

        self.resize(400, 200)

        layout = QVBoxLayout()

        title = QLabel("Add Video Feed Source")

        title.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
            """)

        self.addButton = QPushButton("Select Video File")

        self.addButton.clicked.connect(self.select_video)

        layout.addWidget(title)

        layout.addWidget(self.addButton)

        self.setLayout(layout)

    def select_video(self):

        file, _ = QFileDialog.getOpenFileName(
            self, "Select Video", "", "Video Files (*.mp4 *.avi *.mkv)"
        )

        if file:

            self.videoAdded.emit(file)

            self.close()


CameraManager = VideoSourceManager
