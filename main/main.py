import config

from pid_regulator import PID
from server import sendMessageToClient
from cameraRuspberry.cameraRPI import Camera_RPI

from line_following import turn_side, stop_robot
from line_detection import detect_turn_end, apply_thresh

import serial
import socket


def main():
    right_turn = 0

    # Sixth right turn indicates last dead end on the track
    while right_turn < 6:
        frame = rpi_camera.take_picture()
        frame = apply_thresh(frame)

        turns = detect_turn_end(frame)

        # Left turn detected, so picture needs to be taken
        if turns[0]:
            # Short stop allowing camera wobble to settle
            stop_robot(serializer, stop_time=0.7)

            # Send singal to take picture
            sendMessageToClient(connection, 'detect')

            # Wait for picure to be taken
            stop_robot(serializer, stop_time=0.)

        # Right turn detected, so turning robot
        if turns[1]:
            right_turn += 1

            # Skips false right turn to mines
            if right_turn == 3: continue

            turn_id = 1
            # Driving forward until camera loses sight of turn
            while turns[turn_id]:
                frame = rpi_camera.take_picture()
                frame = apply_thresh(frame)

                # Crop sides of an image, so PID regulator keeps driving straight
                # ignoring center of mass shift caused by turn
                frame_center = frame.shape[1] // 2
                window_width = 100
                frame_tmp = frame[
                    :, frame_center - window_width:frame_center + window_width
                ]

                pid_regulator.iteration(frame_tmp, serializer)

                # Shifting searching window to the bottom, so robot can stop
                # at the very last moment
                turns = detect_turn_end(frame, up_line=570, down_line=600)

            # Turning robot
            turn_side(turn_id, serializer, speed=250, turning_time=1.3)

        # No turns or dead ends, which means driving forward
        if not any(turns):
            pid_regulator.iteration(frame, serializer)


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
    connection, address = server_socket.accept()
    print(f'New connection from {address}')

    # Stop robot even if unexpected error occurred
    try:
        main()
    finally:
        stop_robot(serializer)
