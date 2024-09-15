from cameraRealsense import RealsenseCamera

import cv2 as cv

def main():
    while True:
        frame = realsense_camera.__takePicture()

        video.write(frame)

        if cv.waitKey(1) == ord('q'):
            break

    video.release()


if __name__ == '__main__':
    realsense_camera = RealsenseCamera()

    fourcc = cv.VideoWriter_fourcc(*'XVID')
    video = cv.VideoWriter('output.avi', fourcc, realsense_camera.fps, realsense_camera.frame_shape)

    main()
