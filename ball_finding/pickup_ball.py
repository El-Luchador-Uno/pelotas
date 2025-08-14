from pin_management import servo_pin
from time import sleep
from constants import INTAKE_SERVO
from constants import Direction
from self_drive.drive import drive

def pickup_ball(drive_milliseconds: int, drive_pwm: float):
    servo_pin.control_servo(INTAKE_SERVO, -0.75)
    sleep(0.5)
    drive(dir=Direction.UP, duration_in_milliseconds=drive_milliseconds, pwm_speed=drive_pwm)
    sleep(2)
    servo_pin.control_servo(INTAKE_SERVO, 0)