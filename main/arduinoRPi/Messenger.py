from config import ARDUINO_PORT

import time
import serial


def send_message(ser, message):
    ser.flush()

    message = str(message) + '\n'
    message = message.encode()
    ser.write(message)


def receive_message(ser):
    message = ser.readline().decode().rstrip()

    return message
