import cv2
import numpy as np
import io
import av  # PyAV library for video decoding
from flask import Flask, request, render_template
from flask_socketio import SocketIO
from gesture import detect_gesture  # Import your gesture detection function
import assemblyai as aai
import wave
import av  # PyAV for audio decoding
import ffmpeg  # Streaming-friendly decoding
import subprocess

import tempfile

from get_audio import *

from oursecrets import ASSEMBLY_API_KEY

transcript = ""

# Set AssemblyAI API Key
aai.settings.api_key = ASSEMBLY_API_KEY

# Initialize the transcriber
transcriber = aai.RealtimeTranscriber(
    sample_rate=16_000,
    on_data=lambda transcript: process_transcript(transcript),
    on_error=lambda error: print("An error occurred:", error),
    on_open=lambda session: print("Session ID:", session.session_id),
    on_close=lambda: print("Closing Session"),
)

transcriber.connect()

audio_buffer = bytearray()


app = Flask(__name__)
app.config["SECRET_KEY"] = "secret-hackathon-key"

# Allow all CORS origins for demo. In production, limit this!
socketio = SocketIO(app, cors_allowed_origins="*")

video_buffer = bytearray()

def process_transcript(transcript):
    """Send transcribed text to the frontend."""
    if transcript.text:
        print("Transcribed:", transcript.text)


@app.route("/")
def index():
    return render_template("index.html")


def decode_to_pcm16(raw_audio_bytes):
    """
    Use ffmpeg to decode raw container/codec data to PCM s16le, 16kHz, mono.
    raw_audio_bytes is the raw chunk from the browser's MediaRecorder.
    """

    # Construct the ffmpeg command:
    # -i pipe:0        -> read from stdin (the raw audio chunk)
    # -ac 1            -> convert to mono
    # -ar 16000        -> convert to 16kHz
    # -f s16le         -> output 16-bit PCM
    # pipe:1           -> write to stdout
    command = [
        'ffmpeg',
        '-y',                  # overwrite output if needed
        '-i', 'pipe:0',       # input is stdin
        '-ac', '1',           # single channel
        '-ar', '16000',       # 16 kHz
        '-f', 's16le',        # 16-bit PCM
        'pipe:1'
    ]

    # Launch ffmpeg process
    process = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    out, err = process.communicate(input=raw_audio_bytes)

    if process.returncode != 0:
        error_msg = err.decode("utf-8", errors="ignore")
        raise RuntimeError(f"ffmpeg decoding failed: {error_msg}")

    # 'out' should now be the raw 16-bit, 16kHz, mono PCM data
    return out



# "decode_buffer" accumulates raw mp4 data until we can decode at least one frame.
decode_buffer = bytearray()

# "pcm_buffer" accumulates decoded PCM data. We only send to AssemblyAI once
# we have at least BUFFER_SIZE_THRESHOLD bytes.
pcm_buffer = bytearray()

# For 16 kHz, mono, 16-bit PCM: 16000 samples/sec * 2 bytes/sample = 32000 bytes/sec
# If we want 100ms, that’s 3200 bytes. Let's use that as a threshold.
BUFFER_SIZE_THRESHOLD = 3200


