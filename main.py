import time
import cv2
import json

from detector import MotionDetector

with open('settings.json', 'r') as file:
    settings=json.load(file)

DEBUG = settings["DEBUG"]
CAMERA = settings["CAMERA"]
RECORDING = settings["RECORDING"]
TIMESTOP = settings["TIMESTOP"]
SHOWVIDEO = settings["SHOWVIDEO"]
TIMEDURATION = settings["TIMEDURATION"]
MINAREA = settings["MINAREA"]
testVideo = settings["testVideo"]
    
# Variable for test video 
if CAMERA: source = settings["CAMERA_SOURCE"]
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
draw_time = 0.0
recordingTime = 0.0

# Initializes the motionDetector class from detector.py
detector = MotionDetector(history=settings["detectorSettings"]["history"], varThreshhold=settings["detectorSettings"]["varThreshhold"], shadow=settings["detectorSettings"]["shadow"])

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
    boxes = detector.getBoundingBoxes(frame=video, minArea=MINAREA)
    t3 = time.time()
    math_time += (t3-t2)

    t4 = time.time()
    # Draws the bounding boxes on the raw video input 
    for (x,y, h, w) in boxes:
        area = (w*h)
        cv2.rectangle(video, (x,y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(video, f"{area}", (x,y+h+24), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0)) 

    t5= time.time()
    draw_time += (t5 - t4)


    # Displays the video feeds | Timed for performance measuring
    t6 = time.time()
    if SHOWVIDEO:
        cv2.imshow('video feed', video)

    # allows the program to be exited without "crashing" also allows imShow window to appear | reduces performance
    if SHOWVIDEO:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    t7 = time.time()
    imshowTime += (t7 - t5)

    # Measures total frames processed 
    total_frames += 1

    # Slows down video for debug purposes
    if DEBUG: time.sleep(0.05)

    if TIMESTOP: 
        if ((time.time() - startTime) > TIMEDURATION):
            break

    t8 = time.time()
    # if recording
    if RECORDING:
        out.write(video)
    t9 = time.time()
    recordingTime += (t9 - t8)


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
print(f"Total Draw Time: {draw_time:.2f} seconds")
print(f"Total imshow Time: {imshowTime:.2f} seconds")
print(f"Total Recording Time: {recordingTime:.2f} seconds")

cam.release()
cv2.destroyAllWindows()