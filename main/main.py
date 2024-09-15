import config
from pid_regulator import PID
import arduinoRPi.Messenger as arduino
from cameraRuspberry.cameraRPI import Camera_RPI
from server import sendMessageToClient, getMessageFromClient

from line_following import turn_side, turn_around
from line_detection import count_error, detect_turn_end, apply_thresh

import serial
import socket
import config

import cv2 as cv
import time

def main():
    right_turns = 0

    while True:
        
        frame = rpi_camera.take_picture()
        frame = apply_thresh(frame)

        turns = detect_turn_end(frame)
        # if sum(turns):
        #     print(turns)
        #     print(right_turns)

        if turns == [0, 0]:
            pid_regulator.iteration(frame, serializer)

        if turns == [1, 1]:
            if right_turns == 4:
                while True:
                    arduino.send_message(serializer, 0, 0)

                return

        if turns[0] == 1:
            print(turns)
            print(right_turns)
            arduino.send_message(serializer, 0, 0)
            #здесь сообщение для джетсона о запуске функци
            time.sleep(2)

        if turns[1] == 1:
            
            right_turns += 1
            print(turns)
            print(right_turns)
 
            turn_id = 1
            while turns[turn_id] == 1:
                frame = rpi_camera.take_picture()
                frame = apply_thresh(frame)

                window_width = frame.shape[1] // 2
                frame_tmp = frame[:, window_width - 100:window_width + 100]

                pid_regulator.iteration(frame_tmp, serializer)
                turns = detect_turn_end(frame, up_line=570, down_line=600)

            turn_side(turn_id, serializer, speed=180, turning_time=2.5)

            if right_turns == 2:
                tic = time.time()
                toc = time.time()
                while toc - tic != 1.5:
                    frame = rpi_camera.take_picture()
                    frame = apply_thresh(frame)

                    

                    pid_regulator.iteration(frame, serializer)
                    turns = detect_turn_end(frame, up_line=570, down_line=600)


        # if any(turns):
        #     pid_regulator.prev_error = 0


if __name__ == '__main__':
    pid_regulator = PID(base_speed=250)

    rpi_camera = Camera_RPI()

    serializer = serial.Serial(config.ARDUINO_PORT, config.ARDUINO_BUND)
    serializer.reset_input_buffer()
    serializer.flush()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(config.SERVER_ADDRESS)
    server_socket.listen(1)
    print('Server is running')
    #connection, address = server_socket.accept()
    #print(f'New connection from {address}')

    try:
        main()
    finally:
        arduino.send_message(serializer, 0, 0)
