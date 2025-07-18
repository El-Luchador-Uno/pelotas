import cv2
import uuid
import os

def take_picture():
    cap = cv2.VideoCapture(0)
    _, frame = cap.read()
    pic_id = uuid.uuid4()
    filename = f"{str(pic_id)}.jpg"
    output_dir = os.path.expanduser("~/training")
    full_path = os.path.join(output_dir, filename)
    cv2.imwrite(full_path, frame)
    cap.release()

