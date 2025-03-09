# Hand Tracking ----> Palm Detection    +  Hand Landmark  

import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self,mode=False,maxHands=2,detectionCon=0.5,trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode, 
            max_num_hands=self.maxHands, 
            min_detection_confidence=self.detectionCon, 
            min_tracking_confidence=self.trackCon
        )
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self,frame,draw=True):
        frameRGB = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

        self.results = self.hands.process(frameRGB)
        # print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(frame,handLms, self.mpHands.HAND_CONNECTIONS)
        return frame
    
    def findPosition(self,frame,handNo=0,draw=True):
        self.lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]

            for id,lm in enumerate(myHand.landmark):
                #our landmarks are in decimal values, but we want them in pixels so would multiple them by height and width
                h,w,c = frame.shape
                cx, cy = int(lm.x*w), int(lm.y*h) # center values
                # print(id,cx,cy)
                self.lmList.append([id,cx,cy])

                if draw:
                    cv2.circle(frame,(cx,cy),15,(255,0,255),cv2.FILLED)

        return self.lmList
    
    def fingersUp(self):
        """Returns a list where 1 means the finger is up and 0 means it is down."""
        fingers = []
        if not hasattr(self, "lmList") or len(self.lmList) == 0:
            return fingers

        # Thumb (compare tip with IP joint)
        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:  
            fingers.append(1)
        else:
            fingers.append(0)

        # Other four fingers (compare tip with PIP joint)
        for i in range(1, 5):
            if self.lmList[self.tipIds[i]][2] < self.lmList[self.tipIds[i] - 2][2]:  
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers


mpHands = mp.solutions.hands

hands = mpHands.Hands(False)

mpDraw = mp.solutions.drawing_utils