import arduinoRPi.Messenger as arduino
from line_detection import count_error, apply_thresh

import time

import numpy as np


def turn_side(side, serializer, *, speed, turning_time, sleep_time=0.05):
    tic = time.time()
    toc = time.time()
    while toc - tic < turning_time:
        toc = time.time()
        arduino.send_message(serializer, side * speed, (1 - side) * speed)

        time.sleep(sleep_time)


def turn_around(camera, serializer, frame, sleep_time=0.05):
    frame_width = 100
    rotation_speed = 180

    error = count_error(frame)

    start_sign = np.sign(error)
    start_sign = 1 if not start_sign else start_sign

    while np.sign(error) == start_sign or error == 0:
        arduino.send_message(serializer,
            start_sign * rotation_speed * -1,
            start_sign * rotation_speed)

        frame = camera.take_picture()
        frame = frame[:, frame_width:frame.shape[1] - frame_width]

        error = count_error(apply_thresh(frame))

        time.sleep(sleep_time)
