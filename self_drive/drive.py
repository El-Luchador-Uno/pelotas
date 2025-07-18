from constants import SL1, SL2, SR1, SR2, PWML, PWMR, Direction
from pin_management import standard_pin
from time import sleep

def drive(dir: Direction, duration_in_milliseconds: int, pwm_speed: float = 0.5):
    MILLISECONDS_PER_SECOND = 1000

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
        pwm_left = pwm_speed
        pwm_right = pwm_speed        
    elif dir == Direction.DOWN:
        left_one = 0
        left_two = 1
        right_one = 0
        right_two = 1
        pwm_left = pwm_speed
        pwm_right = pwm_speed 
    elif dir == Direction.LEFT:
        left_one = 0
        left_two = 1
        right_one = 1
        right_two = 0
        pwm_left = pwm_speed
        pwm_right = pwm_speed
    elif dir == Direction.RIGHT:
        left_one = 1
        left_two = 0
        right_one = 0
        right_two = 1
        pwm_left = pwm_speed
        pwm_right = pwm_speed 

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

    sleep(duration_in_milliseconds / MILLISECONDS_PER_SECOND)

    standard_pin.bulk_adjust_standard_pins(adjustments=[
        {
            'pin': SL1,
            'duty_cycle': 0
        },
        {
            'pin': SL2,
            'duty_cycle': 0
        },
        {
            'pin': SR1,
            'duty_cycle': 0
        },
        {
            'pin': SR2,
            'duty_cycle': 0
        },
        {
            'pin': PWML,
            'duty_cycle': 0
        },
        {
            'pin': PWMR,
            'duty_cycle': 0
        }
    ])
    

