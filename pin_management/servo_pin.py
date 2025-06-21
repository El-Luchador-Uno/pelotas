from gpiozero import Servo

servo_objects = {}

def control_servo(pin: int, value: float):
    if pin not in servo_objects:
        servo_objects[pin] = Servo(pin)
    
    servo = servo_objects[pin]

    if value == 0:
        servo.detach()
        return

    servo.value = value