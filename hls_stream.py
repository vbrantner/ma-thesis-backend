import os
import cv2
import http.server
import socketserver
import subprocess

# Define video dimensions and FPS
width = 640
height = 480
fps = 30

# Create video writer object
fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter("output.avi", fourcc, fps, (width, height))

# Start capturing video
cap = cv2.VideoCapture(0)

# Define HLS parameters
hls_time = 2  # Segment duration in seconds
hls_list_size = 10  # Maximum number of playlist entries
# Delete old segments, and don't write the endlist tag
hls_flags = "delete_segments+omit_endlist"
hls_base_url = "/hls/"  # Base URL for HLS segments

# Start HLS streaming server using FFmpeg
ffmpeg_cmd = [
    "ffmpeg",
    "-y",
    "-f", "rawvideo",
    "-pixel_format", "bgr24",
    "-video_size", f"{width}x{height}",
    "-framerate", str(fps),
    "-i", "-",
    "-hls_time", str(hls_time),
    "-hls_list_size", str(hls_list_size),
    "-hls_flags", hls_flags,
    "-hls_base_url", hls_base_url,
    "-vcodec", "libx264",
    "-pix_fmt", "yuv420p",
    "-preset", "ultrafast",
    # "-f", "",
    "index.m3u8"
]
process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

# Change current working directory to the HLS output directory
os.chdir("/home/pi/backend/output")

# Define HTTP request handler
handler = http.server.SimpleHTTPRequestHandler

# Start web server
with socketserver.TCPServer(("", 8002), handler) as httpd:
    print("Serving at port 8002...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()

# Stop FFmpeg process
process.stdin.close()
process.wait()
