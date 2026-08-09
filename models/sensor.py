from dataclasses import dataclass
from typing import Optional
@dataclass
class Sensor:
    """
    Represents one sensor/radar.
    """
    # Information loaded from Excel
    name: str
    latitude: float
    longitude: float
    # Configurable Sensor Settings
    elevation: Optional[float] = None
    heading: Optional[float] = None
    fov: Optional[float] = None
    detection_range: Optional[float] = None
    mode: Optional[str] = None

