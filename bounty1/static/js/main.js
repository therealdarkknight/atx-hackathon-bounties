
let audioRecorder = null;
let videoRecorder = null;
let audioStream = null;
let videoStream = null;
let isContinuousAudio = false; // Flag to keep looping 10s audio
let recordedAudioChunks = [];

const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");
const videoEl = document.getElementById("preview");

// Connect to the Flask-SocketIO server
const socket = io();

/**
 * Send a snapshot frame from the live video every 500ms.
 * You already have this logic in your code.
 */
function captureAndSendFrame() {
  if (!videoStream) return;

  const canvas = document.createElement("canvas");
  const ctx = canvas.getContext("2d");

  canvas.width = videoEl.videoWidth;
  canvas.height = videoEl.videoHeight;
  ctx.drawImage(videoEl, 0, 0, canvas.width, canvas.height);

  canvas.toBlob((blob) => {
    const reader = new FileReader();
    reader.readAsArrayBuffer(blob);
    reader.onloadend = () => {
      socket.emit("image_chunk", { chunk: reader.result });
    };
  }, "image/jpeg"); // JPEG for efficiency
}

/**
 * Start capturing both:
 *  - 10-second audio chunks (in MP4)
 *  - 500ms frames for video
 */
startBtn.addEventListener("click", async () => {
  try {
    // 1) Request combined audio+video from the user
    const combinedStream = await navigator.mediaDevices.getUserMedia({
      video: true,
      audio: true,
    });

    // 2) Separate out the tracks so we can handle them differently
    const audioTrack = combinedStream.getAudioTracks()[0];
    const videoTrack = combinedStream.getVideoTracks()[0];

    audioStream = new MediaStream([audioTrack]);
    videoStream = new MediaStream([videoTrack]);

    // 3) Display local preview
    videoEl.srcObject = combinedStream;
    videoEl.play(); // ensure video is playing

    // 4) Send snapshot frames every 500ms
    setInterval(captureAndSendFrame, 500);

    // 5) Start continuous audio in 10s chunks
    isContinuousAudio = true;
    startNewAudioChunk(); // see function below

    // 6) Video Recorder: 500ms intervals (unchanged)
    videoRecorder = new MediaRecorder(videoStream, {
      mimeType: "video/mp4",
    });
    videoRecorder.ondataavailable = (e) => {
      if (e.data.size > 0) {
        // If you actually need these video chunks, you can send them here
        const reader = new FileReader();
        reader.onload = () => {
          socket.emit("video_chunk", { chunk: reader.result });
        };
        reader.readAsArrayBuffer(e.data);
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
  // Stop continuous audio
  isContinuousAudio = false;
  if (audioRecorder && audioRecorder.state === "recording") {
    audioRecorder.stop();
  }

  // Stop the video recorder
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

/**
 * Start recording a new 10s audio chunk with MediaRecorder.
 * Once it completes, we emit the chunk to the server,
 * and if we're still capturing, we start a new chunk again.
 */
function startNewAudioChunk() {
  if (!isContinuousAudio || !audioStream) return;

  recordedAudioChunks = [];

  audioRecorder = new MediaRecorder(audioStream, {
    mimeType: "audio/mp4",
  });

  // Collect data in recordedAudioChunks
  audioRecorder.ondataavailable = (e) => {
    if (e.data && e.data.size > 0) {
      recordedAudioChunks.push(e.data);
    }
  };

  // When this chunk stops, we finalize and send it
  audioRecorder.onstop = async () => {
    // Combine all chunks into a single valid MP4
    const mp4Blob = new Blob(recordedAudioChunks, { type: "audio/mp4" });
    const arrayBuf = await mp4Blob.arrayBuffer();

    // Emit the MP4 chunk to server (fully closed MP4 container)
    socket.emit("audio_chunk", arrayBuf);
    console.log("Sent a 10s MP4 chunk to server. Size:", arrayBuf.byteLength);

    // If we're still supposed to keep capturing, start another 10s chunk
    if (isContinuousAudio) {
      startNewAudioChunk();
    }
  };

  // Start recording this chunk
  audioRecorder.start();
  console.log("Started a 10s chunk...");

  // Automatically stop after 10 seconds
  setTimeout(() => {
    if (isContinuousAudio && audioRecorder.state === "recording") {
      audioRecorder.stop();
    }
  }, 10000);
}

// Optional beep logic
const beep = new Audio("/static/sounds/beep.mp3");

function playBeep() {
  beep.currentTime = 0;
  beep.play().catch((err) => console.log("Playback blocked:", err));
}

// Listen for gesture responses
socket.on("gesture_response", (data) => {
  console.log("Received Gesture Response:", data.message);
  if (data.message == "ok") {
    playBeep();
  }
});

