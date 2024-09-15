import config
from pid_regulator import PID
import arduinoRPi.Messenger as arduino
from cameraRuspberry.cameraRPI import Camera_RPI

from line_following import turn_side, turn_around
from line_detection import count_error, detect_turn_end, apply_thresh

import serial

import cv2 as cv


def main():
    while True:
        frame = rpi_camera.take_picture()
        frame = apply_thresh(frame)

        turns = detect_turn_end(frame)
        print(turns)
        if turns == [1, 1]:
            turn_around(rpi_camera, serializer, frame)
            cv.imwrite('fuck.png', frame)
        elif turns == [0, 0]:
            pid_regulator.iteration(frame, serializer)
        else:
            if turns[1]:
                cv.imwrite('right.png', frame)
            else:
                cv.imwrite('fuck.png', frame)

            turn_id = turns.index(1)
            while turns[turn_id] == 1:
                frame = rpi_camera.take_picture()
                frame = apply_thresh(frame)

                window_width = frame.shape[1] // 2
                frame_tmp = frame[:, window_width - 60:window_width + 60 ]

                pid_regulator.iteration(frame_tmp, serializer)
                turns = detect_turn_end(frame)
            turn_side(turn_id, serializer, speed=180, turning_time=1.6)

        if turns == [1, 1] or sum(turns) == 1:
            pid_regulator.prev_error = 0

  
if __name__ == '__main__':
    pid_regulator = PID(base_speed=110)

    rpi_camera = Camera_RPI()

    serializer = serial.Serial(config.ARDUINO_PORT, config.ARDUINO_BUND)
    serializer.reset_input_buffer()
    serializer.flush()

    try:
        main()
    finally:
        arduino.send_message(serializer, 0, 0)
