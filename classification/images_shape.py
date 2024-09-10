import os
from PIL import Image


def main():
    base_path = os.getcwd()
    dataset_path = os.path.join(base_path, 'test_images')
    reshaped_path = os.path.join(base_path, 'test_images')

    images_names = os.listdir(dataset_path)
    default_shape = 640, 640
    for image_name in images_names:
        image_path = os.path.join(dataset_path, image_name)
        image = Image.open(image_path)
        
        image_reshaped = image.resize(default_shape, Image.LANCZOS)
        image_reshaped.save(os.path.join(reshaped_path, image_name))


if __name__ == '__main__':
    main()
