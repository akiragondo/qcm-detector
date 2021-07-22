from rtqcm.detectors.secondary_detectors.detector import Detector
import pandas as pd
from rtqcm.models.detection import Detection
from typing import List
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing


class PredictionDetector(Detector):
    def __init__(self):
        self.initial_sample_time = 15  # Minimum sample time in minutes
        self.forecast_time_step = 12  # Forecast time in minutes
        self.error_threshold = 1  # Percent error threshold for each forecast

        self.prediction_model = None
        self.last_forecast_start_time = None
        self.previous_forecast = pd.DataFrame()

    def describe(self) -> str:
        return 'Expo-predict'

    def reset(self):
        self.prediction_model = None
        self.last_forecast_start_time = None
        self.previous_forecast = pd.DataFrame()

    def detect_anomalies(self, detection_dataframe: pd.DataFrame) -> List[Detection]:
        resistance_endog = detection_dataframe['Resistance']
        self.prediction_model = ExponentialSmoothing(
            endog=resistance_endog,
            trend='add',
            damped_trend=False,
            seasonal=None
        ).fit()
        detection_times = []
        if not self.previous_forecast.empty:
            error_df = np.abs((resistance_endog[
                        self.last_forecast_start_time:] - self.previous_forecast) * 100 / self.previous_forecast)
            error_df = error_df.dropna()
            detection_times = [time for time, error in error_df.iteritems() if error > self.error_threshold]
        self.previous_forecast = self.prediction_model.forecast(self.forecast_time_step)
        self.last_forecast_start_time = self.previous_forecast.index[0]
        detections = [self.make_detection_from_element(
            dataframe=detection_dataframe,
            index=detection_time,
            detector=self.describe()
        ) for detection_time in detection_times]
        return detections
