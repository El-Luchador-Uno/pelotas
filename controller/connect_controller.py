from evdev import InputDevice, ecodes, list_devices
from pin_management import manage_servo


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
    
    A_BUTTON_CODE = 305
    B_BUTTON_CODE = 304
    Y_BUTTON_CODE = 308
    
    for event in controller.read_loop():
        if event.type == ecodes.EV_KEY or event.type == ecodes.EV_ABS:
            if event.code == A_BUTTON_CODE and event.value == 1:
                manage_servo.control_servo(17, True)
            elif event.code == B_BUTTON_CODE and event.value == 1:
                manage_servo.control_servo(17, False)
            elif event.code == Y_BUTTON_CODE and event.value == 1:
                exit(0)