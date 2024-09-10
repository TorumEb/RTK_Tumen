import pyrealsense2 as rs
import numpy as np
import realsense.configAruco as configAruco
import cv2 as cv
import time 


class RealsenseCamera: 
    def __init__(self):
        self.camera = rs.pipeline()
        self.cfg = rs.config()
        self.cfg.enable_stream(rs.stream.any, 1920, 1080, rs.format.bgr8, 30)
        self.camera.start()

    def  __takePicture(self):
        frame = self.camera.wait_for_frames()
        data = frame.get_color_frame()
        data = data.get_data()
        np_data = np.asanyarray(data)
        
        return np_data

    def detectAruco(self, aruco_type = None):
        if aruco_type is None: 
            aruco_type = configAruco.aruco_type
        
        image = self.__takePicture()
        
        dictionary = cv.aruco.getPredefinedDictionary(aruco_type)
        parameters =  cv.aruco.DetectorParameters()
        detector = cv.aruco.ArucoDetector(dictionary, parameters)
        corners, ids, rejectedCandidates = detector.detectMarkers(image)

        if ids is None:
            return [] 
        
        ids = ids.flatten().tolist()

        return [*zip(corners, ids)]
