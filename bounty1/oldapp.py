# flask_app.py
from flask import Flask, request, jsonify
import base64
import cv2
import numpy as np

app = Flask(__name__)

@app.route("/")
def index():
    return "Flask backend is running!"

@app.route("/process_frame", methods=["POST"])
def process_frame():
    """
    Expects JSON payload with a key 'frame' that is a base64-encoded image string.
    """
    data = request.json
    if "frame" not in data:
        return jsonify({"error": "No frame data received"}), 400
    
    # Decode the base64 string
    frame_data = data["frame"].split(",")[-1]  # if "data:image/png;base64,..." then skip prefix
    img_bytes = base64.b64decode(frame_data)
    
    # Convert bytes to numpy array and decode as image
    np_arr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    
    # Here you could do any processing with OpenCV, etc.
    # For demo, let's just return the shape
    height, width, channels = img.shape
    
    print(f"received frame! {len(img_bytes)}")

    return jsonify({
        "message": "Frame processed",
        "height": height,
        "width": width,
        "channels": channels
    })

if __name__ == "__main__":
    # Run Flask on localhost port 5000
    app.run(host="0.0.0.0", port=7070, debug=True)
