import cv2
import os

# set the path of the video file
video_path = "/home/pi/backend/output.avi"

# create a VideoCapture object to read the video file
cap = cv2.VideoCapture(video_path)

# create the output directory to save the BMP files
output_dir = os.path.join(os.path.dirname(video_path), "images")
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# loop through each frame of the video and save as BMP
frame_count = 0
while True:
    # read the next frame from the video
    ret, frame = cap.read()

    # check if the frame was successfully read
    if not ret:
        break

    # save the frame as a BMP file in the output directory
    output_file = os.path.join(output_dir, f"frame{frame_count:05d}.bmp")
    cv2.imwrite(output_file, frame)

    # increment the frame count
    frame_count += 1

# release the VideoCapture object
cap.release()

