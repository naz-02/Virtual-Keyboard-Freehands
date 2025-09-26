
import cv2
import time

class UI:
    def __init__(self):
        pass

    def draw(self, frame, keys, highlighted_key, typed_text, pressed_keys):
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
