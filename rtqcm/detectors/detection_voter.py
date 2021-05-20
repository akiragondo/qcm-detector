import datetime

from rtqcm.detectors.secondary_detectors.mean_detector import MeanDetector
from rtqcm.detectors.secondary_detectors.prediction_detector import PredictionDetector
from rtqcm.models.detection import Detection
from rtqcm.models.qcm_model import QCMModel
import pandas as pd

class DetectionVoter:
    """
    Class responsible for:
        - Making detections with all detectors available
        - Voting whether or not the detections are valid
        - Making the detection
        - Comparing the detection to previous ones to see if it hasn't already been detected
    """
    def __init__(
            self,
            run_controller
        ):
        self.mean_detector = MeanDetector(
            lag_time=15,
            moving_average_time=10,
            detection_threshold=1.5,
            parent_controller=run_controller
        )
        self.prediction_detector = PredictionDetector()
        self.run_controller = run_controller
        self.dataframe_model = None

    def make_dataframe_from_model(self, qcm_model: QCMModel):
        index = pd.to_datetime(qcm_model.timestamps, unit='s') - pd.Timedelta('03:00:00')
        dataframe = pd.DataFrame(
            data=zip(qcm_model.resistances, qcm_model.frequencies),
            index=index,
            columns= ['Frequency', 'Resistance']
        )
        return dataframe

    def detect(self) -> Detection:
        self.dataframe_model = self.make_dataframe_from_model(self.run_controller.data_model)
        mean_detection = self.mean_detector.detectAnomaly()