@socketio.on("audio_chunk")
def handle_audio_chunk(raw_mp4_bytes):
    """
    Receives a single ~10-second .mp4 audio chunk as raw bytes,
    decodes it with PyAV, re-encodes as MP3, and saves to a temp file.
    """

    print(f"Received chunk of length: {len(raw_mp4_bytes)}")

    global transcript
    try:
        # 1) Create a named temp file for the final MP3
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_mp3:
            mp3_path = temp_mp3.name

        # 2) Open the incoming .mp4 data as an in-memory container
        input_container = av.open(io.BytesIO(raw_mp4_bytes), format="mp4", mode="r")

        # 3) Create an output container for MP3
        output_container = av.open(mp3_path, mode="w", format="mp3")

        # 4) Add an MP3 audio stream to the output container
        #    If PyAV complains, try specifying "libmp3lame" explicitly, 
        #    e.g. output_container.add_stream("libmp3lame", rate=44100)
        audio_stream = output_container.add_stream("mp3")

        # 5) Decode frames from the input
        in_audio_stream = input_container.streams.audio[0]
        for frame in input_container.decode(in_audio_stream):
            # Encode each frame to MP3
            packet = audio_stream.encode(frame)
            if packet:
                output_container.mux(packet)

        # 6) Flush the encoder
        # Pass None to indicate "no more frames"
        flush_packet = audio_stream.encode(None)
        if flush_packet:
            output_container.mux(flush_packet)

        # 7) Close both containers
        output_container.close()
        input_container.close()

        print(f"Saved MP3 to: {mp3_path}")

        # Optionally, notify the client
        #emit("save_status", f"Saved MP3 to {mp3_path}")

        # TRANSCRIBE

        delta = transcribe_audio(filename=mp3_path)

        transcript += delta

        print(transcript)

    except Exception as e:
        print(f"Error: {e}")
        #emit("save_status", f"Error: {e}")


# @socketio.on("audio_chunk")
# def handle_audio_chunk(raw_chunk):
#     return
#     """
#     Receives raw .mp4 chunk from the client. We'll buffer it and decode with PyAV.
#     """
#     global decode_buffer, pcm_buffer

#     # Append the new chunk to the decode_buffer
#     decode_buffer.extend(raw_chunk)

#     # Attempt to decode frames from decode_buffer using PyAV
#     # Because we might have partial frames, we do this in a loop until no more frames are found.
#     while True:
#         # We'll open an in-memory container using whatever data we have so far.
#         container = None
#         try:
#             container = av.open(io.BytesIO(decode_buffer), format="mp4", mode='r')
#         except Exception as e:
#             # If PyAV can't open it yet (partial data/corrupt), break and wait for more
#             break

#         # Attempt to decode audio frames
#         decoded_any_frame = False

#         try:
#             stream = container.streams.audio[0]  # We assume there's one audio stream
#         except IndexError:
#             # No audio stream found (unlikely in typical .mp4 audio)
#             container.close()
#             break

#         # We'll create a resampler for 16-bit, 16kHz, mono
#         # If your mp4 is already 16kHz, mono, 16-bit, you could skip the resampler.
#         resampler = av.audio.resampler.AudioResampler(
#             format='s16',
#             layout='mono',
#             rate=16000
#         )

#         # Try to decode frames
#         new_decode_buffer = bytearray()  # We'll reassemble leftover data
#         try:
#             # As we read frames, PyAV consumes some portion of "decode_buffer".
#             # However, PyAV doesn't directly tell us how many bytes it used.
#             # We'll have to rely on container.read() to see how many frames we get.
#             for frame in container.decode(stream):
#                 decoded_any_frame = True
#                 # Resample to ensure 16kHz mono s16
#                 resampled_frame = resampler.resample(frame)
#                 # Convert to raw bytes
#                 pcm_data = resampled_frame.to_ndarray().tobytes()
#                 pcm_buffer.extend(pcm_data)
#         except Exception as e:
#             # If we can't decode further frames, maybe partial/corrupt
#             pass

#         # We close the container to flush any resources
#         container.close()

#         if not decoded_any_frame:
#             # No frames were decoded => we likely didn't have enough data yet.
#             # We'll wait for more data from the client.
#             break
#         else:
#             """
#             Now, PyAV might have consumed some portion of decode_buffer internally,
#             but it doesn't automatically remove those bytes. Typically, partial or 
#             leftover data remains at the end. There's no built-in "used bytes" count 
#             from PyAV to tell us how many bytes were consumed.
            
#             The simplest approach is:
#                 1) If we successfully decoded frames, we *assume* we used up all
#                    decode_buffer data for those frames.
#                 2) We set decode_buffer = bytearray() and break.
            
