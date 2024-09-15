import config

import time
from math import copysign
import cv2
import socket, pickle
import json
import numpy as np
from cameraRuspberry.cameraRPI import Camera_RPI
import arduinoRPi.Messenger as messanger
import serial


def sendMessageToClient(connection, message):
    message = message.tolist()
    data = json.dumps({"message": message})
    connection.sendall(data.encode())
    return 0


def GetMessageFromClient(connection):
    while True:
        data = connection.recv(4096)
        #data = pickle.load(data)
        data = json.loads(data.decode())
        if data == 404:
            break
        return data
    return None


def main():
    error1, error, ierror, h = 0, 0, 0, 0.05
    START_SPEED = 170
    left_motor = 0
    right_motor = 0   
    # server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server_socket.bind(config.SERVER_ADDRESS)
    # server_socket.listen(1)
    # print('server is running, please, press ctrl+c to stop')
    # connection, address = server_socket.accept()
    # print("new connection from {address}".format(address=address))
    camera = Camera_RPI()
    ser = serial.Serial(config.ARDUINO_PORT, 115_200, timeout=1)
    ser.reset_input_buffer()
    ser.flush()
    
    #turn_around(camera, ser)

    try:
        while True:
            frame = PID(camera, ser, error1, error, ierror, h, START_SPEED, left_motor, right_motor)
            detect = camera.detect_turn_end(frame)
            if detect[0] == 1:
                while detect[0] == 1:
                    detect = camera.detect_turn_end(frame)
                    frame = PID(camera, ser, error1, error, ierror, h, START_SPEED, left_motor, right_motor)
                    
                turn_side(1, camera, ser, START_SPEED)
    except KeyboardInterrupt:
        messanger.send_message(ser, 0, 0)


def PID(camera, ser, error1, error, ierror, h, START_SPEED, left_motor, right_motor):
    #data = GetMessageFromClient(connection)
    tic = time.time()

    error1 = error

    frame = camera.take_picture()
    error = camera.countError(frame)

    derror = (error - error1) / h
    ierror += (error1 + error) * (h / 2)

    w = 0.3 * error + 0.025 * derror + 0 * ierror
    left_motor = max(0, min(START_SPEED + w, 220))
    right_motor = max(0, min(START_SPEED - w, 220))

    messanger.send_message(ser, int(right_motor), int(left_motor))

    toc = time.time()
    dtime = h - (toc - tic)
    if dtime > 0:
        time.sleep(dtime)

    return frame


def turn_side(side, camera, ser, START_SPEED):
    tic = time.time()
    toc = time.time()
    while toc - tic != 3:
        messanger.send_message(ser, side * START_SPEED, (1 - side) * START_SPEED)
        time.slee(0.05)


# def turn_side(side, camera, ser, START_SPEED):
#     # 1 - left
#     frame = camera.take_picture()
#     frame = frame[400:800, 0 : 100]
#     _, frame = cv2.threshold(frame, *camera.thresh_range, cv2.THRESH_BINARY_INV)
#     sum_white = np.sum(frame) // 255
#     print(sum_white)
#     while(sum_white < 300):
    
#         messanger.send_message(ser, START_SPEED, -1)
#         time.sleep(0.05)


def turn_around(camera, ser):
    frame = camera.take_picture()
    frame = frame[:, 100:frame.shape[1] - 100]
    error = camera.countError(frame)

    start_sign = np.sign(error)
    
    while np.sign(error) == start_sign or error == 0 : 
        if start_sign == 0: start_sign += 1
        messanger.send_message(ser, start_sign * 180 * -1, start_sign * 180)

        frame = camera.take_picture()
        frame = frame[:, 100 : frame.shape[1] - 100]
        error = camera.countError(frame)
        print("turn", error )
        time.sleep(0.05)


if __name__ == "__main__":
    main()
