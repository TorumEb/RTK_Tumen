import config
import arduinoRPi.Messenger as arduino
from cameraRuspberry.cameraRPI import Camera_RPI

import sys
import tty
import termios
from select import select
import serial
import time

import cv2 as cv


def get_pressed_key(settings, timeout=0.05):
    tty.setraw(sys.stdin.fileno())

    rlist, _, _ = select([sys.stdin], [], [], timeout)

    key = sys.stdin.read(1) if rlist else ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

    return key


def main():
    keyboard_settings = termios.tcgetattr(sys.stdin)

    rpi_camera = Camera_RPI()

    arduino_serial = serial.Serial(config.ARDUINO_PORT, 115_200, timeout=1)
    arduino_serial.reset_input_buffer()
    arduino_serial.flush()


    while True:
        frame = rpi_camera.take_picture()

        video.write(frame)

        key_pressed = get_pressed_key(keyboard_settings).lower()
        if key_pressed in key_bindings:
            arduino.send_message(arduino_serial, *key_bindings[key_pressed])
        elif key_pressed == 'q':
            break

    arduino.send_message(arduino_serial, 0, 0)
    video.release()


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

    main()