#             Or, if you suspect partial leftover at the end, you can re-try or 
#             keep a rolling approach. But in practice, for small chunk-based usage, 
#             resetting decode_buffer after successful decode is often enough.
#             """
#             decode_buffer = bytearray()  # Clear the decode buffer
#             # There's a chance we had leftover partial data from the container,
#             # but PyAV doesn't provide a direct leftover. For chunk-based streaming,
#             # we typically discard or re-buffer in a more advanced approach.
#             break

#     # Now we have new PCM data in `pcm_buffer`. Check if we exceed threshold.
#     # If so, we repeatedly send out 3200-byte segments until we're under threshold.
#     while len(pcm_buffer) >= BUFFER_SIZE_THRESHOLD:
#         # Extract a 3200-byte chunk (for example)
#         segment = pcm_buffer[:BUFFER_SIZE_THRESHOLD]
#         # Send that to AssemblyAI
#         print("sending!!!")
#         transcriber.send(segment)
#         # Remove that part from the buffer
#         del pcm_buffer[:BUFFER_SIZE_THRESHOLD]

# @socketio.on("audio_chunk")
# def handle_audio_chunk(data):
#     """
#     Receives raw audio chunks, decodes using FFMPEG, and streams to AssemblyAI.
#     """
#     try:
#         audio_bytes = data.get("chunk", None)

#         if not audio_bytes or len(audio_bytes) < 1000:
#             print(f"Warning: Received very small audio chunk ({len(audio_bytes)} bytes). Skipping.")
#             return

#         # Decode raw audio bytes (WebM/MP4) to PCM using FFmpeg
#         process = (
#             ffmpeg
#             .input("pipe:0", format="mp4")  # Set format dynamically
#             .output("pipe:1", format="wav", acodec="pcm_s16le", ac=1, ar="16k")  # PCM 16-bit, mono, 16kHz
#             .run_async(pipe_stdin=True, pipe_stdout=True, pipe_stderr=True)
#         )

#         pcm_audio, _ = process.communicate(input=audio_bytes)  # Decode raw bytes

#         if not pcm_audio:
#             print("Warning: No valid PCM audio decoded. Skipping.")
#             return

#         # Stream to AssemblyAI
#         transcriber.stream(pcm_audio)

#     except Exception as e:
#         print("Error processing audio chunk:", e)



# @socketio.on("audio_chunk")
# def handle_audio_chunk(data):
#     """
#     Receives raw audio chunks from the frontend.
#     Decodes them from MP4/WebM, converts to WAV, and streams to AssemblyAI.
#     """
#     try:
#         audio_bytes = data["chunk"]  # Raw binary audio (MP4/WebM format)

#         if not audio_bytes or len(audio_bytes) < 1000:
#             print(f"Warning: Received very small audio chunk ({len(audio_bytes)} bytes). Skipping.")
#             return

#         print('ok 1')

#         # Convert raw audio bytes to an in-memory file
#         audio_stream = io.BytesIO(audio_bytes)
#         print("ok 2")
#         # Decode MP4/WebM audio using PyAV
#         container = av.open(audio_stream, format="mp4")  # or "webm" if using webm
#         print("ok 2")
#         audio_frames = container.decode(audio=0)

#         pcm_data = b""  # Buffer for decoded PCM audio

#         print(f"frames len: {len(audio_frames)}")
#         for frame in audio_frames:
#             # Convert to 16-bit PCM (Mono)
#             pcm_data += frame.to_ndarray().astype(np.int16).tobytes()

#         # Ensure the correct sample rate (16,000Hz) and channel format
#         wav_buffer = io.BytesIO()
#         with wave.open(wav_buffer, "wb") as wav_file:
#             wav_file.setnchannels(1)  # Mono audio
#             wav_file.setsampwidth(2)  # 16-bit PCM
#             wav_file.setframerate(16_000)
#             wav_file.writeframes(pcm_data)

