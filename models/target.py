from dataclasses import dataclass
@dataclass
class Target:
    """
    Represents one target.
    """
    name: str

    latitude: float

    longitude: float

    elevation: float = 0.0

    def to_dict(self):

        return {
            "name": self.name,
            "lat": self.latitude,
            "lon": self.longitude,
            "elevation": self.elevation,
        }
