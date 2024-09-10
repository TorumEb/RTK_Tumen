import serial
import time 
if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)
    ser.flush()
    while True:
        ser.write('Hello\n')
        time.sleep(1)