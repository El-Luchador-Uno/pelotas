from constants import SL1, SL2, SR1, SR2, PWML, PWMR, Direction
from pin_management import standard_pin
from time import sleep

def drive(dir: Direction, duration_in_milliseconds: int):
    ON_PWM_VALUE = 0.5 # Arbitrary but don't want to go to fast
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
        pwm_left = ON_PWM_VALUE
        pwm_right = ON_PWM_VALUE        
    elif dir == Direction.DOWN:
        left_one = 0
        left_two = 1
        right_one = 0
        right_two = 1
        pwm_left = ON_PWM_VALUE
        pwm_right = ON_PWM_VALUE 
    elif dir == Direction.LEFT:
        left_one = 0
        left_two = 1
        right_one = 1
        right_two = 0
        pwm_left = ON_PWM_VALUE
        pwm_right = 0.0
    elif dir == Direction.RIGHT:
        left_one = 1
        left_two = 0
        right_one = 0
        right_two = 1
        pwm_left = 0.0
        pwm_right = ON_PWM_VALUE 

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
    

