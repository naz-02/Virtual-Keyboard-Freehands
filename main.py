
import numpy as np
import cv2
import time
import winsound
from collections import deque

from virtual_keyboard.hand_tracker import HandTracker
from virtual_keyboard.keyboard import Keyboard
from virtual_keyboard.ui import UI
from virtual_keyboard.gestures import GestureRecognizer

def main():
    # Initialize components
    hand_tracker = HandTracker()
    keyboard = Keyboard()
    ui = UI()
    gesture_recognizer = GestureRecognizer()

    # Webcam settings
    is_low_res = False
    def init_webcam(low_res):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open webcam.")
            return None
        if low_res:
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        else:
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        return cap

    cap = init_webcam(is_low_res)
    if cap is None: return

    print("Starting Virtual Keyboard. Press 'q' to quit.")

    typed_text = ""
    last_press_time = 0
    cooldown = 0.5
    pressed_keys = {}
    tip_history = deque(maxlen=5)

    while True:
        success, frame = cap.read()
        if not success:
            continue

        frame = cv2.flip(frame, 1)
        results = hand_tracker.process_frame(frame)
        keys = keyboard.get_keys()
        highlighted_key = None

        if results.multi_hand_landmarks:
            for hand_idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                hand_label = results.multi_handedness[hand_idx].classification[0].label

                if hand_label == "Right":
                    h, w, c = frame.shape
                    ix_raw, iy_raw = int(hand_landmarks.landmark[hand_tracker.mp_hands.HandLandmark.INDEX_FINGER_TIP].x * w), int(hand_landmarks.landmark[hand_tracker.mp_hands.HandLandmark.INDEX_FINGER_TIP].y * h)
                    tip_history.append((ix_raw, iy_raw))
                    ix = int(np.mean([p[0] for p in tip_history]))
                    iy = int(np.mean([p[1] for p in tip_history]))

                    for row_idx, row_keys in enumerate(keys):
                        for col_idx, key in enumerate(row_keys):
                            kx, ky, kw, kh = 50 + col_idx*70, 50 + row_idx*70, 60, 60
                            if key == "Space": kw = 200
                            elif key == "<-": kw = 130
                            elif key == "MODE" or key == "Shift" or key == "RES": kw = 100

                            if kx < ix < kx + kw and ky < iy < ky + kh:
                                highlighted_key = key
                                break
                        if highlighted_key: break

                    if gesture_recognizer.detect_pinch(hand_landmarks, frame.shape) and highlighted_key is not None:
                        current_time = time.time()
                        if current_time - last_press_time > cooldown:
                            winsound.Beep(1000, 100)
                            if highlighted_key == "<-": typed_text = typed_text[:-1]
                            elif highlighted_key == "Space": typed_text += " "
                            elif highlighted_key == "MODE": keyboard.switch_layout()
                            elif highlighted_key == "Shift": keyboard.toggle_shift()
                            elif highlighted_key == "RES":
                                is_low_res = not is_low_res
                                cap.release()
                                cap = init_webcam(is_low_res)
                            else: typed_text += highlighted_key
                            last_press_time = current_time
                            pressed_keys[highlighted_key] = current_time

                if hand_label == "Left":
                    if gesture_recognizer.detect_pinch(hand_landmarks, frame.shape):
                        current_time = time.time()
                        if current_time - last_press_time > cooldown:
                            winsound.Beep(1000, 100)
                            typed_text += " "
                            last_press_time = current_time
                            pressed_keys["Space"] = current_time

                    if gesture_recognizer.detect_thumbs_up(hand_landmarks):
                        current_time = time.time()
                        if current_time - last_press_time > cooldown:
                            winsound.Beep(1000, 100)
                            typed_text = typed_text[:-1]
                            last_press_time = current_time
                            pressed_keys["<-"] = current_time

                    if gesture_recognizer.detect_swipe_left(hand_landmarks):
                        current_time = time.time()
                        if current_time - last_press_time > cooldown:
                            winsound.Beep(800, 100)
                            last_space = typed_text.rfind(' ')
                            if last_space != -1:
                                typed_text = typed_text[:last_space]
                            else:
                                typed_text = ""
                            last_press_time = current_time

        ui.draw(frame, keys, highlighted_key, typed_text, pressed_keys)
        cv2.imshow('Virtual Keyboard', frame)

        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Application closed.")

if __name__ == "__main__":
    main()
