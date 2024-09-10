import socket, pickle
from realsense.cameraRealsense import RealsenseCamera
import json, codecs
import numpy as np

MAX_CONNECTIONS = 1
MODEL_DETECTION_PATH = 'realsense/yolov8n_e100.pt'
MODEL_CLASSIFICATION_PATH = 'realsense/yolov8n_cls_v4_e100.pt'

def sendMessageToServer(client, message):
    data = json.dumps(message)
    client.sendall(data.encode())

def getMessageFromClient():
    return 0


def main(adress = ('192.168.2.113', 8686)):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    
    client.connect(adress)
    realsense = RealsenseCamera(MODEL_DETECTION_PATH, MODEL_CLASSIFICATION_PATH)
    while True:
        frame = realsense.take_pirture()

        arucos = realsense.find_aruco(frame)

        aruco2manometr_class, frame = realsense.detection_pipeline(
            frame, arucos,
            display=True
        )
        sendMessageToServer(client, aruco2manometr_class)
        print(aruco2manometr_class)
        

if __name__== "__main__":
    main()

    








