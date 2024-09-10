import cv2 as cv
import numpy as np
import pyrealsense2 as rs


class RealsenseCamera: 
    def __init__(self, shape=(1920, 1080), fps=30):
        self.camera = rs.pipeline()
        self.cfg = rs.config()
        self.cfg.enable_stream(rs.stream.any, *shape, rs.format.bgr8, fps)
        self.camera.start()

    def __takePicture(self):
        frame = self.camera.wait_for_frames()
        data = frame.get_color_frame()
        data = data.get_data()
        np_data = np.asanyarray(data)
        
        return np_data

    def detect_markers(self, aruco_type=cv.aruco.DICT_5X5_100):
        # Detects all ArUco markers in image
        # 
        # Input pararms:
        # 	aruco_type (not required) - type of ArUco markers
        # 	debug (default: false) - if True also return corners of markers and taken image
        # 
        # Returns just ids of detected markers if debug is diabled,
        # else image, corners and ids
        image = self.__takePicture()

        dictionary = cv.aruco.getPredefinedDictionary(aruco_type)
        parameters =  cv.aruco.DetectorParameters()
        detector = cv.aruco.ArucoDetector(dictionary, parameters)

        corners, ids, _ = detector.detectMarkers(image)
        if ids is None:
            return []

        ids = ids.flatten().tolist()

        return [*zip(corners, ids)]
