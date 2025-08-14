import cv2
from ultralytics import YOLO
import os
import time
from self_drive.drive import drive
from constants import Direction
from self_drive.callibration import get_half_screen_turn
from ball_finding.find_ball import find_ball
from ball_finding.pickup_ball import pickup_ball

def find_ball_and_pickup():
    print("Callibrating turning power and duration")
    base_pwm_speed, base_duration_milliseconds = get_half_screen_turn()
    print(f"Base pwm speed: {base_pwm_speed}, base duration milliseconds: {base_duration_milliseconds}")

    print("Finding ball")
    # It takes 50 half screen turns to turn 360 degrees so 52 is used to make sure we turn enough
    ball_found = find_ball(milliseconds_to_use=base_duration_milliseconds, pwm_to_use=base_pwm_speed, max_turns=52)

    if not ball_found:
        print("Ball not found")
        return
    
    print("Ball found")
    
    model_path = os.path.join(os.path.dirname(__file__), "best.torchscript")
    model = YOLO(model_path, task="detect")
    
    cap = cv2.VideoCapture(0)

    desired_fps = 0.50 
    frame_interval = 1.0 / desired_fps 

    slow_down_multiplier = 0.3
    turn_multiplier = 0.2
    go_straight_multiplier = 0.75

    # If these conditions are met, the max pwm is already moving really slow and the robot probably
    # won't move at 0.3
    if base_pwm_speed == 1.0 and base_duration_milliseconds > 400:
        slow_down_multiplier = 0.7
    
    slow_pwm = base_pwm_speed * slow_down_multiplier
    slow_duration_milliseconds = 1500

    turn_pwm = base_pwm_speed
    turn_duration_milliseconds = base_duration_milliseconds * turn_multiplier
    go_straight_pwm = base_pwm_speed
    go_straight_milliseconds = base_duration_milliseconds * go_straight_multiplier

    last_ball_center_x = 0
    last_direction = Direction.UP
    
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
        frame_height = frame.shape[0]
        frame_center_x = frame_width / 2

        ACCEPTABLE_PERCENT_FROM_X_CENTER = 0.05
        ACCEPTABLE_PERCENT_FROM_Y_CENTER = .50

        acceptable_distance_from_center = ACCEPTABLE_PERCENT_FROM_X_CENTER * frame_center_x
        pickup_height = ACCEPTABLE_PERCENT_FROM_Y_CENTER * frame_height

        # Find the ball with highest confidence
        best_ball = None
        best_confidence = 0
        
        for r in results:
            boxes = r.boxes 
            for box in boxes:
                confidence = float(box.conf[0])
                if confidence > best_confidence:
                    best_confidence = confidence
                    best_ball = box
        
        if best_ball is not None:
            x1, y1, x2, y2 = int(best_ball.xyxy[0][0]), int(best_ball.xyxy[0][1]), int(best_ball.xyxy[0][2]), int(best_ball.xyxy[0][3])

            ball_center_x = (x1 + x2) / 2
            ball_center_y = (y1 + y2) / 2

            ball_distance_from_x_center = ball_center_x - frame_center_x
            ball_distance_from_y_bottom = frame_height - ball_center_y

            print(f"ball height: {ball_center_y}, distance from bottom: {ball_distance_from_y_bottom}")

            if abs(ball_distance_from_x_center) < acceptable_distance_from_center and ball_distance_from_y_bottom < pickup_height:
                    print(f"Ball is ready for pickup")
                    pickup_ball(drive_milliseconds=slow_duration_milliseconds, drive_pwm=slow_pwm)
                    break
            else:
                current_direction = None

                if abs(ball_distance_from_x_center) < acceptable_distance_from_center:
                    print(f"Ball is centered {ball_distance_from_x_center}, {frame_center_x}")
                    current_direction = Direction.UP
                    last_ball_center_x = 0
                elif ball_distance_from_x_center > 0:
                    print(f"Ball is right of center {ball_distance_from_x_center}, {frame_center_x}")
                    current_direction = Direction.RIGHT
                    last_ball_center_x += 1
                elif ball_distance_from_x_center < 0:
                    print(f"Ball is left of center {ball_distance_from_x_center}, {frame_center_x}")
                    current_direction = Direction.LEFT
                    last_ball_center_x += 1

                if current_direction is None:
                    raise ValueError("current_direction should not be none after checking ball location")
                
                if last_ball_center_x > 1 and current_direction != last_direction:
                    if turn_duration_milliseconds > 25:
                        turn_duration_milliseconds = turn_duration_milliseconds * 0.9
                    else:
                        turn_pwm = turn_pwm * 0.9

                pwm_to_drive = go_straight_pwm if current_direction == Direction.UP else turn_pwm
                milliseconds_to_drive = go_straight_milliseconds if current_direction == Direction.UP else turn_duration_milliseconds

                print(f"Driving, direction: {current_direction}, duration: {milliseconds_to_drive}, pwm_speed: {pwm_to_drive}")

                drive(dir=current_direction, duration_in_milliseconds=milliseconds_to_drive, pwm_speed=pwm_to_drive)
                last_direction = current_direction


        # Check for keyboard interrupt to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        elapsed = time.time() - start_time
        if elapsed < frame_interval:
            time.sleep(frame_interval - elapsed)
    
    # Clean up
    cap.release()