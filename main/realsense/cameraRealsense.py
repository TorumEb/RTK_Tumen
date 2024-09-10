from typing import List, Tuple, Dict

import cv2 as cv
import numpy as np
import pyrealsense2 as rs
from ultralytics import YOLO


class RealsenseCamera:
    def __init__(self,
            model_detection_path, model_classification_path,
            shape=(1920, 1080), fps=30,
        ) -> None:
        self.model_detection = YOLO(model_detection_path)
        self.model_classification = YOLO(model_classification_path)

        self.__camera = rs.pipeline()
        __rs_config = rs.config()
        __rs_config.enable_stream(rs.stream.any, *shape, rs.format.bgr8, fps)
        self.__camera.start()

        # Green and Red keys correspond to class names for classification model
        # thus shouldn't be changed
        self.colors = {
            'Green': (0, 255, 0),
            'Red': (0, 0, 255),
            'Blue': (255, 0, 0)
        }


    def classify_manometr(self, image, manometr_box):
        # Predicts manometr reading with YOLOv8 model

        manometr = self.__crop_manometr(image, manometr_box)

        predicted_class = self.model_classification.predict(
            manometr, verbose=False)[0]
        class_names = predicted_class.names
        most_probable_class = predicted_class.probs.top1

        manometr_class = class_names[most_probable_class]

        return manometr_class


    def detection_pipeline(self, image, arucos, display=False):
    
        prediction = self.model_detection.predict(image, conf=.75, verbose=False)[0]

        arucos_centers = {
            id: self.__get_aruco_center(corners[0][0], corners[0][2])
            for corners, id in arucos
        }

        manometrs_centers = np.array(self.__get_manometrs_center(prediction))

        aruco2manometr_centers = self.__closest_aruco(manometrs_centers, arucos_centers)

        aruco2manometr_class = dict()
        for aruco_id, man_idx in aruco2manometr_centers.items():
            manometr_box = prediction.boxes.xyxy[man_idx].tolist()
            manometr_class = self.classify_manometr(image, manometr_box)

            aruco2manometr_class[aruco_id] = manometr_class

        if not display:
            return aruco2manometr_class

        image = self.__display_prediction(
            prediction, image,
            aruco2manometr_centers, aruco2manometr_class
        )

        return aruco2manometr_class, image


    @staticmethod
    def find_aruco(image, aruco_type=cv.aruco.DICT_5X5_100):
        # Detects all ArUco markers in image
        # 
        # Input pararms:
        # 	aruco_type (not required) - type of ArUco markers
        # 	debug (default: false) - if True also return corners of markers and taken image
        # 
        # Returns just ids of detected markers if debug is diabled,
        # else image, corners and ids
        dictionary = cv.aruco.getPredefinedDictionary(aruco_type)
        parameters =  cv.aruco.DetectorParameters()
        detector = cv.aruco.ArucoDetector(dictionary, parameters)

        corners, ids, _ = detector.detectMarkers(image)
        if ids is None:
            return []

        ids = ids.flatten().tolist()

        return [*zip(corners, ids)]


    def take_pirture(self):
        frame = self.__camera.wait_for_frames()
        data = frame.get_color_frame()
        data = data.get_data()

        image = np.asanyarray(data)
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

        return image


    def __display_prediction(self, prediction, image, aruco2manometr_centers, aruco2manometr_class):

        for aruco_id, man_idx in aruco2manometr_centers.items():
            man_color = aruco2manometr_class[aruco_id]
            man_color = self.colors[man_color]

            man_box = prediction.boxes.xyxy[man_idx].tolist()
            man_box = [*map(round, man_box)]

            cv.rectangle(
                image, man_box[:2], man_box[2:],
                color=man_color, thickness=3)
            cv.putText(
                image, f'{aruco_id}', (man_box[0], man_box[1] - 10),
                cv.FONT_HERSHEY_SIMPLEX, 0.9, color=self.colors['Blue'], thickness=3)

        return image

    @staticmethod
    def __get_aruco_center(top_left, bottom_right):
        # Diagonal center between top left and bottom right corner of aruco marker

        center_x = int((top_left[0] + bottom_right[0]) / 2.0)
        center_y = int((top_left[1] + bottom_right[1]) / 2.0)

        return [center_x, center_y]

    @staticmethod
    def __get_manometrs_center(prediction):
        # Center of detected manometr from boxes.xywh, where xy is center itself

        centers = prediction.boxes.xywh.tolist()
        centers = [
            [*map(round, center[:2])]
            for center in centers
        ]

        return centers

    @staticmethod
    def __closest_aruco(manometr_centers, arucos):

        # Computes distances between centers of every
        # manometr and aruco marker, then gives closest
        # aruco for every manometr
        #
        # Return:
        #   {aruco_id_1: manometr index in prediction, aruco_id_2: ...}

        if not len(arucos) or not len(manometr_centers):
            return dict()

        aruco_centers = np.array([*arucos.values()])

        distances = np.zeros(
            (manometr_centers.shape[0], aruco_centers.shape[0]))

        for man_i, manometr in enumerate(manometr_centers):
            for ar_i, aruco in enumerate(aruco_centers):
                distances[man_i, ar_i] = np.linalg.norm(manometr - aruco)

        nearest_arucos = np.argmin(distances, axis=1)
        aruco2manometr_map = {
            [*arucos.keys()][ar_i]: man_i
            for man_i, ar_i in enumerate(nearest_arucos)
        }

        return aruco2manometr_map

    @staticmethod
    def __crop_manometr(image, box):
        # Crop manometr from frame based on YOLO detection

        box = [*map(round, box)]
        x1, y1, x2, y2 = box

        return image[y1:y2, x1:x2]
