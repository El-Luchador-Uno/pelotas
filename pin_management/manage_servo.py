from gpiozero import Servo

servo_objects = {}

def control_servo(pin: int, state: bool):
    if pin not in servo_objects:
        servo_objects[pin] = Servo(pin)
    
    servo = servo_objects[pin]

    if state:
        print("on")
        servo.value = -1
    else:
        print("off")
        servo.detach()