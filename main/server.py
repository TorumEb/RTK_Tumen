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
import config

def sendMessageToClient(connection, message):
    data = json.dumps({"message": message})
    connection.sendall(data.encode())
    


def getMessageFromClient(connection):
    while True:
        data = connection.recv(4096)
        #data = pickle.load(data)
        data = json.loads(data.decode())
        if data == 404:
            break
        return data
    return None
