import os

from ultralytics import YOLO


def main():
    base_path = os.getcwd()
    dataset_path = os.path.join(base_path, 'test_images')
    
    model = YOLO(os.path.join(base_path, 'yolov8n_e50_b9.pt'))

    test_images = os.listdir(dataset_path)
    test_images = [
        os.path.join(dataset_path, im)
        for im in test_images
    ]

    prediction = model(test_images)
    for i, pred in enumerate(prediction):
        pred.save(os.path.join(base_path, 'predictions', f'{i}.jpg'))


if __name__ == '__main__':
    main()
