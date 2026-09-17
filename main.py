import time
import cv2 as cv

openTime = time.time()
cam = cv.VideoCapture('RollingBall.mp4')
endOpenTime = time.time()
totalOpenTime = endOpenTime - openTime
imshowTime = 0
if not cam.isOpened():
    print("Camera could not open")
    exit()

backgroundFrame = None

avg = None

frameCounter = 0

total_frames = 0
startTime = time.time()
decode_time = 0.0
math_time = 0.0

while True:

    if frameCounter > 10:
        frameCounter = 0

    # Reads camera input
    t0 = time.time()
    ret, video = cam.read()
    if not ret:
        print("Error: Can't receive frame (stream end?). Exiting...")
        break
    t1 = time.time()
    decode_time += (t1 - t0)

    # Converts raw video input to grayscale
    t2 = time.time()
    gray = cv.cvtColor(video, cv.COLOR_BGR2GRAY)

    # Blurs the grayed video input
    blurred = cv.GaussianBlur(gray, (21,21), 0)

    if avg is None: 
        avg = blurred.copy().astype("float")
        continue

    cv.accumulateWeighted(blurred, avg, 0.01)

    backgroundFrame = cv.convertScaleAbs(avg)

    frame_delta = cv.absdiff(backgroundFrame, blurred)

    _, thresh = cv.threshold(frame_delta, 25, 255, cv.THRESH_BINARY)

    thresh = cv.dilate(thresh, None, iterations=2)

    contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        print(f"Size:{cv.contourArea(contour)}")
        if cv.contourArea(contour) < 1000:
            continue

        x, y, h, w = cv.boundingRect(contour)

        cv.rectangle(video, (x,y), (x + w, y + h), (0, 255, 0), 2)

    t3 = time.time()
    math_time += (t3 - t2)

    t4 = time.time()
    cv.imshow('video feed', video)
    # cv.imshow('Gray Scale', gray)
    # cv.imshow('blurred feed', blurred)
    # cv.imshow('Delta feed', frame_delta)
    # cv.imshow('thresh feed', thresh)
    t5 = time.time()
    imshowTime += (t5 - t4)


    if cv.waitKey(1) & 0xFF == ord('q'):
        break

    total_frames += 1

    frameCounter += 1

    time.sleep(0.025)

    # if ((time.time() - startTime) > 15):
    #     break

endTime = time.time()
totalTime = endTime - startTime
averageFPS = total_frames / totalTime

print(f"Total Frames: {total_frames}")
print(f"Total time: {totalTime:.2f}")
print(f"FPS: {averageFPS:.2f}")
print(f"Total Opening Time: {totalOpenTime:.2f} seconds")
print(f"Total Decode Time (cap.read): {decode_time:.2f} seconds")
print(f"Total Math Time: {math_time:.2f} seconds")
print(f"Total imshow Time: {imshowTime:.2f} seconds")

cam.release()
cv.destroyAllWindows()