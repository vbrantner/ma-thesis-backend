// Import necessary libraries
import express from 'express';
import { StreamCamera, Codec } from 'pi-camera-connect';
import { pipeline } from 'stream/promises';

// Create a new express application
const app = express();

// Set up the stream camera
const cam = new StreamCamera({
  codec: Codec.H264
});
console.log('cam', cam)

// Set up the video route
app.get('/video', async (req, res) => {
  console.log('get request')
  res.writeHead(200, {
    'Content-Type': 'video/h264'
  });

  try {
    console.log('try to create a stream')
    // Create a video stream
    const videoStream = cam.createStream();

    await cam.startCapture();

    videoStream.on('data', data => console.log('New video data', data));
    // Use pipeline method to pipe the video stream to the response
    // Pipeline will automatically handle cleanup in case of errors
    await pipeline(videoStream, res);

    console.log('Video streaming ended');
  } catch (error) {
    console.error('An error occurred:', error);
  } finally {
    await cam.stopCapture();
  }
});

// Set up the server to listen on port 3000
app.listen(3000, () => {
  console.log('Server started on port 3000');
});
