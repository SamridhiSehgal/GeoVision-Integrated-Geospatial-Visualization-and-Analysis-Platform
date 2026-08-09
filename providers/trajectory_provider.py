from trajectory.trajectory_loader import TrajectoryLoader

class TrajectoryProvider:

    def __init__(self):

        self.loader = TrajectoryLoader()

        self.points = []

    def load_trajectory(self, filename):

        self.points = self.loader.load(filename)

        return self.points

