import cv2 as cv
import numpy as np


def count_error(image, *, up_line=550, down_line=580):
    croped_image = image[:][up_line:down_line]

    mass_center = cv.moments(croped_image, 1)

    if mass_center['m00'] > 1:
        x = int(mass_center['m10'] / mass_center['m00'])

        error = croped_image.shape[1] // 2 - x 

        return error

    return 0


def detect_turn_end(image, *, up_line=400, down_line=540):
    # Returns list of two elements, representing left and right turn respectively

    crop_image_left = image[up_line:down_line, 0:image.shape[1] // 2]
    crop_image_right = image[up_line:down_line, image.shape[1] // 2 : image.shape[1]]

    amount_left = np.sum(crop_image_left) / 255
    amount_right = np.sum(crop_image_right) / 255

    procent_size_image = (down_line - up_line) * (image.shape[1] // 2)
    procent_size_image = procent_size_image * 0.8

    ans = [
        int(amount_left  >= procent_size_image),
        int(amount_right >= procent_size_image)
    ]

    return ans 


def apply_thresh(image, thresh_range=(120, 255)):
    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    _, thresh = cv.threshold(image, *thresh_range, cv.THRESH_BINARY_INV)

    return thresh
