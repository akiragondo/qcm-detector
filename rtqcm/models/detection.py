from dataclasses import dataclass
from typing import List
import json
import pandas as pd

@dataclass
class Detection:
    timestamp: float
    frequency: float
    resistance: float
    period: List[float]
    time: str
    severity: str or None
    detector: str
    notified: bool = False

    def make_email_body(self, destination : str):
        assert(self.severity is not None)
        contamination = "severa" if self.severity == "severe" else "provável"
        time_obj = pd.to_datetime(self.timestamp,unit = 's')
        email = {
            "body": {
                "to": destination,
                "subject": contamination,
                "severity": contamination,
                "hour": time_obj.strftime("%H:%M"),
                "date": time_obj.strftime("%d/%m/%Y")
            }
        }
        email = json.dumps(email)
        return email
