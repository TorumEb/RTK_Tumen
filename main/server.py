import config

import time

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
    error1, error, ierror, h = 0, 0, 0, 1

    # server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server_socket.bind(config.SERVER_ADDRESS)
    # server_socket.listen(1)
    # print('server is running, please, press ctrl+c to stop')
    # connection, address = server_socket.accept()
    # print("new connection from {address}".format(address=address))
    # camera = Camera_RPI()
    ser = serial.Serial(config.ARDUINO_PORT, 115_200, timeout=1)
    ser.reset_input_buffer()
    ser.flush()

    while True:
        # data = GetMessageFromClient(connection)
        # tic = time.time()

        # error1 = error

        # error = camera.countError()
        # derror = (error - error1) / h
        # ierror += (error1 + error) * (h / 2)

        # w = error + .45 * derror + .4 * ierror

        messanger.send_message(ser, 14, -53)

        # toc = time.time()
        # dtime = h - (toc - tic)
        # if dtime > 0:
        #    time.sleep(dtime)

        time.sleep(0.1)


if __name__ == "__main__":
    main()
