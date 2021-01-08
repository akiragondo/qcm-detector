import numpy as np

class DetectorInterface:
    def detectAnomaly(self, sample: np.ndarray) -> int:
        pass

    def describe(self) -> str:
        pass