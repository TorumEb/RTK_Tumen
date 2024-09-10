import cv2 as cv
import numpy as np


def detect_markers(image, aruco_type=cv.aruco.DICT_5X5_100):
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

    return corners, ids


def draw_coordinates(
        image, corners, marker_length=0.7,
        camera_intrinsic=None, camera_distortion=None):

    camera_intrinsic = np.array([
        [933.15867, 0, 657.59],
        [0, 933.1586, 400.36993], 
        [0, 0, 1]
    ]) if camera_intrinsic is None else camera_intrinsic

    camera_distortion = np.array([
        -0.43948, 0.18514, 0, 0
    ]) if camera_distortion is None else camera_distortion

    coordinate_vectors = np.array([
        [-marker_length / 2,  marker_length / 2, 0],
        [ marker_length / 2,  marker_length / 2, 0],
        [ marker_length / 2, -marker_length / 2, 0],
        [-marker_length / 2, -marker_length / 2, 0]
    ])
    coordinate_vectors = np.expand_dims(coordinate_vectors, 1)

    for i in range(corners.shape[0]):
        _, rvec, tvec = cv.solvePnP(
            coordinate_vectors, corners[i],
            camera_intrinsic, camera_distortion
        )

        image = cv.drawFrameAxes(
            image, camera_intrinsic, camera_distortion,
            rvec, tvec,
            marker_length * 1.5, 2
        )

    return image


def main():
    ...


if __name__ == '__main__':
    main()