import numpy as np
from rtqcm.models.QCMModel import QCMModel
class DetectorInterface:
    def detectAnomalies(self, model : QCMModel, time_frame: int) -> int:
        pass

    def describe(self) -> str:
        pass