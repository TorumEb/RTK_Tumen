
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

		self.thresh_range = 100, 255
	

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

		cv2.imwrite('test_thresh.png', self.__apply_thresh(gray))
		#cv2.imwrite('test_adaptive_thresh.png', self.adaptive_thresh(gray))

		up_line, down_line = 200, 220
		croped_gray = gray[:][up_line:down_line]

		thresh = self.__apply_thresh(croped_gray)
		C = cv2.moments(thresh, 1)

		if C['m00'] > 1:
			x = int(C['m10'] / C['m00'])

			error = croped_gray.shape[1] // 2 - x 

			return error

		return 0


	def detect_turn_end(self, image):
		up_line, down_line = 520, 600

		crop_image_left = image[up_line:down_line, 0:image.shape[1] // 2]
		crop_image_right = image[up_line:down_line, image.shape[1] // 2 : image.shape[1]]
		
		crop_image_left = cv2.cvtColor(crop_image_left, cv2.COLOR_BGR2GRAY)
		crop_image_right = cv2.cvtColor(crop_image_right, cv2.COLOR_BGR2GRAY)
		
		crop_image_left_thresh = self.__apply_thresh(crop_image_left)
		crop_image_right_thresh = self.__apply_thresh(crop_image_right)
		
		C_left = np.sum(crop_image_left_thresh) / 255
		C_right = np.sum(crop_image_right_thresh) / 255
		
		ans = [0, 0]
		cv2.imwrite("right.png",crop_image_right_thresh)
		cv2.imwrite("left.png",crop_image_left_thresh)
		
		procent_size_image = (down_line - up_line) * (image.shape[1] // 2)
		procent_size_image = procent_size_image * 0.85
		
		
		if C_left >= procent_size_image:
			ans[0] = 1
		if C_right >= procent_size_image:
			ans[1] = 1
		print(ans)
		return ans 


	def __apply_thresh(self, image):
		_, thresh = cv2.threshold(image, *self.thresh_range, cv2.THRESH_BINARY_INV)

		return thresh
