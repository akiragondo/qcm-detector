from dataclasses import dataclass
from typing import List


@dataclass
class Detection:
    timestamp: float
    period: List[float]
    severity: str or None
    frequency: float
    resistance: float