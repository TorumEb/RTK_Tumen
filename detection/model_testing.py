import os

import cv2 as cv
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator


def predict_video_stream(model):
    webcam = cv.VideoCapture(0)

    while True:
        _, frame = webcam.read()

        prediction = model.predict(frame)
        for pred in prediction:
            annotator = Annotator(frame)

            boxes = pred.boxes
            for box in boxes:
                box_coordinates = box.xyxy[0]
                box_conf = box.conf[0].tolist()

                if box_conf <= .5:
                    continue

                annotator.box_label(box_coordinates, str(box_conf), color=(0, 0, 255))

        predicted_frame = annotator.result()

        cv.imshow('Predicted Frame', predicted_frame)
        if cv.waitKey(30) == ord('q'):
            break

    cv.destroyAllWindows()
    webcam.release()


def main():
    base_path = os.getcwd()
    
    model = YOLO(os.path.join(base_path, 'yolov8n_e100.pt'))

    for image_name in os.listdir(os.path.join(base_path, 'test_images')):
        image_path = os.path.join(base_path, 'test_images', image_name)

        prediction = model.predict(image_path)
        prediction[0].save(os.path.join(base_path, 'predictions', image_name))


if __name__ == '__main__':
    main()
        