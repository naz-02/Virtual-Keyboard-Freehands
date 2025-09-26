
import mediapipe as mp

class HandTracker:
    def __init__(self, max_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.5):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=max_hands, 
                                          min_detection_confidence=min_detection_confidence, 
                                          min_tracking_confidence=min_tracking_confidence)

    def process_frame(self, frame):
        rgb_frame = frame.copy()
        rgb_frame.flags.writeable = False
        results = self.hands.process(rgb_frame)
        rgb_frame.flags.writeable = True
        return results
