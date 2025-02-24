import cv2
import numpy as np
from deepface import DeepFace
from ultralytics import YOLO
import datetime
import logging
from dataclasses import dataclass
from typing import List, Tuple, Dict
import pandas as pd

# Yeh class ek single detection ka result store karegi
@dataclass
class DetectionResult:
    timestamp: datetime.datetime
    people_count: int
    movement_speed: float
    panic_expressions: int
    weapons_detected: List[str]
    stampede_probability: float
    new_weapon_detected: bool = False
    
class StampedeDetector:
    def __init__(self, people_threshold: int = 25, speed_threshold: float = 40.0, panic_threshold: float = 0.6):
        # YOLO model load kiya, jo log aur objects detect karega
        self.yolo_model = YOLO('yolov8n.pt')
        
        # OpenCV ka face detector load kiya
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        self.prev_frame = None  # Pehle wala frame store karne ke liye
        
        # Thresholds jo alert trigger karenge
        self.people_threshold = people_threshold
        self.speed_threshold = speed_threshold
        self.panic_threshold = panic_threshold
        
        # Dangerous objects ki list, jo agar detect hue to alert milega
        self.dangerous_objects = [28, 43, 67, 73, 76, 77, 85, 86, 87, 88, 89, 90]
        
        # Logging ka setup, jo incidents ko file me store karega
        logging.basicConfig(
            filename='stampede_events.log',
            level=logging.INFO,
            format='%(asctime)s - %(message)s'
        )
        
        # Results store karne ke liye Pandas DataFrame
        self.results_df = pd.DataFrame(columns=['timestamp', 'people_count', 'movement_speed', 'panic_expressions', 'weapons_detected', 'stampede_probability'])
        
        # Pehle detect hue weapons ko store karne ke liye
        self.prev_weapons = set()

    # YOLO ka use karke log detect karega frame me
    def detect_people(self, frame):
        results = self.yolo_model(frame, classes=[0])  # Class 0 means person
        return len(results[0].boxes), results[0].boxes
    
    # Optical flow se movement speed analyze karega
    def analyze_movement(self, frame):
        if self.prev_frame is None:
            self.prev_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            return 0.0
        
        current_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        flow = cv2.calcOpticalFlowFarneback(self.prev_frame, current_frame, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        speed = np.mean(np.abs(flow))
        self.prev_frame = current_frame
        return speed
    
    # DeepFace ka use karke panic detect karega
    def detect_panic(self, frame):
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            panic_count = 0
            
            for (x, y, w, h) in faces:
                face_img = frame[max(0, y-20):min(frame.shape[0], y+h+20), max(0, x-20):min(frame.shape[1], x+w+20)]
                if face_img.size == 0:  
                    continue
                
                result = DeepFace.analyze(face_img, actions=['emotion'], enforce_detection=False, detector_backend='opencv')
                if isinstance(result, list):
                    result = result[0]
                
                # Agar fear, anger ya surprise detect hua to count badhao
                if result['dominant_emotion'] in ['fear', 'angry', 'surprise']:
                    panic_count += 1
                    
            return panic_count
        except Exception as e:
            logging.error(f"Face analysis error: {str(e)}")
            return 0
    
    # YOLO ka use karke dangerous objects detect karega
    def detect_weapons(self, frame):
        results = self.yolo_model(frame, classes=self.dangerous_objects, conf=0.35)
        detected_objects = []
        current_weapons = set()
        
        for box in results[0].boxes:
            class_id = int(box.cls[0])
            conf = float(box.conf[0])
            if conf > 0.35:
                object_name = self.yolo_model.names[class_id]
                detected_objects.append(f"{object_name} ({conf:.2f})")
                current_weapons.add(object_name)
        
        new_weapons = current_weapons - self.prev_weapons
        self.prev_weapons = current_weapons
        
        return detected_objects, bool(new_weapons)
    
    # Stampede ka probability calculate karega
    def calculate_stampede_probability(self, people_count, movement_speed, panic_count, weapons):
        probability = 0.0
        if people_count > self.people_threshold:
            probability += 0.40 * min(people_count / self.people_threshold, 1.0)
        if movement_speed > self.speed_threshold:
            probability += 0.25 * min(movement_speed / self.speed_threshold, 1.0)
        if panic_count > 0:
            probability += 0.25 * min(panic_count / (people_count or 1), 1.0)
        if weapons:
            probability += 0.10 * min(len(weapons) / 2, 1.0)
        return min(probability, 1.0) * 100
    
    # Har frame ko process karega aur result return karega
    def process_frame(self, frame):
        people_count, boxes = self.detect_people(frame)
        movement_speed = self.analyze_movement(frame)
        panic_count = self.detect_panic(frame)
        weapons, new_weapon_detected = self.detect_weapons(frame)
        probability = self.calculate_stampede_probability(people_count, movement_speed, panic_count, weapons)
        
        result = DetectionResult(
            timestamp=datetime.datetime.now(),
            people_count=people_count,
            movement_speed=movement_speed,
            panic_expressions=panic_count,
            weapons_detected=weapons,
            stampede_probability=probability,
            new_weapon_detected=new_weapon_detected
        )
        
        if probability > 70 or new_weapon_detected:
            logging.warning(f"{'NEW WEAPON DETECTED! ' if new_weapon_detected else ''}High stampede risk detected! Probability: {probability:.1f}% People: {people_count} Speed: {movement_speed:.2f} Panic: {panic_count} Objects: {', '.join(weapons)}")
        
        self.results_df.loc[len(self.results_df)] = [result.timestamp, result.people_count, result.movement_speed, result.panic_expressions, result.weapons_detected, result.stampede_probability]
        
        return result, boxes
