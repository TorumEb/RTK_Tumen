
import cv2
import numpy as np
from picamera2 import Picamera2

#from picamera2 import Picamera2 # type: ignore


class Camera_RPI:
	def __init__(self, camera_config=None):
		self.camera = Picamera2()

		if camera_config is None:
			camera_config = {'format': 'XRGB8888', 'size': (800, 600)}
		camera_config = self.camera.create_preview_configuration(camera_config)
		self.camera.configure(camera_config)

		self.camera.start()

		self.thresh_range = 70, 255
	

	def take_picture(self, stream='main'):
		# Takes picture of specified stream
		# 
		# Input arguments:
		# 	stream (default 'main') - stream to take picture from, also lores available.
		# Can be changed with suited config provided in init
		# 
		# Returns BGR (with default config) image of np.array

		image = self.camera.capture_array(stream)
		image = np.array(image)
		image = image[:, :, :3]

		return image


	def countError(self, image):
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

		up_line, down_line = 400, 420
		croped_gray = gray[:][up_line:down_line]

		thresh = self.__apply_thresh(croped_gray)

		C = cv2.moments(thresh, 1)
		if C['m00'] > 1:
			x = int(C['m10'] / C['m00'])

			error = croped_gray.shape[1] // 2 - x 

			return error

		return 0


	def detect_dead_end(self, image):
		side_width = 30
		left_side = image[:, 0:side_width]
		right_side = image[:, image.shape[1] - side_width:image.shape[1]]

		left_side = self.__apply_thresh(left_side)
		right_side = self.__apply_thresh(right_side)

		if np.any(left_side) and np.any(right_side):
			return True
		return False


	def __apply_thresh(self, image):
		_, thresh = cv2.threshold(image, *self.thresh_range, cv2.THRESH_BINARY_INV)

		return thresh
