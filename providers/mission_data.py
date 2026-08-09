class MissionData:

    def __init__(self):

        self.sensors = []
        self.targets = []

    def update(self, sensors, targets):

        self.sensors = sensors
        self.targets = targets

    def get_sensors(self):

        return self.sensors

    def get_targets(self):

        return self.targets

    def clear(self):

        self.sensors.clear()
        self.targets.clear()
