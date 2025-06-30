import cv2
from ultralytics import YOLO
import os
import time

def find_ball():
    model_path = os.path.join(os.path.dirname(__file__), "best.torchscript")
    model = YOLO(model_path, task="detect")
    
    cap = cv2.VideoCapture(0)

    desired_fps = 0.25 
    frame_interval = 1.0 / desired_fps 
    
    while True:
        start_time = time.time()
        
        num_of_frames_to_flush = 5

        for _ in range(num_of_frames_to_flush):
            cap.read()

        ret, frame = cap.read()
        if not ret:
            break
            
        results = model.predict(source=frame, imgsz=640, conf=0.5)

        frame_width = frame.shape[1]
        frame_center_x = frame_width / 2

        ACCEPTABLE_PERCENT_FROM_CENTER = 0.05

        acceptable_distance_from_center = ACCEPTABLE_PERCENT_FROM_CENTER * frame_center_x

        for r in results:
            boxes = r.boxes 
            for box in boxes:
                x1, _, x2, _ = map(int, box.xyxy[0])
                
                ball_center_x = (x1 + x2) / 2

                ball_distance_from_center = ball_center_x - frame_center_x

                if abs(ball_distance_from_center) < acceptable_distance_from_center:
                    print(f"Ball is centered {ball_center_x}, {frame_center_x}")
                elif ball_distance_from_center > 0:
                    print(f"Ball is right of center {ball_distance_from_center}, {frame_center_x}")
                elif ball_distance_from_center < 0:
                    print(f"Ball is left of center {ball_distance_from_center}, {frame_center_x}")

        # Check for keyboard interrupt to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        elapsed = time.time() - start_time
        if elapsed < frame_interval:
            time.sleep(frame_interval - elapsed)
    
    # Clean up
    cap.release()