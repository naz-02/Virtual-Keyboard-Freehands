
import numpy as np
import mediapipe as mp
from collections import deque

class GestureRecognizer:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.left_wrist_history = deque(maxlen=10)

    def detect_pinch(self, hand_landmarks, frame_shape):
        h, w, c = frame_shape
        index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        middle_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        ix, iy = int(index_tip.x * w), int(index_tip.y * h)
        mx, my = int(middle_tip.x * w), int(middle_tip.y * h)
        distance = np.sqrt((ix - mx)**2 + (iy - my)**2)
        return distance < 30

    def detect_thumbs_up(self, hand_landmarks):
        thumb_tip_y = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP].y
        index_pip_y = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_PIP].y
        middle_pip_y = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y
        ring_pip_y = hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_PIP].y
        pinky_pip_y = hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_PIP].y

        index_tip_y = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].y
        middle_tip_y = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
        ring_tip_y = hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP].y
        pinky_tip_y = hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_TIP].y

        if (thumb_tip_y < index_pip_y and thumb_tip_y < middle_pip_y and thumb_tip_y < ring_pip_y and thumb_tip_y < pinky_pip_y and
            index_tip_y > index_pip_y and middle_tip_y > middle_pip_y and ring_tip_y > ring_pip_y and pinky_tip_y > pinky_pip_y):
            return True
        return False

    def detect_swipe_left(self, hand_landmarks):
        wrist = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]
        self.left_wrist_history.append(wrist.x)
        if len(self.left_wrist_history) == 10:
            if self.left_wrist_history[0] - self.left_wrist_history[-1] > 0.1:
                self.left_wrist_history.clear()
                return True
        return False
