from gpiozero import PWMOutputDevice

pin_objects = {}

def control_pin(pin_number: int, duty_cycle: float):
    if pin_number not in pin_objects:
        pin_objects[pin_number] = PWMOutputDevice(pin_number)

    pin = pin_objects[pin_number]
    pin.value = duty_cycle

def bulk_adjust_standard_pins(adjustments):
    for adjustment in adjustments:
        control_pin(adjustment['pin'], adjustment['duty_cycle'])
