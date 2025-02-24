import cv2
import numpy as np
from typing import Tuple, List
import tkinter as tk
from tkinter import messagebox  # Bas sundarta ke liye... 😎
import threading
import time
from collections import deque

# Yeh class frame visualize karne ke liye hai
class VisualizationManager:
    def __init__(self, frame_width: int, frame_height: int):
        self.frame_width = frame_width  # Frame ka width store karne ka
        self.frame_height = frame_height  # Frame ka height store karne ka
        self.font = cv2.FONT_HERSHEY_SIMPLEX  # Jo text likhna ho uska font set kar diya
        self.warning_alpha = 0.0  # Warning ka transparency level rakha
        self.last_popup_time = 0  # Last popup kab dikhaya tha
        self.popup_cooldown = 4  # Kitne seconds ke gap me popup aaye

        # Tkinter ka setup sirf popups ke liye
        self.root = tk.Tk()
        self.root.withdraw()  # Window dikhane ki zarurat nahi

        # Trend analysis ke liye setup
        self.probability_history = deque(maxlen=30)  # Last 30 frames ka data store hoga
        self.trend_threshold = 1.5  # Agar risk fast increase ho raha toh alert dena hai
        self.predictive_warning = False  # Pehle se koi prediction warning active nahi
        self.last_predictive_popup = 0  # Last predictive popup kab aaya

        # Camera disruption detect karne ke liye setup
        self.last_frame_time = time.time()  # Last frame ka timestamp
        self.frame_timeout = 0.5  # 500ms ke andar naye frame na aaye toh alert
        self.camera_disrupted = False  # Pehle se disruption nahi hai

    def analyze_trend(self, current_probability: float) -> bool:
        """Check kar raha ki risk increase ho raha ya nahi"""
        self.probability_history.append(current_probability)

        if len(self.probability_history) < 10:  # Agar 10 se kam data points hain toh kuch nahi karna
            return False

        # Last 10 frames ka rate of change calculate kar raha
        recent_values = list(self.probability_history)[-10:]
        rate_of_change = (recent_values[-1] - recent_values[0]) / len(recent_values)

        # 5 second baad ka risk estimate kar raha (30 fps assume karke)
        predicted_probability = current_probability + (rate_of_change * 150)

        return (rate_of_change > self.trend_threshold and 
                predicted_probability > 70 and 
                current_probability > 40)  # Risk 40+ ho aur badhne ke chances ho tabhi alert dena hai

    def check_camera_disruption(self, frame) -> bool:
        """Check kar raha camera feed theek hai ya disrupt ho gaya"""
        current_time = time.time()

        # Frame ko gray bana ke blur aur brightness check kar raha
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()
        brightness = np.mean(gray)

        # Time difference check kar raha previous frame se
        time_gap = current_time - self.last_frame_time
        self.last_frame_time = current_time

        # Agar koi bhi issue ho toh disruption detect ho jayega
        is_disrupted = (
            time_gap > self.frame_timeout or  # Frame delay ho raha kya
            blur_score < 50 or  # Blur ho gaya kya
            brightness < 30 or  # Andhera ho gaya kya
            brightness > 250  # Zyada chamak aa rahi kya
        )

        if is_disrupted and not self.camera_disrupted:
            self.show_popup_warning(100, camera_alert=True)  # Camera disruption alert dega
            self.camera_disrupted = True
        elif not is_disrupted:
            self.camera_disrupted = False

        return is_disrupted

    def show_popup_warning(self, probability: float, predictive: bool = False, 
                           weapon_alert: bool = False, camera_alert: bool = False):
        """Ye popup dikhane ka function hai, alag thread me chalega"""
        current_time = time.time()
        if camera_alert:
            if current_time - self.last_popup_time >= self.popup_cooldown:
                self.last_popup_time = current_time
                thread = threading.Thread(target=self._display_camera_alert)
                thread.daemon = True
                thread.start()
        elif predictive:
            if current_time - self.last_predictive_popup >= self.popup_cooldown:
                self.last_predictive_popup = current_time
                thread = threading.Thread(target=self._display_predictive_popup, args=(probability,))
                thread.daemon = True
                thread.start()
        else:
            if current_time - self.last_popup_time >= self.popup_cooldown:
                self.last_popup_time = current_time
                thread = threading.Thread(target=self._display_popup, args=(probability,))
                thread.daemon = True
                thread.start()

    def _display_popup(self, probability: float):
        """Normal alert popup dikhayega"""
        messagebox.showwarning("⚠️", f"Risk Level: {probability:.1f}%\nTake Action Now!")

    def _display_camera_alert(self):
        """Camera issue ka alert dikhayega"""
        messagebox.showwarning("🎥", "Camera Disruption Detected!\nPossible Security Threat")

    def _display_predictive_popup(self, probability: float):
        """Agar risk badhne wala hai toh alert dikhayega"""
        messagebox.showwarning("🚨 Alert", f"Risk Increasing!\nLevel: {probability:.1f}%\n• Act now\n• Control crowd\n• Ready protocols")

    def draw_boxes(self, frame, boxes, color=(0, 255, 0)):
        """Frame pe bounding boxes draw karega"""
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        return frame

    def draw_stats(self, frame, result):
        """Frame pe stats aur alerts draw karega"""
        camera_disrupted = self.check_camera_disruption(frame)

        # Panel ka color decide kar raha based on alerts
        if camera_disrupted or result.new_weapon_detected or result.stampede_probability > 70:
            panel_color = (0, 0, 255)  # Red alert
        else:
            panel_color = (0, 255, 0)  # Green normal

        # Neeche ek panel bana raha info dikhane ke liye
        panel_height = 100
        panel_y = self.frame_height - panel_height - 10
        cv2.rectangle(frame, (10, panel_y), (300, self.frame_height - 10), panel_color, -1)

        # Stats dikhane ke liye text add kar raha
        font_size = 0.4
        base_y = panel_y + 25
        line_spacing = 20

        cv2.putText(frame, f"People: {result.people_count}", (20, base_y), self.font, font_size, (255, 255, 255), 1)
        cv2.putText(frame, f"Speed: {result.movement_speed:.1f}", (20, base_y + line_spacing), self.font, font_size, (255, 255, 255), 1)
        cv2.putText(frame, f"Panic: {result.panic_expressions}", (20, base_y + 2 * line_spacing), self.font, font_size, (255, 255, 255), 1)

        # Risk level ka text
        risk_text = f"Risk: {result.stampede_probability:.1f}%" if not camera_disrupted else "CAMERA DISRUPTED - SECURITY ALERT"
        cv2.putText(frame, risk_text, (20, base_y + 3 * line_spacing), self.font, font_size, (255, 0, 0), 1)

        return frame  # Frame return kar raha with updates
