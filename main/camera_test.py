import cv2 as cv
import cameraRuspberry.cameraRPI as camera
import numpy as np

camera = camera.Camera_RPI()
img = camera.take_picture()
image = cv.imwrite('test_image.png', img)

# image = cv.imread('test_image.png')
# print(camera.detect_turn_end(image))
