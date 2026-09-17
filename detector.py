import cv2

class MotionDetector:
    def __init__(self):
        self.avg = None
    
    def getBoundingBoxes(self, frame, minArea):
        self.boundingBoxes = []

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        blurred = cv2.GaussianBlur(gray, (21,21), 0)

        if self.avg is None:
            self.avg = blurred.copy().astype("float")

        cv2.accumulateWeighted(blurred, self.avg, 0.01)

        backgroundFrame = cv2.convertScaleAbs(self.avg)

        frameDelta = cv2.absdiff(backgroundFrame, blurred)

        _, thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)

        thresh = cv2.dilate(thresh, None, iterations=2)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) < minArea:
                continue

            x, y, h, w = cv2.boundingRect(contour)
            self.boundingBoxes.append((x,y,h,w))

        return self.boundingBoxes