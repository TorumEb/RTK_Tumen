from config import ARDUINO_PORT

import time
import serial


def send_message(message):
    ser = serial.Serial(ARDUINO_PORT, 9600, timeout=1)
    ser.flush()

    ser.write(f'{message}\n')

    ser.end()


def receive_message():
    ser = serial.Serial(ARDUINO_PORT, 9600, timeout=1)

    message = ser.readline().decode('utf-8').rstrip()

    ser.end()

    return message
