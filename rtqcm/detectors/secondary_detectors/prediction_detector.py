from rtqcm.detectors.secondary_detectors.detector_interface import DetectorInterface
from rtqcm.models.qcm_model import QCMModel
class PredictionDetector(DetectorInterface):
    def __init__(self):
        pass

    def describe(self) -> str:
        raise NotImplementedError

    def detectAnomalies(self, model : QCMModel, time_frame: int) -> int:
        raise NotImplementedError