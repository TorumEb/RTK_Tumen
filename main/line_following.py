import arduinoRPi.Messenger as arduino

import time


def turn_side(side, serializer, *, speed, turning_time, sleep_time=0.05):
    tic = time.time()
    toc = time.time()
    while toc - tic < turning_time:
        toc = time.time()
        arduino.send_message(serializer, side * speed, (1 - side) * speed)

        time.sleep(sleep_time)


def stop_robot(serializer, stop_time=-1, *, sleep_time=0.05):
    stop_start = time.time()
    stop_curr = time.time()
    while stop_curr - stop_start < stop_time:
        stop_curr = time.time()

        arduino.send_message(serializer, 0, 0)

        time.sleep(sleep_time)
