from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret-hackathon-key"

# Allow all CORS origins for demo. In production, limit this!
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("audio_chunk")
def handle_audio_chunk(data):
    """
    Receives small audio chunks (near real-time, e.g. every 100ms)
    data["chunk"] is a Latin1 string representing raw binary data from MediaRecorder.
    """
    audio_bytes = data["chunk"]
    print(f"Received AUDIO chunk of size: {len(audio_bytes)} bytes")

    # Here you can decode or process audio_bytes as needed

@socketio.on("video_chunk")
def handle_video_chunk(data):
    """
    Receives small video chunks (e.g. every 500ms).
    data["chunk"] is a Latin1 string representing raw binary data from MediaRecorder.
    """
    video_bytes = data["chunk"]
    print(f"Received VIDEO chunk of size: {len(video_bytes)} bytes")

    # Here you can decode or process video_bytes as needed

if __name__ == "__main__":
    # Run on 0.0.0.0 to allow external access. 
    # Use debug=True for auto-reload in dev.
    socketio.run(app, host="0.0.0.0", port=7070, debug=True)
