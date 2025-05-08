from evdev import InputDevice, categorize, ecodes, list_devices


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
    
    for event in controller.read_loop():
        if event.type == ecodes.EV_KEY or event.type == ecodes.EV_ABS:
            print(categorize(event))