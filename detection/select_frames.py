import os
import shutil


def main():
    base_path = os.getcwd()
    dataset_path = os.path.join(base_path, 'realsense_dataset')

    desired_amount = 40

    images_list = os.listdir(dataset_path)
    total_amount = len(images_list)

    for frame_i in range(0, total_amount, total_amount // desired_amount):
        frame = images_list[frame_i]

        shutil.copy(
            os.path.join(dataset_path, frame),
            os.path.join(base_path, 'selected_frames', frame)
        )


if __name__ == '__main__':
    main()
