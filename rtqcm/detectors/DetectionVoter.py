
class DetectionVoter:
    """
    Class responsible for:
        - Making detections with all detectors available
        - Voting whether or not the detections are valid
        - Making the detection
        - Comparing the detection to previous ones to see if it hasn't already been detected
    """
