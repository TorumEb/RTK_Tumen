from config import ARDUINO_PORT

import struct
import time
import serial


def send_message(ser, val1, val2):
    data = struct.pack("<hh", val1, val2) + b'\n'

    ser.write(data)


def receive_message(ser):
    message = ser.readline().decode().rstrip()

    return message
