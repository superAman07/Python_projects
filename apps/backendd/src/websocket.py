import cv2
import base64
import numpy as np
from flask import Flask
from flask_socketio import SocketIO
from stampede_detector import StampedeDetector
from visualization import VisualizationManager

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

def generate_frames():
    cap = cv2.VideoCapture(0)
    
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    detector = StampedeDetector()
    visualizer = VisualizationManager(frame_width, frame_height)

    while True:
        success, frame = cap.read()
        if not success:
            break
        
        output = detector.process_frame(frame)
        
        # Handling response format properly
        if len(output) == 2:
            result, boxes = output
            logs = "No logs available"
        else:
            result, boxes, logs = output

        frame = visualizer.draw_boxes(frame, boxes)
        frame = visualizer.draw_stats(frame, result)

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = base64.b64encode(buffer).decode('utf-8')

        socketio.emit('log_data', {"log": logs})
        print("Emitted logs:", logs)
        socketio.emit('video_frame', {'frame': frame_bytes})
        
        socketio.sleep(0.1)

@socketio.on('connect')
def connect():
    print("Client connected")
    socketio.start_background_task(generate_frames)

if __name__ == "__main__":
    print("Starting WebSocket Server...")
    socketio.run(app, host='0.0.0.0', port=5000)  # Debug mode removed
