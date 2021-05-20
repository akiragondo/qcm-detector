import pandas as pd

class DetectorInterface:
    def detect_anomalies(self, detection_dataframe: pd.DataFrame) -> int:
        pass

    def describe(self) -> str:
        pass