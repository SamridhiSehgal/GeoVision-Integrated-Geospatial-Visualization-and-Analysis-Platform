from PySide6.QtCore import QObject, QTimer, Signal


class TrajectoryPlayer(QObject):

    positionChanged = Signal(object)
    finished = Signal()

    def __init__(self):
        super().__init__()

        self.points = []
        self.index = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.next_point)

    def load(self, points):
        self.points = points
        self.index = 0

    def play(self, interval=100):
        if not self.points:
            return

        self.timer.start(interval)

    def stop(self):
        self.timer.stop()

    def next_point(self):

        print("Index:", self.index)

        if self.index >= len(self.points):
            self.timer.stop()
            self.finished.emit()
            return

        self.positionChanged.emit(self.points[self.index])

        self.index += 1