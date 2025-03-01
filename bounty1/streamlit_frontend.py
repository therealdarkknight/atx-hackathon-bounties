import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings
import av
import cv2
import base64
import requests

FLASK_ENDPOINT = "http://127.0.0.1:5000/process_frame"

st.title("Streamlit WebRTC Demo")

# Simple global counter
frame_counter = 0

def video_frame_callback(frame):
    global frame_counter
    frame_counter += 1

    img = frame.to_ndarray(format="bgr24")

    # Encode as JPEG
    ret, jpeg = cv2.imencode(".jpg", img)
    if not ret:
        return frame

    # Every 10 frames, send to Flask
    if frame_counter % 10 == 0:
        frame_b64 = base64.b64encode(jpeg.tobytes()).decode("utf-8")
        frame_b64_str = f"data:image/jpg;base64,{frame_b64}"

        try:
            response = requests.post(
                FLASK_ENDPOINT,
                json={"frame": frame_b64_str},
                timeout=3  # Increase if needed
            )
            if response.status_code == 200:
                print("Server response:", response.json())
            else:
                print("Server error:", response.text)
        except Exception as e:
            print("Exception in sending frame:", e)

    # Return the frame for local preview
    return av.VideoFrame.from_ndarray(img, format="bgr24")

webrtc_ctx = webrtc_streamer(
    key="example",
    # Switch to SENDRECV for local preview
    mode=WebRtcMode.SENDRECV,
    client_settings=ClientSettings(
        rtc_configuration={
            "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
        },
        media_stream_constraints={
            "video": True,
            "audio": True  # set to True only if you also want audio
        },
    ),
    video_frame_callback=video_frame_callback,
)

st.write("Open the dev console to see Flask server responses.")
