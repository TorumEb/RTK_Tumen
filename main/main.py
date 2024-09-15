import config
from pid_regulator import PID
import arduinoRPi.Messenger as arduino
from cameraRuspberry.cameraRPI import Camera_RPI
from server import sendMessageToClient, GetMessageFromClient

from line_following import turn_side, turn_around
from line_detection import count_error, detect_turn_end, apply_thresh

import serial
import socket

import cv2 as cv


def main():
    while True:
        frame = rpi_camera.take_picture()
        frame = apply_thresh(frame)

        turns = detect_turn_end(frame)
        print(turns)

        if turns == [0, 0]:
            pid_regulator.iteration(frame, serializer)

        elif turns == [0, 1]:
            turn_id = turns.index(1)
            while turns[turn_id] == 1:
                frame = rpi_camera.take_picture()
                frame = apply_thresh(frame)

                window_width = frame.shape[1] // 2
                frame_tmp = frame[:, window_width - 100:window_width + 100]

                pid_regulator.iteration(frame_tmp, serializer)
                turns = detect_turn_end(frame, up_line=570, down_line=600)

            turn_side(turn_id, serializer, speed=180, turning_time=1.6)

        elif turns == [1, 0]:
            arduino.send_message(serializer, 0, 0)

            time.sleep(1_000)

        if any(turns):
            pid_regulator.prev_error = 0

  
if __name__ == '__main__':
    pid_regulator = PID(base_speed=250)

    rpi_camera = Camera_RPI()

    serializer = serial.Serial(config.ARDUINO_PORT, config.ARDUINO_BUND)
    serializer.reset_input_buffer()
    serializer.flush()

    # server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server_socket.bind(config.SERVER_ADDRESS)
    # server_socket.listen(1)
    # print('Server is running')
    # connection, address = server_socket.accept()
    # print(f'New connection from {address}')

    try:
        main()
    finally:
        arduino.send_message(serializer, 0, 0)
