import config
from server import getMessageFromClient
from realsense.realsense_detection import Realsense, ManometrDetector

import json
import socket


def main():
    while True:
        data = getMessageFromClient(client)

        if data == {'message': 'detect'}:
            frame = realsense.take_pirture()

            arucos = manometr_detector.find_aruco(frame)

            aruco2manometr = manometr_detector.detection_pipeline(frame, arucos)

            print(json.dumps(aruco2manometr, indent=3, sort_keys=True), end='\n\n')


if __name__== "__main__":
    print('Initializing models...', end=' ')
    model_detection_path = 'realsense/yolov8n_e100.pt'
    model_classification_path = 'realsense/yolov8n_cls_v4_e100.pt'

    manometr_detector = ManometrDetector(
        model_detection_path, model_detection_path
    )

    manometr_detector.initialize_detection()
    print('Done')

    print('Connecting realsense...', end=' ')
    realsense = Realsense()
    print('Done')

    print('Connecting to server...', end=' ')
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(config.SERVER_ADDRESS)
    print('Done', end='\n\n')

    main()
