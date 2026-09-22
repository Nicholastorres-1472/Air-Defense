import cv2

class MotionDetector:
    def __init__(self, history, varThreshhold=16, shadow=False,):
        self.fgbg = cv2.createBackgroundSubtractorMOG2(
            history=history,
            varThreshold=varThreshhold,
            detectShadows=shadow
        )
    
    def getBoundingBoxes(self, frame, minArea):
        thresh = self.fgbg.apply(frame)
        cv2.imshow('MOG2',thresh)
        thresh = cv2.dilate(thresh, None, iterations=2)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        boxes = []
        for contour in contours:
            if cv2.contourArea(contour) >= minArea:
                boxes.append(cv2.boundingRect(contour))
        return boxes