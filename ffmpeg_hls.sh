#!/bin/bash

# Set the output directory and filename
OUTPUT_DIR="/Users/vinzenz/Code/ma-thesis-backend/stream"
OUTPUT_FILENAME="stream.m3u8"

# Set the video input device
VIDEO_DEVICE="0"

# Set the video codec options
VIDEO_CODEC="libx264"
VIDEO_PRESET="ultrafast"
VIDEO_BITRATE="2000k"
VIDEO_RESOLUTION="1280x720"
VIDEO_FRAMERATE="30"

# Set the segment duration and number of segments to keep in the playlist
SEGMENT_DURATION="4"
SEGMENT_COUNT="10"

# Create the output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Start the ffmpeg command to capture and encode the video
ffmpeg -f avfoundation -framerate "$VIDEO_FRAMERATE" -i "$VIDEO_DEVICE" \
  -c:v "$VIDEO_CODEC" -preset "$VIDEO_PRESET" -b:v "$VIDEO_BITRATE" -s "$VIDEO_RESOLUTION" \
  -hls_time "$SEGMENT_DURATION" -hls_list_size "$SEGMENT_COUNT" \
  -hls_segment_filename "$OUTPUT_DIR/segment%03d.ts" "$OUTPUT_DIR/$OUTPUT_FILENAME"



# ffmpeg -f avfoundation -framerate 30 -i "0" -f hls stream.m3u8
