
import cv2
import mediapipe as mp
import numpy as np
import time
from collections import deque
import winsound

# Function to draw the keyboard and the text output with a prettier UI
def draw_ui(frame, keys, highlighted_key=None, typed_text="", pressed_keys={}):
    # Create a semi-transparent overlay
    overlay = frame.copy()
    alpha = 0.5  # Transparency factor

    # Keyboard background
    cv2.rectangle(overlay, (40, 40), (820, 340), (50, 50, 50), -1)

    # Draw the keyboard
    for row_idx, row_keys in enumerate(keys):
        for col_idx, key in enumerate(row_keys):
            x, y, w, h = 50 + col_idx*70, 50 + row_idx*70, 60, 60
            if key == "Space": w = 200
            elif key == "<-": w = 130
            elif key == "MODE" or key == "Shift" or key == "RES": w = 100

            key_color = (100, 100, 100)
            if key == highlighted_key:
                # Glow effect for highlighted key
                cv2.rectangle(overlay, (x-5, y-5), (x + w+5, y + h+5), (0, 255, 255), -1)
            
            cv2.rectangle(overlay, (x, y), (x + w, y + h), key_color, -1)
            cv2.putText(overlay, key, (x + 15, y + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

            # Fading green animation for pressed keys
            if key in pressed_keys:
                time_since_press = time.time() - pressed_keys[key]
                if time_since_press < 0.5:
                    fade_alpha = 1 - (time_since_press / 0.5)
                    green_overlay = overlay.copy()
                    cv2.rectangle(green_overlay, (x, y), (x + w, y + h), (0, 255, 0), -1)
                    cv2.addWeighted(green_overlay, fade_alpha, overlay, 1 - fade_alpha, 0, overlay)

    # Blend the overlay with the frame
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

    # Draw the text display area
    cv2.rectangle(frame, (50, 350), (810, 420), (50, 50, 50), -1)
    cv2.putText(frame, typed_text, (60, 400), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)

def main():
    # Initialize MediaPipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.5)
    
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

    # Define keyboard layouts
    layouts = {
        "QWERTY_LOWER": [
            ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
            ["a", "s", "d", "f", "g", "h", "j", "k", "l", ";"],
            ["z", "x", "c", "v", "b", "n", "m", ",", ".", "/"],
            ["Space", "<-", "Shift", "MODE", "RES"]
        ],
        "QWERTY_UPPER": [
            ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L", ":"],
            ["Z", "X", "C", "V", "B", "N", "M", "<", ">", "?"],
            ["Space", "<-", "Shift", "MODE", "RES"]
        ],
        "NUMPAD": [
            ["7", "8", "9"],
            ["4", "5", "6"],
            ["1", "2", "3"],
            ["0", "<-", "MODE", "RES"]
        ],
        "YES/NO": [
            ["YES", "NO"],
            ["<-", "MODE", "RES"]
        ]
    }
    layout_names = list(layouts.keys())
    current_layout_name = "QWERTY_LOWER"
    keys = layouts[current_layout_name]
    is_shifted = False
    typed_text = ""
    
    # Cooldown for key presses
    last_press_time = 0
    cooldown = 0.5  # seconds
    pressed_keys = {}

    # For smoothing the cursor and gestures
    tip_history = deque(maxlen=5)
    left_wrist_history = deque(maxlen=10)

    while True:
        success, frame = cap.read()
        if not success:
            continue

        frame = cv2.flip(frame, 1)
        h, w, c = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        highlighted_key = None
        if results.multi_hand_landmarks:
            for hand_idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                hand_label = results.multi_handedness[hand_idx].classification[0].label

                if hand_label == "Right":
                    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
                    
                    ix_raw, iy_raw = int(index_tip.x * w), int(index_tip.y * h)
                    tip_history.append((ix_raw, iy_raw))

                    ix = int(np.mean([p[0] for p in tip_history]))
                    iy = int(np.mean([p[1] for p in tip_history]))

                    mx, my = int(middle_tip.x * w), int(middle_tip.y * h)

                    cv2.circle(frame, (ix, iy), 10, (255, 0, 0), -1)
                    cv2.circle(frame, (mx, my), 10, (0, 0, 255), -1)

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
                    
                    distance = np.sqrt((ix - mx)**2 + (iy - my)**2)

                    if distance < 30 and highlighted_key is not None:
                        current_time = time.time()
                        if current_time - last_press_time > cooldown:
                            winsound.Beep(1000, 100)
                            if highlighted_key == "<-": typed_text = typed_text[:-1]
                            elif highlighted_key == "Space": typed_text += " "
                            elif highlighted_key == "MODE":
                                current_layout_index = layout_names.index(current_layout_name)
                                next_layout_index = (current_layout_index + 1) % len(layout_names)
                                current_layout_name = layout_names[next_layout_index]
                                keys = layouts[current_layout_name]
                            elif highlighted_key == "Shift":
                                is_shifted = not is_shifted
                                if is_shifted: keys = layouts["QWERTY_UPPER"]
                                else: keys = layouts["QWERTY_LOWER"]
                            elif highlighted_key == "RES":
                                is_low_res = not is_low_res
                                cap.release()
                                cap = init_webcam(is_low_res)
                            else: typed_text += highlighted_key
                            last_press_time = current_time
                            pressed_keys[highlighted_key] = current_time
                
                if hand_label == "Left":
                    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                    left_wrist_history.append(wrist.x)

                    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                    index_tip_left = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

                    tx, ty = int(thumb_tip.x * w), int(thumb_tip.y * h)
                    ix_left, iy_left = int(index_tip_left.x * w), int(index_tip_left.y * h)

                    cv2.circle(frame, (tx, ty), 10, (0, 255, 255), -1)
                    cv2.circle(frame, (ix_left, iy_left), 10, (0, 255, 255), -1)

                    space_distance = np.sqrt((tx - ix_left)**2 + (ty - iy_left)**2)
                    if space_distance < 30:
                        current_time = time.time()
                        if current_time - last_press_time > cooldown:
                            winsound.Beep(1000, 100)
                            typed_text += " "
                            last_press_time = current_time
                            pressed_keys["Space"] = current_time
                    
                    # Thumbs up for backspace
                    thumb_tip_y = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y
                    index_pip_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y
                    middle_pip_y = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y
                    ring_pip_y = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y
                    pinky_pip_y = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y

                    index_tip_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
                    middle_tip_y = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
                    ring_tip_y = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y
                    pinky_tip_y = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y

                    if (thumb_tip_y < index_pip_y and thumb_tip_y < middle_pip_y and thumb_tip_y < ring_pip_y and thumb_tip_y < pinky_pip_y and
                        index_tip_y > index_pip_y and middle_tip_y > middle_pip_y and ring_tip_y > ring_pip_y and pinky_tip_y > pinky_pip_y):
                        current_time = time.time()
                        if current_time - last_press_time > cooldown:
                            winsound.Beep(1000, 100)
                            typed_text = typed_text[:-1]
                            last_press_time = current_time
                            pressed_keys["<-"] = current_time

                    if len(left_wrist_history) == 10:
                        if left_wrist_history[0] - left_wrist_history[-1] > 0.1:
                            current_time = time.time()
                            if current_time - last_press_time > cooldown:
                                winsound.Beep(800, 100)
                                last_space = typed_text.rfind(' ')
                                if last_space != -1:
                                    typed_text = typed_text[:last_space]
                                else:
                                    typed_text = ""
                                last_press_time = current_time
                                left_wrist_history.clear()

        draw_ui(frame, keys, highlighted_key, typed_text, pressed_keys)
        cv2.imshow('Virtual Keyboard', frame)

        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

    hands.close()
    cap.release()
    cv2.destroyAllWindows()
    print("Application closed.")

if __name__ == "__main__":
    main()
