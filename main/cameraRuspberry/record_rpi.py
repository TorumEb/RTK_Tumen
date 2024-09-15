from cameraRPI import Camera_RPI

import cv2 as cv


def main():
    while True:
        frame = rpi_camera.take_picture()

        video.write(frame)

        if cv.waitKey(30) == ord('q'):
            break


if __name__ == '__main__':
    rpi_camera = Camera_RPI()

    fourcc = cv.VideoWriter_fourcc(*'XVID')
    video = cv.VideoWriter('output.avi', fourcc, 20., (800, 600))

    main()
    video.release()
