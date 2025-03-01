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

    const audio_reader = new FileReader();

    audio_reader.onload = () => {
        // Send raw binary data directly, no conversion to Latin1
        socket.emit("audio_chunk", { chunk: audio_reader.result });
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
        console.log("audio");
        if (e.data.size > 0) {
          audio_reader.readAsArrayBuffer(e.data);
        }
      };
    audioRecorder.start(10); // get ~100ms audio chunks

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
