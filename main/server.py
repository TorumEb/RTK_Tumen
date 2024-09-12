import config

import time
from math import copysign

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
    START_SPEED = 150
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
    try:
        while True:
                #data = GetMessageFromClient(connection)
                tic = time.time()

                error1 = error

                error = camera.countError()
                if -10 < error < 10:
                    error = copysign(10, error)
                print(error)

                derror = (error - error1) / h
                ierror += (error1 + error) * (h / 2)

                w = 0.1 * error + 0.01 * derror + 0 * ierror
                left_motor = max(0, min(START_SPEED + w, 220))
                right_motor = max(0, min(START_SPEED - w, 220))

                #messanger.send_message(ser, int(right_motor), int(left_motor))
                messanger.send_message(ser, 255, -255)

                toc = time.time()
                dtime = h - (toc - tic)
                if dtime > 0:
                   time.sleep(dtime)
    except KeyboardInterrupt:
        messanger.send_message(ser, 0, 0)


if __name__ == "__main__":
    main()
