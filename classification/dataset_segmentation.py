import os

import cv2 as cv
import splitfolders


TRAIN_SPLIT = 0.8
TEST_SPLIT = 0.1
VAL_SPLIT = 0.1


def get_class_from_user(image):
    user_input = None
    while user_input not in ['g', 'r']:
        cv.imshow('Image', image)
        cv.waitKey(100)

        user_input = input()

    cv.destroyWindow('Image')

    if user_input == 'g':
        return 'green'
    return 'red'


def dataset_augmentation(dataset_path, images_path):
    for image_path in images_path:
        image_name = image_path.split('/')[-1]
        image = cv.imread(image_path)

        image_class = get_class_from_user(image)
        cv.imwrite(
            os.path.join(dataset_path, image_class, image_name),
            image
        )


def create_dataset_structure(dataset_path, seed=1337):
    splitfolders.ratio(
        dataset_path,
        output='dataset_splited',
        ratio=(TRAIN_SPLIT, VAL_SPLIT, TEST_SPLIT),
        seed=seed
    )


def main():
    base_path = os.getcwd()
    dataset_path = os.path.join(base_path, 'dataset_segmented')

    images_path = os.listdir(dataset_path)
    images_path = [
        os.path.join(dataset_path, im_name)
        for im_name in images_path
    ]

    create_dataset_structure(
        os.path.join(base_path, dataset_path)
    )


if __name__ == '__main__':
    main()
