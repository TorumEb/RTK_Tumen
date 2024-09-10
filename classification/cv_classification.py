import cv2 as cv


def sift_test(image):
    sift = cv.SIFT().create()

    key_points = sift.detect(image, None)

    image = cv.drawKeypoints(
        image, key_points, image,
        flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    return image


def orb_test(image):
    orb = cv.ORB().create()

    key_points = orb.detect(image, None)

    key_points, description = orb.compute(image, key_points)

    image = cv.drawKeypoints(
        image, key_points, image,
        color=(255, 0, 0), flags=0
    )

    return image


def main():
    image_path = 'dataset_reshaped/IMG_20240902_173059.jpg'
    image = cv.imread(image_path)

    image = orb_test(image)

    cv.imshow('Image', image)
    cv.waitKey(-1)
    cv.destroyWindow('Image')


if __name__ == '__main__':
    main()
