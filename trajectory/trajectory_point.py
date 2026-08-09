from dataclasses import dataclass


@dataclass
class TrajectoryPoint:

    timestamp: float
    latitude: float
    longitude: float
    alt: float
    velocity: float
    acceleration: float
