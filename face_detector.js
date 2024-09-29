// Wait for the DOM to load
document.addEventListener('DOMContentLoaded', async () => {
    const video = document.getElementById('video');
    const canvas = document.getElementById('overlay');
    const context = canvas.getContext('2d');

    // Load face-api.js models
    await faceapi.nets.tinyFaceDetector.loadFromUri('/models');
    // Start the video stream
    navigator.mediaDevices.getUserMedia({ video: {} })
        .then(stream => {
            video.srcObject = stream;
        })
        .catch(err => {
            console.error("Error accessing the webcam: ", err);
            alert("Cannot access webcam. Please allow camera permissions.");
        });

    // Once the video plays, start detection
    video.addEventListener('play', () => {
        const displaySize = { width: video.width, height: video.height };
        faceapi.matchDimensions(canvas, displaySize);

        setInterval(async () => {
            const detections = await faceapi.detectAllFaces(video, new faceapi.TinyFaceDetectorOptions());
            const resizedDetections = faceapi.resizeResults(detections, displaySize);
            
            // Clear the canvas
            context.clearRect(0, 0, canvas.width, canvas.height);
            
            // Draw detections
            faceapi.draw.drawDetections(canvas, resizedDetections);
        }, 100); // Adjust the interval as needed
    });
});