
import cv2
import numpy as np
from picamera2 import Picamera2


class Camera_RPI:
	def __init__(self, camera_config=None):
		self.camera = Picamera2()

		if camera_config is None:
			camera_config = {'format': 'XRGB8888', 'size': (800, 600)}
		camera_config = self.camera.create_preview_configuration(camera_config)
		self.camera.configure(camera_config)

		self.camera.start()


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
