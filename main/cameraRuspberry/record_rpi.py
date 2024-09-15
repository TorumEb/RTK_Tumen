from cameraRPI import Camera_RPI

import cv2 as cv


def main():
    ...


if __name__ == '__main__':
    rpi_camera = Camera_RPI()

    fourcc = cv.VideoWriter_fourcc(*'XVID')
    video = cv.VideoWriter('output.avi', fourcc, 20., (800, 600))

    main()
