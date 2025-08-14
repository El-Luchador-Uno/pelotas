import cv2
from ultralytics import YOLO
import os
from self_drive.drive import drive
import time
from constants import Direction

def find_ball(milliseconds_to_use: int, pwm_to_use: float, max_turns: int) -> bool:
    model_path = os.path.join(os.path.dirname(__file__), "best.torchscript")
    model = YOLO(model_path, task="detect")
    
    cap = cv2.VideoCapture(0)

    desired_fps = 0.50 
    frame_interval = 1.0 / desired_fps 

    current_iteration = 1
    ball_found = False
    
    try:
        while current_iteration <= max_turns:
            start_time = time.time()
            
            num_of_frames_to_flush = 5

            for _ in range(num_of_frames_to_flush):
                ret = cap.read()
                if not ret[0]:
                    print("Failed to flush frame")
                    break

            ret, frame = cap.read()
            if not ret:
                print("Failed to capture frame")
                break

            results = model.predict(source=frame, imgsz=640, conf=0.5)
            
            if len(results) > 0 and len(results[0].boxes) > 0:
                result = results[0]    
                for box in result.boxes:
                    class_id = int(box.cls[0])
                    class_name = result.names[class_id]
                    
                    if class_name.lower() == 'bouncy_ball':
                        ball_found = True
                        break
            
            if ball_found:
                break
            
            drive(dir=Direction.RIGHT, duration_in_milliseconds=milliseconds_to_use, pwm_speed=pwm_to_use)
            current_iteration += 1
            
            elapsed = time.time() - start_time
            if elapsed < frame_interval:
                time.sleep(frame_interval - elapsed)
    
    finally:
        cap.release()
        return ball_found