import cv2
import mediapipe as mp
import numpy as np
import time
import HandTrackingModule as htm
import math
import subprocess

# For Linux - Volume Control Using pactl
def set_volume(volume_percent):
    """Set system volume in Linux using pactl."""
    volume_percent = max(0, min(100, volume_percent))  # Ensure volume is within 0-100%
    subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"{volume_percent}%"])

# Webcam Settings
widthCam, heightCam = 640, 480
hand_min, hand_max = 40, 300

vol_min, vol_max = 0, 100
prevTime = 0

cap = cv2.VideoCapture(0)
cap.set(3, widthCam)
cap.set(4, heightCam)

detector = htm.handDetector(detectionCon=0.7)

volBar = 400
volPer = 0

while True:
    success, frame = cap.read()
    frame = detector.findHands(frame)
    lmList = detector.findPosition(frame, draw=False)

    if len(lmList) != 0:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        # Draw Circles and Line Between Fingers
        cv2.circle(frame, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(frame, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)

        length = math.hypot(x2 - x1, y2 - y1)
        
        volume = np.interp(length, [hand_min, hand_max], [vol_min, vol_max])
        volPer = np.interp(length, [hand_min, hand_max], [0, 100])

        set_volume(int(volume))

        if length < 50:
            cv2.circle(frame, (cx, cy), 15, (255, 255, 255), cv2.FILLED)

    # **🔹 NEW SEGMENTED VOLUME BAR (EMPTY & FILLED BLOCKS)**
    num_segments = 10
    segment_height = 25
    start_y = 400
    filled_segments = int(volPer / 10)  # Determine how many segments should be filled

    for i in range(num_segments):
        y = start_y - (i * segment_height)
        color = (50, 50, 50)  # Default: empty block color (gray)
        
        if i < filled_segments:
            color = (0, 255, 0)  # Filled segments in green
        
        cv2.rectangle(frame, (50, y), (85, y - segment_height + 5), color, cv2.FILLED)
        cv2.rectangle(frame, (50, y), (85, y - segment_height + 5), (200, 200, 200), 2)  # Border for clarity

    # Display Volume Percentage
    cv2.putText(frame, f'{int(volPer)}%', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    # FPS Display
    currTime = time.time()
    fps = 1 / (currTime - prevTime)
    prevTime = currTime
    cv2.putText(frame, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    cv2.imshow("Hand Gesture Volume Control", frame)
    cv2.waitKey(1)
