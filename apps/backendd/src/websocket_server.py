import asyncio
import websockets
import json
from stampede_detector import StampedeDetector
from visualization import VisualizationManager
import cv2

async def send_data(websocket, path):
    if path == "/ws/data":
        cap = cv2.VideoCapture(0)
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        detector = StampedeDetector()
        visualizer = VisualizationManager(frame_width, frame_height)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            result, boxes = detector.process_frame(frame)
            data = {
                "people_count": result.people_count,
                "movement_speed": result.movement_speed,
                "stampede_probability": result.stampede_probability,
            }
            await websocket.send(json.dumps(data))
            await asyncio.sleep(0.1)  # Adjust the frequency as needed

        cap.release()
    elif path == "/ws/video":
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            _, buffer = cv2.imencode('.jpg', frame)
            await websocket.send(buffer.tobytes())
            await asyncio.sleep(0.1)  # Adjust the frequency as needed

        cap.release()

async def main():
    async with websockets.serve(send_data, "localhost", 8000):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())