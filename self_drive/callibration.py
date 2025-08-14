import numpy as np
from self_drive.drive import drive
import cv2
from constants import Direction
import time
from typing import Optional, NamedTuple

STRIP_WIDTH = 10
CLOSE_ENOUGH = 2

class TurnCalibrationResult(NamedTuple):
    pwm_speed: float
    duration_milliseconds: int

def get_middle_strip(frame: np.ndarray) -> np.ndarray:
    _, width, _ = frame.shape
    center_x = width // 2
    half_strip = STRIP_WIDTH // 2
    start_x = max(center_x - half_strip, 0)
    end_x = min(center_x + half_strip, width)

    return frame[:, start_x:end_x, :]

def split_into_strips(frame: np.ndarray, strip_width: int) -> list[np.ndarray]:
    _, w, _ = frame.shape
    strips = []
    for x in range(0, w - strip_width + 1, strip_width):
        strips.append(frame[:, x:x + strip_width, :])
    return strips

def find_best_matching_strip_index(template: np.ndarray, strips: list[np.ndarray]) -> int:
    min_mse = float('inf')
    best_index = -1

    for i, strip in enumerate(strips):
        mse = np.mean((strip.astype(np.float32) - template.astype(np.float32)) ** 2)
        if mse < min_mse:
            min_mse = mse
            best_index = i

    return best_index

def get_half_screen_turn() -> TurnCalibrationResult:
    cap = cv2.VideoCapture(0)
    frame_one: Optional[np.ndarray] = None
    frame_two: Optional[np.ndarray] = None
    milliseconds_to_half_turn = None

    initial_pwm = 0.5
    initial_milliseconds_to_drive = 20
    milliseconds_step = 10
    pwm_step = 0.05
    max_duration = 5000 
    current_milliseconds_to_drive = initial_milliseconds_to_drive
    current_pwm = initial_pwm

    while milliseconds_to_half_turn is None:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_one is None:
            frame_one = frame
            drive(dir=Direction.RIGHT, duration_in_milliseconds=current_milliseconds_to_drive, pwm_speed=current_pwm)
        elif frame_two is None:
            frame_two = frame

        if frame_one is not None and frame_two is not None:
            frame_one_middle = get_middle_strip(frame=frame_one)
            strips = split_into_strips(frame=frame_two, strip_width=STRIP_WIDTH)
            middle_index = len(strips) // 2
            best_match_index = find_best_matching_strip_index(template=frame_one_middle, strips=strips)

            target_offset = middle_index // 2
            actual_offset = middle_index - best_match_index

            difference = abs(actual_offset - target_offset)

            if difference <= CLOSE_ENOUGH:
                milliseconds_to_half_turn = current_milliseconds_to_drive
                break
            else:
                if abs(actual_offset) < 3 and current_pwm < 1:
                    current_pwm = min(current_pwm + pwm_step, 1.0)
                    current_milliseconds_to_drive = initial_milliseconds_to_drive
                elif actual_offset < target_offset:
                    current_milliseconds_to_drive += milliseconds_step
                else:
                    current_milliseconds_to_drive = max(current_milliseconds_to_drive - milliseconds_step, milliseconds_step)

                frame_one = None
                frame_two = None

                if current_milliseconds_to_drive >= max_duration:
                    milliseconds_to_half_turn = current_milliseconds_to_drive

        time.sleep(1)

    cap.release()

    return TurnCalibrationResult(
        pwm_speed=current_pwm,
        duration_milliseconds=milliseconds_to_half_turn
    )







        


