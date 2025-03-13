import cv2
import time
import numpy as np
import mediapipe as mp
import HandTrackingModule as htm
from utils import draw_mode_switch_buttons, draw_keyboard, check_key_press, color_buttons, detect_v_gesture

# Initialize variables
typed_text = ""
pinch_threshold = 90
pinching = False
debounce_time = 0.5
last_key_press_time = time.time()
drawing_mode = False

# Default drawing settings
color = "Red"
drawing_color = (0, 0, 255)
drawing_thickness = 8
eraser_thickness = 40  # Increased eraser thickness
eraser = False

# Store drawn strokes
strokes = []
current_stroke = []

# Debounce for V gesture
last_v_gesture_time = 0
v_gesture_debounce = 0.5  # Half a second debounce

drawing_canvas = np.zeros((1080, 1920, 3), dtype=np.uint8)  # Blank canvas for drawing

prev_x, prev_y = None, None  # Store the previous fingertip position

# Exponential Moving Average for smoother movement
smooth_x, smooth_y = None, None
alpha = 0.1  # Smoothing factor (adjusted for better fluidity)

# Initialize Webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# Initialize Hand Detector
detector = htm.handDetector(detectionCon=0.8)


while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (1920, 1080))
    frame = detector.findHands(frame)
    lmList = detector.findPosition(frame, draw=False)

    # Draw mode switch buttons
    mode_buttons = draw_mode_switch_buttons(frame, drawing_mode)
    
    # Draw keyboard if not in drawing mode
    if not drawing_mode:
        draw_keyboard(frame)

    if len(lmList) != 0:
        x1, y1 = lmList[8][1], lmList[8][2]  # Index Finger Tip
        x2, y2 = lmList[4][1], lmList[4][2]  # Thumb Tip
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2  # Midpoint (For typing mode)
        pinch_distance = np.linalg.norm(np.array([x1, y1]) - np.array([x2, y2]))

        cv2.circle(frame, (x1, y1), 15, (0, 255, 0), -1)  # Show index finger tip

        # **Mode Switching**
        for (bx, by, bw, bh, mode) in mode_buttons:
            if bx < x1 < bx + bw and by < y1 < by + bh:
                if pinch_distance < pinch_threshold and not pinching:
                    drawing_mode = (mode == "draw")
                    if drawing_mode:
                        typed_text = ""  # Clear text in draw mode
                    else:
                        drawing_canvas.fill(0)  # Clear canvas in type mode
                    pinching = True
                    time.sleep(0.2)

        # Reset pinching flag
        if pinch_distance > pinch_threshold:
            pinching = False

        # **Color Selection in Drawing Mode**
        if drawing_mode:
            color, eraser, drawing_color = color_buttons(frame, x1, y1, color, eraser, drawing_color)

        # **Drawing Mode with Smoothing**
        if drawing_mode and pinch_distance < pinch_threshold:
            if smooth_x is None or smooth_y is None:
                smooth_x, smooth_y = x1, y1  # Initialize on first frame
            else:
                smooth_x = alpha * x1 + (1 - alpha) * smooth_x
                smooth_y = alpha * y1 + (1 - alpha) * smooth_y

            # Ensure significant movement before drawing
            if prev_x is not None and prev_y is not None:
                if np.hypot(smooth_x - prev_x, smooth_y - prev_y) > 2:
                    thickness = eraser_thickness if eraser else drawing_thickness
                    color_to_draw = (0, 0, 0) if eraser else drawing_color
                    cv2.line(drawing_canvas, (prev_x, prev_y), (int(smooth_x), int(smooth_y)), color_to_draw, thickness, cv2.LINE_AA)
                    current_stroke.append((prev_x, prev_y, smooth_x, smooth_y, color_to_draw, thickness))

            prev_x, prev_y = int(smooth_x), int(smooth_y)  # Update previous position

        else:
            if current_stroke:
                strokes.append(current_stroke[:])
                current_stroke = []
            prev_x, prev_y = None, None
            smooth_x, smooth_y = None, None  # Reset smoothing to prevent unwanted strokes

        # **Detect 'V' Gesture to Remove Last Stroke**
        if detect_v_gesture(lmList) and strokes and (time.time() - last_v_gesture_time > v_gesture_debounce):
            strokes.pop()
            last_v_gesture_time = time.time()
            drawing_canvas.fill(0)  # Clear canvas
            for stroke in strokes:
                for x1, y1, x2, y2, col, thick in stroke:
                    cv2.line(drawing_canvas, (x1, y1), (int(x2), int(y2)), col, thick, cv2.LINE_AA)

        # **Typing Mode**
        if not drawing_mode:
            key_pressed = check_key_press(x1, y1)
            if pinch_distance < pinch_threshold and not pinching and key_pressed:
                typed_text = (typed_text[:-1] if key_pressed == "<-" else typed_text + key_pressed) if key_pressed != "SPACE" else typed_text + " "
                pinching = True
                time.sleep(0.2)  # Debounce to prevent multiple inputs

    # **Merge Drawing Canvas with Frame**
    frame = cv2.addWeighted(frame, 1, drawing_canvas, 0.7, 0)  # Increase weight for bolder strokes

    # **Display Typed Text**
    cv2.putText(frame, typed_text, (500, 150), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (255, 255, 0), 5, cv2.LINE_AA)

    # **Show Frame**
    cv2.imshow("Virtual Keyboard", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
