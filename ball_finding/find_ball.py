import cv2
from ultralytics import YOLO
import os

def find_ball():
    model_path = os.path.join(os.path.dirname(__file__), "best.torchscript")
    model = YOLO(model_path)
    
    cap = cv2.VideoCapture(0) 
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        print(frame.shape)
            
        results = model.predict(source=frame, imgsz=640, conf=0.5)

        for r in results:
            boxes = r.boxes 
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])
                print(f"Ball detected at ({x1}, {y1}) to ({x2}, {y2}) with confidence: {conf:.2f}")
                
                # Draw on frame for processing (but don't display)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"Bouncy Ball: {conf:.2f}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                
                cv2.circle(frame, (960, 1070), 10, (255, 0, 0), 2)
        
        # Check for keyboard interrupt to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Clean up
    cap.release()