import os

import cv2 as cv
from ultralytics import YOLO


def main():
    base_path = os.getcwd()
    dataset_path = os.path.join('..', 'detection', 'selected_frames')
    new_dataset = os.path.join(base_path, 'from_detection')

    model = YOLO('../detection/yolov8n_e100.pt')

    for image_name in os.listdir(dataset_path):
        image_path = os.path.join(dataset_path, image_name)
        image = cv.imread(image_path)

        prediction = model.predict(image, conf=.75, verbose=False)[0]
        for i, box in enumerate(prediction.boxes.xyxy):
            box = [*map(int, box.tolist())]
            x1, y1, x2, y2 = box

            manometr_i = image[y1:y2, x1:x2]
            new_image = os.path.join(new_dataset, f'{i}_{image_name}')

            cv.imwrite(new_image, manometr_i)


if __name__ == '__main__':
    main()
