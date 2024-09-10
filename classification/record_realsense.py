# https://github.com/IntelRealSense/librealsense/issues/8528

import cv2 as cv
import numpy as np
import pyrealsense2 as rs


RESOLUTION = 1920, 1080
FPS = 30


pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, *RESOLUTION, rs.format.bgr8, FPS)

color_path = 'V00P00A00C00_rgb.avi'
color_writer = cv.VideoWriter(color_path, cv.VideoWriter_fourcc(*'XVID'), FPS, RESOLUTION, 1)

pipeline.start()

try:
    while True:
        frame = pipeline.wait_for_frames()
        color_frame = frame.get_color_frame()

        if not color_frame:
            continue

        color_frame = np.asanyarray(color_frame.get_data())
        color_writer.write(color_frame)

        cv.imshow('Stream', color_frame)
        if cv.waitKey(1) == ord('q'):
            break
finally:
    cv.destroyAllWindows()
    color_writer.release()
    pipeline.stop()
