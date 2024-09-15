import cv2
import cameraRuspberry.cameraRPI as camera
import numpy as np

camera = camera.Camera_RPI()
img = np.array(camera.camera.capture_array("main"))[:, :, :3]

image = cv2.imwrite('test_image.png', img)

# image = cv.imread('test_image.png')
# print(camera.detect_turn_end(image))
