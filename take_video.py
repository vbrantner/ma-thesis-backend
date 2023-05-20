import cv2
import time

# set the video resolution
width = 1024
height = 1024

# create a VideoCapture object to capture video from the camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# set the codec and create a VideoWriter object to save the video to a file
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (width, height))

# set the recording duration to 30 seconds
recording_duration = 30  # seconds

# start the recording
start_time = time.time()
while (time.time() - start_time) < recording_duration:
    # read the next frame from the camera
    ret, frame = cap.read()

    # check if the frame was successfully read
    if not ret:
        break

    # write the frame to the output file
    out.write(frame)

# release the VideoCapture and VideoWriter objects, and close the window
cap.release()
out.release()
cv2.destroyAllWindows()

