from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QGridLayout,
    QScrollArea,
    QPushButton,
    QFileDialog,
    QMessageBox,
)

from widgets.video_widget import VideoWidget


class VideoPanel(QWidget):

    def __init__(self):

        super().__init__()

        main_layout = QVBoxLayout()

        # ==========================
        # TITLE
        # ==========================

        title = QLabel("VIDEO MONITORING PANEL")

        title.setStyleSheet("""
            font-size:20px;
            font-weight:bold;
            """)

        main_layout.addWidget(title)

        # ==========================
        # LOAD BUTTON
        # ==========================

        self.load_button = QPushButton("Load Video Feeds")

        self.load_button.clicked.connect(self.load_videos)

        main_layout.addWidget(self.load_button)

        # ==========================
        # SCROLL AREA
        # ==========================

        self.scroll = QScrollArea()

        self.scroll.setWidgetResizable(True)

        self.container = QWidget()

        self.grid = QGridLayout(self.container)

        self.grid.setSpacing(5)

        self.scroll.setWidget(self.container)

        main_layout.addWidget(self.scroll)

        self.setLayout(main_layout)

        # ==========================
        # DATA
        # ==========================

        self.video_widgets = []

        self.expanded_camera = None

        self.restore_button = None

    # ==========================
    # LOAD VIDEOS
    # ==========================

    def load_videos(self):

        files, _ = QFileDialog.getOpenFileNames(
            self, "Select Video Feeds", "", "Video Files (*.mp4 *.avi *.mkv)"
        )

        if not files:

            return

        # minimum 9

        if len(files) < 9:

            QMessageBox.warning(self, "Video Count", "Please select minimum 9 videos")

            return

        # maximum 15

        files = files[:15]

        # clear old videos

        for widget in self.video_widgets:

            widget.deleteLater()

        self.video_widgets.clear()

        self.expanded_camera = None

        # create cameras

        for index, path in enumerate(files):

            video = VideoWidget(f"Camera {index+1}", path)

            video.removeCamera.connect(self.remove_camera)

            video.enlargeCamera.connect(self.enlarge_camera)

            self.video_widgets.append(video)

        self.refresh_grid()

    # ==========================
    # REMOVE CAMERA
    # ==========================

    def remove_camera(self, camera):

        if camera in self.video_widgets:

            self.video_widgets.remove(camera)

            camera.deleteLater()

        self.expanded_camera = None

        self.refresh_grid()

    # ==========================
    # REFRESH GRID
    # ==========================

    def refresh_grid(self):

        # clear layout

        while self.grid.count():

            item = self.grid.takeAt(0)

            widget = item.widget()

            if widget:

                widget.setParent(None)

        # rebuild

        for index, video in enumerate(self.video_widgets):

            row = index // 2

            col = index % 2

            self.grid.addWidget(video, row, col)

    # ==========================
    # ENLARGE CAMERA
    # ==========================

    def enlarge_camera(self, camera):

        # already enlarged

        if self.expanded_camera == camera:

            self.restore_grid()

            return

        self.expanded_camera = camera

        # hide others

        for widget in self.video_widgets:

            if widget != camera:

                widget.hide()

        camera.show()

        self.grid.removeWidget(camera)

        self.grid.addWidget(camera, 0, 0, 1, 2)

        # restore button

        if self.restore_button is None:

            self.restore_button = QPushButton("Restore Cameras")

            self.restore_button.clicked.connect(self.restore_grid)

        self.restore_button.show()

        self.grid.addWidget(self.restore_button, 1, 0, 1, 2)

    # ==========================
    # RESTORE GRID
    # ==========================

    def restore_grid(self):

        self.expanded_camera = None

        if self.restore_button:

            self.restore_button.hide()

        for widget in self.video_widgets:

            widget.show()

        self.refresh_grid()
