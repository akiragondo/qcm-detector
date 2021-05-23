from rtqcm.detectors.secondary_detectors.detector import Detector
from rtqcm.models.qcm_model import QCMModel
class PredictionDetector(Detector):
    def __init__(self):
        pass

    def describe(self) -> str:
        raise NotImplementedError

    def detectAnomalies(self, model : QCMModel, time_frame: int) -> int:
        raise NotImplementedError