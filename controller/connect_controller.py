from evdev import InputDevice, ecodes, list_devices
from pin_management import servo_pin
from constants import A_BUTTON_CODE, B_BUTTON_CODE, Y_BUTTON_CODE, INTAKE_SERVO, X_BUTTON_CODE, Direction
from controller.handle_joystick_move import handle_move, get_degrees_of_direction
from ball_finding.find_ball import find_ball

def connect_controller():
    devices = [InputDevice(fn) for fn in list_devices()]
    controller = None

    for device in devices:
        if device.name == 'Nintendo Switch Pro Controller':
            controller = device
            print(f"Connected to: {device}")
            break

    if not controller:
        print("Controller not found")
        exit(1)

    x = 0
    y = 0

    DIRECTION = Direction.STOP
    
    for event in controller.read_loop():
        if event.type == ecodes.EV_KEY or event.type == ecodes.EV_ABS:
            if event.code == A_BUTTON_CODE and event.value == 1:
                servo_pin.control_servo(INTAKE_SERVO, -1)
            elif event.code == B_BUTTON_CODE and event.value == 1:
                find_ball()
                # servo_pin.control_servo(INTAKE_SERVO, 0)
            elif event.code == X_BUTTON_CODE and event.value == 1:
                servo_pin.control_servo(INTAKE_SERVO, 1)
            elif event.code == Y_BUTTON_CODE and event.value == 1:
                exit(0)
            
            if event.code == ecodes.ABS_X:
                x = event.value
                    
            elif event.code == ecodes.ABS_Y:
                y = event.value

            angle = get_degrees_of_direction(x, y)

            if (angle >= 315 or angle < 45):
                DIRECTION = Direction.RIGHT
            # Down: 45° to 135°
            elif 45 <= angle < 135:
                DIRECTION = Direction.UP
            # Right: 135° to 225°
            elif 135 <= angle < 225:
                DIRECTION = Direction.LEFT
            # Up: 225° to 315°
            elif 225 <= angle < 315:
                DIRECTION = Direction.DOWN
            else:
                DIRECTION = Direction.STOP

            handle_move(x=x, y=y, dir=DIRECTION)


        print(f"x: {x} and y: {y}, direction: {DIRECTION}")
