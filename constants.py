from enum import Enum

A_BUTTON_CODE = 305
B_BUTTON_CODE = 304
Y_BUTTON_CODE = 308
X_BUTTON_CODE = 307

JOYSTICK_EVENT_MAX = 32767

SL1 = 6
SL2 = 26
PWML = 13

SR1 = 25
SR2 = 16
PWMR = 12

INTAKE_SERVO = 27

class Direction(Enum):
    LEFT = 'left',
    RIGHT = 'right',
    UP = 'up',
    DOWN = 'down'
    STOP = 'stop'