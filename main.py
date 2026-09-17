import time
import cv2

from detector import MotionDetector

DEBUG = False
CAMERA = True
RECORDING = False
TIMESTOP = True
SHOWVIDEO = False
TIMEDURATION = 5
testVideo = "Ball.mp4"
    
# Variable for test video 
if CAMERA: source = 0
else: source = f"./TestVideos/{testVideo}"  

# Opens Camera/Video and times it
openTime = time.time()
cam = cv2.VideoCapture(source)
endOpenTime = time.time()
totalOpenTime = endOpenTime - openTime

# Camera settings for recording
if RECORDING:
    width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cam.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('auto_output.mp4', fourcc, fps, (width, height))

# Initializes imshow Timer
imshowTime = 0

# Error handling if camera fails to open
if not cam.isOpened():
    print("Camera could not open")
    exit()

# Initializes performance measuring variables
total_frames = 0
startTime = time.time()
decode_time = 0.0
math_time = 0.0

# Initializes the motionDetector class from detector.py
detector = MotionDetector()

while True:

    # Reads camera input | times it for performance measuring.
    t0 = time.time()
    ret, video = cam.read()
    if not ret:
        print("Error: Can't receive frame (stream end?). Exiting...")
        break
    t1 = time.time()
    decode_time += (t1 - t0)

    # Uses the getBoundingBoxes function from detector.py | times it for performance measuring
    t2 = time.time()
    boxes = detector.getBoundingBoxes(frame=video, minArea=1000)

    # Draws the bounding boxes on the raw video input 
    for (x,y, h, w) in boxes:
        cv2.rectangle(video, (x,y), (x + w, y + h), (0, 255, 0), 2)

    t3 = time.time()
    math_time += (t3 - t2)


    # Displays the video feeds | Timed for performance measuring
    t4 = time.time()
    if SHOWVIDEO:
        cv2.imshow('video feed', video)
        # cv2.imshow('Gray Scale', gray)
        # cv2.imshow('blurred feed', blurred)
        # cv2.imshow('Delta feed', frame_delta)
        # cv2.imshow('thresh feed', thresh)
    t5 = time.time()
    imshowTime += (t5 - t4)

    t6 = time.time()


    # allows the program to be exited without "crashing" | reduces performance, comment for increased performance
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

    # Measures total frames processed 
    total_frames += 1

    # Slows down video for debug purposes
    if DEBUG: time.sleep(0.025)

    if TIMESTOP: 
        if ((time.time() - startTime) > TIMEDURATION):
            break

    # if recording
    if RECORDING:
        out.write(video)


# Calculates performance
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
cv2.destroyAllWindows()