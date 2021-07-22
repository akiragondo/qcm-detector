from dataclasses import dataclass
from typing import List


@dataclass
class Detection:
    timestamp: float
    frequency: float
    resistance: float
    period: List[float]
    time: str
    severity: str or None
    detector: str
