let audioRecorder = null;
let videoRecorder = null;
let audioStream = null;
let videoStream = null;

const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");
const videoEl = document.getElementById("preview");

// Connect to the Flask-SocketIO server
const socket = io();

/**
 * Convert ArrayBuffer -> Latin1 string, so we can send raw binary over Socket.IO easily.
 */
function arrayBufferToLatin1(buffer) {
  let binaryStr = "";
  const bytes = new Uint8Array(buffer);
  for (let i = 0; i < bytes.byteLength; i++) {
    binaryStr += String.fromCharCode(bytes[i]);
  }
  return binaryStr;
}

function captureAndSendFrame() {
    if (!videoStream) return;

    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d");

    canvas.width = videoEl.videoWidth;
    canvas.height = videoEl.videoHeight;
    ctx.drawImage(videoEl, 0, 0, canvas.width, canvas.height);

    // Convert frame to Blob (image format)
    canvas.toBlob((blob) => {
        const reader = new FileReader();
        reader.readAsArrayBuffer(blob);
        reader.onloadend = () => {
            socket.emit("image_chunk", { chunk: reader.result });
        };
    }, "image/jpeg"); // Send as JPEG for efficiency
}


/**
 * Start capturing: 
 * - near real-time audio chunks (100ms)
 * - half-second video chunks (500ms)
 */
startBtn.addEventListener("click", async () => {
  try {
    // Request combined audio+video from the user
    const combinedStream = await navigator.mediaDevices.getUserMedia({
      video: true,
      audio: true,
    });

    // Separate out the tracks so we can record them at different intervals
    const audioTrack = combinedStream.getAudioTracks()[0];
    const videoTrack = combinedStream.getVideoTracks()[0];

    audioStream = new MediaStream([audioTrack]);
    videoStream = new MediaStream([videoTrack]);

    // Display local preview (both audio+video, or just video)
    videoEl.srcObject = combinedStream;

    setInterval(captureAndSendFrame, 500);

    const audio_reader = new FileReader();

    audio_reader.onload = () => {
        // Send raw binary data directly, no conversion to Latin1
        //socket.emit("audio_chunk", { chunk: audio_reader.result });
        socket.emit("audio_chunk", audio_reader.result);
        //socket.emit("audio_chunk", buffer, { binary: true });
    };

    const video_reader = new FileReader();

    video_reader.onload = () => {
        // Send raw binary data directly, no conversion to Latin1
        socket.emit("video_chunk", { chunk: video_reader.result });
    };

    // 1) Audio Recorder: short timeslice for near real-time
    audioRecorder = new MediaRecorder(audioStream, {
      //mimeType: "audio/webm; codecs=opus",
      mimeType: "audio/mp4",
    });

    audioRecorder.ondataavailable = (e) => {
        //console.log("audio");
        if (e.data.size > 0) {
          audio_reader.readAsArrayBuffer(e.data);
        }
      };
    audioRecorder.start(1000 * 5); // get ~100ms audio chunks

    // 2) Video Recorder: 500ms intervals
    videoRecorder = new MediaRecorder(videoStream, {
      //mimeType: "video/webm; codecs=vp8",
      mimeType: "video/mp4",
    });
    videoRecorder.ondataavailable = (e) => {
        console.log("video");

        if (e.data.size > 0) {
          video_reader.readAsArrayBuffer(e.data);
        }
    };
      
    videoRecorder.start(500);

    startBtn.disabled = true;
    stopBtn.disabled = false;
  } catch (err) {
    console.error("Error accessing camera/mic:", err);
    alert("Could not access camera or microphone. Check browser permissions!");
  }
});

/**
 * Stop capturing both audio and video recorders
 */
stopBtn.addEventListener("click", () => {
  if (audioRecorder && audioRecorder.state !== "inactive") {
    audioRecorder.stop();
  }
  if (videoRecorder && videoRecorder.state !== "inactive") {
    videoRecorder.stop();
  }
  if (audioStream) {
    audioStream.getTracks().forEach((track) => track.stop());
  }
  if (videoStream) {
    videoStream.getTracks().forEach((track) => track.stop());
  }
  videoEl.srcObject = null;

  startBtn.disabled = false;
  stopBtn.disabled = true;
});


// Preload audio and allow Safari to enable sound after user interaction
const beep = new Audio("/static/sounds/beep.mp3");


// // Enable audio on user interaction (Safari requires this)
// document.addEventListener("click", () => {
//     beep.play().catch(() => {
//         console.log("Safari blocked autoplay; enabling sound.");
//     });
// }, { once: true }); // Ensures it runs only once


// Function to play a beep sound
function playBeep() {
    beep.currentTime = 0; // Reset sound in case it's playing
    console.log("BEEEEP");
    beep.play().catch(err => console.log("Playback blocked:", err));
}


// Listen for gesture responses
socket.on("gesture_response", (data) => {
    console.log("Received Gesture Response:", data.message);
    if (data.message == "ok") {
        playBeep();
    }
});