#         # Send audio to AssemblyAI
#         transcriber.stream(wav_buffer.getvalue())

#     except Exception as e:
#         print("Error processing audio chunk:", e)


# @socketio.on("audio_chunk")
# def handle_audio_chunk(data):
#     """
#     Receives small audio chunks (near real-time, e.g. every 100ms)
#     data["chunk"] is a Latin1 string representing raw binary data from MediaRecorder.
#     """
#     #audio_bytes = data["chunk"]

#     try:
#         audio_bytes = data["chunk"]  # Raw binary audio

#         # Convert raw MP4/WEBM bytes to WAV format for AssemblyAI
#         np_audio = np.frombuffer(audio_bytes, dtype=np.int16)

#         # Ensure the correct sample rate (16,000Hz) and channel format
#         wav_buffer = io.BytesIO()
#         with wave.open(wav_buffer, "wb") as wav_file:
#             wav_file.setnchannels(1)  # Mono audio
#             wav_file.setsampwidth(2)  # 16-bit PCM
#             wav_file.setframerate(16_000)
#             wav_file.writeframes(np_audio.tobytes())

#         # Send audio to AssemblyAI
#         transcriber.stream(wav_buffer.getvalue())

#     except Exception as e:
#         print("Error processing audio chunk:", e)
#     #print(f"Received AUDIO chunk of size: {len(audio_bytes)} bytes")


@socketio.on("image_chunk")
def handle_image_chunk(data):
    try:
        np_arr = np.frombuffer(data["chunk"], np.uint8)
        
        # Decode image from bytes (JPEG) into an OpenCV BGR format
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if frame is None:
            print("Error decoding image frame")
            return

        detected_gesture = detect_gesture(frame)  # Process latest frame

        print(f"\n\ndetected_gesture: {detected_gesture}\n\n")
        response_message = "ok" if detected_gesture in ['thumbs_up', 'thumbs_down', 'five_fingers'] else ""
        socketio.emit("gesture_response", {"message": response_message})

    except Exception as e:
        print(f"Error processing image frame: {e}")

        

# deprecated...
@socketio.on("video_chunk")
def handle_video_chunk(data):
    """
    Receives small video chunks (e.g. every 500ms).
    data["chunk"] is a Latin1 string representing raw binary data from MediaRecorder.
    """
    return
    global video_buffer
    video_bytes = data["chunk"]  # Raw binary data
    video_buffer.extend(video_bytes)  # Append new chunk to buffer

    try:
        # Convert buffer to an in-memory file-like object
        video_stream = io.BytesIO(video_buffer)

        # Use PyAV to decode video chunks
        container = av.open(video_stream, format="mp4")  # Decode as MP4

        last_frame = None
        for frame in container.decode(video=0):
            #last_frame = frame.to_ndarray(format="bgr24")  # Convert to BGR (OpenCV format)
            last_frame = frame

        last_frame_conv = last_frame.to_ndarray(format="bgr24")

        if last_frame_conv is not None:
            detected_gesture = detect_gesture(last_frame_conv)  # Process latest frame

            print(f"\n\ndetected_gesture: {detected_gesture}\n\n")
            response_message = "ok" if detected_gesture in ['thumbs_up', 'thumbs_down', 'five_fingers'] else ""
            socketio.emit("gesture_response", {"message": response_message})
        
        # Clear buffer after processing
       # video_buffer.clear()

    except Exception as e:
        print(f"Error processing video chunk: {e}")


    #video_bytes = data["chunk"]
    #print(f"Received VIDEO chunk of size: {len(video_bytes)} bytes")


if __name__ == "__main__":
    # Run on 0.0.0.0 to allow external access. 
    # Use debug=True for auto-reload in dev.
    socketio.run(app, host="0.0.0.0", port=7070, debug=True)
