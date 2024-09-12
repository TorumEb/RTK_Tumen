
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


	# def __take_picture(self, stream='main'):
	# 	open camera
	# 	cap = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)

	# 	set dimensions
	# 	cap.set(cv2.CAP_PROP_FRAME_WIDTH, 600)
	# 	cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)

	# 	take frame
	# 	ret, frame = cap.read()
	# 	write frame to file
		

	# 	return frame

	def __take_picture(self, stream='main'):
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



	def countError(self):
		img = self.__take_picture() 

		cv2.imwrite('img.png', img)

		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		up_line = 200
		down_line = 220
		croped_gray = gray[:][up_line:down_line]
		_, thresh = cv2.threshold(croped_gray, 140, 255, cv2.THRESH_BINARY_INV)

		cv2.imwrite('thresh.png', thresh)

		C = cv2.moments(thresh,1)
		if C['m00'] > 1:
			x = int(C['m10'] / C['m00'])
			y = int(C['m01']/ C['m00'])
			cv2.circle(croped_gray, (x, y), 10, (255,255,255), -1)
			error = croped_gray.shape[1] // 2 - x 
			return error

		return 0
