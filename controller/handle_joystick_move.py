from math import atan2, degrees, sqrt
from constants import JOYSTICK_EVENT_MAX, SL1, SL2, SR1, SR2, PWML, PWMR
from enum import Enum
from pin_management import standard_pin

class Direction(Enum):
    LEFT = 'left',
    RIGHT = 'right',
    UP = 'up',
    DOWN = 'down'
    STOP = 'stop'

def get_distance_from_center(x: int, y: int) -> float:
    return sqrt(x**2 + y**2)

def get_degrees_of_direction(x: int, y: int) -> float:
    # Convert angle from radians to degrees and normalize to 0–360
    angle = degrees(atan2(y, x))
    return (angle + 360) % 360

def get_pwm_values(x: int, y: int, max_axis_value: int) -> dict:
    pwm_values = {'right': 0.0, 'left': 0.0}
    deadzone = max_axis_value * 0.03

    if abs(x) < deadzone and abs(y) < deadzone:
        return pwm_values

    distance = get_distance_from_center(x, y)
    direction_deg = get_degrees_of_direction(x, y)
    percent_of_max = distance / max_axis_value

    quadrant = int(direction_deg // 90)
    angle_in_quadrant = direction_deg - (quadrant * 90)

    if angle_in_quadrant > 45:
        angle_in_quadrant = 90 - angle_in_quadrant

    ratio = 1 - (0.5 * angle_in_quadrant / 45)

    if quadrant in [0, 3]:  # Forward left and backward left
        pwm_values['right'] = 1.0
        pwm_values['left'] = percent_of_max * ratio
    elif quadrant in [1, 2]:  # Forward right and backward right
        pwm_values['left'] = 1.0
        pwm_values['right'] = percent_of_max * ratio

    return pwm_values

def handle_move(x: int, y: int, dir: Direction):
    left_one: int
    left_two: int
    right_one: int
    right_two: int
    pwm_left: float
    pwm_right: float

    if dir == Direction.UP:
        left_one = 1
        left_two = 0
        right_one = 1
        right_two = 0
        pwm_values = get_pwm_values(x, y, JOYSTICK_EVENT_MAX)
    elif dir == Direction.DOWN:
        left_one = 0
        left_two = 1
        right_one = 0
        right_two = 1
    elif dir == Direction.LEFT:
        left_one = 1
        left_two = 0
        right_one = 0
        right_two = 1
    elif dir == Direction.RIGHT:
        left_one = 0
        left_two = 1
        right_one = 1
        right_two = 0
    elif dir == Direction.STOP:
        left_one = 0
        left_two = 0
        right_one = 0
        right_two = 0
    
    pwm_values = get_pwm_values(x, y, JOYSTICK_EVENT_MAX)
    print(f"values {pwm_values}")

    # For now scaling back max pwm values to half speed slow bot down
    pwm_left = pwm_values['left'] * 0.5
    pwm_right = pwm_values['right'] * 0.5

    adjustments = [
        {
            'pin': SL1,
            'duty_cycle': left_one
        },
        {
            'pin': SL2,
            'duty_cycle': left_two
        },
        {
            'pin': SR1,
            'duty_cycle': right_one
        },
        {
            'pin': SR2,
            'duty_cycle': right_two
        },
        {
            'pin': PWML,
            'duty_cycle': pwm_left
        },
        {
            'pin': PWMR,
            'duty_cycle': pwm_right
        }
    ]

    standard_pin.bulk_adjust_standard_pins(adjustments=adjustments)

