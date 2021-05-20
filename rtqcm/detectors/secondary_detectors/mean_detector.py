from detectors.detectorInterface import DetectorInterface
from rtqcm.controllers.detection_controller import
class MeanDetector(DetectorInterface):
    def __init__(
            self,
            lag_time: float,
            moving_average_time: float,
            detection_threshold: float,
            parent_controller:
    ):
        self.lag_time = lag_time
        self.moving_average_time = moving_average_time
        self.detection_threshold = detection_threshold

