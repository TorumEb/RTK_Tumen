import config
import arduinoRPi.Messenger as arduino
from cameraRuspberry.cameraRPI import Camera_RPI

import sys
import tty
import termios
from select import select
import serial

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

    fourcc = cv.VideoWriter_fourcc(*'XVID')
    video = cv.VideoWriter('output.avi', fourcc, 20.0, (800,  600))

    while True:
        frame = rpi_camera.take_picture()

        video.write(frame)

        key_pressed = get_pressed_key(keyboard_settings).lower()
        if key_pressed in key_bindings:
            arduino.send_message(arduino_serial, *key_bindings[key_pressed])
        elif key_pressed == 'q':
            break

    video.release()


if __name__ == '__main__':
    robot_speed = 200

    # first right motor, then left
    key_bindings = {
        'w': ( robot_speed,  robot_speed),
        'a': ( robot_speed, -robot_speed),
        'd': (-robot_speed,  robot_speed),
        's': (-robot_speed, -robot_speed),
        '': (0, 0)
    }

    main()
