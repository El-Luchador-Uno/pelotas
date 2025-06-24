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

        # If needed we can resize the frame to ease the compute load, but the model performance is significantly worse
        # frame = cv2.resize(frame, (frame.shape[1] // 2, frame.shape[0] // 2)) 
            
        results = model.predict(source=frame, imgsz=640, conf=0.5)

        for r in results:
            boxes = r.boxes 
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])
                print(f"Ball detected at ({x1}, {y1}) to ({x2}, {y2}) with confidence: {conf:.2f}")
                
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"Bouncy Ball: {conf:.2f}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                # TODO: need to programmtically find the bottom center of the frame
                cv2.circle(frame, (960, 1070), 10, (255, 0, 0), 2) 
        
        # Check for keyboard interrupt to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        elapsed = time.time() - start_time
        if elapsed < frame_interval:
            time.sleep(frame_interval - elapsed)
    
    # Clean up
    cap.release()