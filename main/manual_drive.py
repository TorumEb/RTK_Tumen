import config
import arduinoRPi.Messenger as arduino
from line_following import stop_robot

import sys
import tty
import serial
import termios
from select import select


def get_pressed_key(settings, timeout=0.05):
    tty.setraw(sys.stdin.fileno())

    rlist, _, _ = select([sys.stdin], [], [], timeout)

    key = sys.stdin.read(1) if rlist else ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

    return key


def main():
    while True:
        key_pressed = get_pressed_key(keyboard_settings).lower()

        if key_pressed in key_bindings:
            arduino.send_message(arduino_serial, *key_bindings[key_pressed])

        elif key_pressed == 'q':
            break

if __name__ == '__main__':
    linear_speed = 250
    rotation_speed = 140

    # first left motor, then right
    key_bindings = {
        'w': ( linear_speed,  linear_speed),
        's': (-linear_speed, -linear_speed),
        'a': (-rotation_speed,  rotation_speed),
        'd': ( rotation_speed, -rotation_speed),
        '': (0, 0)
    }

    keyboard_settings = termios.tcgetattr(sys.stdin)

    arduino_serial = serial.Serial(config.ARDUINO_PORT, 115_200, timeout=1)
    arduino_serial.reset_input_buffer()
    arduino_serial.flush()

    try:
        main()
    finally:
        stop_robot(arduino_serial)
