# First Version of Air Defense

## TLDR 
Uses video feed to find targets in motion.

## Method
1. Recieves input from video or camera.
2. Converts raw video to grayscale.
3. Applies a Gaussian blur to the grayscale input.
4. Uses a accumalating weighted average to adapt the reference frame. To allow changes in background or environment.
5. Deltas the background frame from the current frame to create a mask that shows the change from the reference frame to the current frame.
6. Creates a threshold of the delta to create either solid black or white (0,1)
7. Contours are than calculated based off that threshold data. Using a threshold set by the user (size of drawn rectangle) to determine if it is noise or a valid target.
8. Rectangles are than drawn on the Raw video feed. 

## Contains perfromance measuring and debugging statements.