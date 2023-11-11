from augmentation import *
import glob, os, shutil
import subprocess
import argparse

def copy_files(source_dir, target_dir, pattern):
    files = glob.iglob(os.path.join(source_dir, pattern))
    for file in files:
        if os.path.isfile(file):
            shutil.copy2(file, target_dir)

def execute(input_dir, output_dir, image_width, image_height, ratio, prefix):
    image_dir = os.path.join(output_dir, "images")
    resized_dir = os.path.join(output_dir, "resized")
    train_dir = os.path.join(resized_dir, "train")
    test_dir = os.path.join(resized_dir, "test")
    yolo_dir = os.path.join(output_dir, "yolo")
    os.mkdir(yolo_dir)
    os.mkdir(os.path.join(yolo_dir, "images"))
    os.mkdir(os.path.join(yolo_dir, "labels"))
    yolo_labels_train_dir = os.path.join(yolo_dir, "labels", "train")
    yolo_images_train_dir = os.path.join(yolo_dir, "images", "train")
    yolo_labels_test_dir = os.path.join(yolo_dir, "labels", "val")
    yolo_images_test_dir = os.path.join(yolo_dir, "images", "val")
    os.mkdir(yolo_labels_train_dir)
    os.mkdir(yolo_images_train_dir)
    os.mkdir(yolo_labels_test_dir)
    os.mkdir(yolo_images_test_dir)
    os.mkdir(image_dir)
    os.mkdir(resized_dir)
    print(f"Copying files from {input_dir} to {image_dir}")
    copy_files(input_dir, image_dir, "*.xml")
    copy_files(input_dir, image_dir, "*.jpg")
    print("Resizing images.")
    resize_all(image_dir, resized_dir, image_width, image_height, prefix)
    print("Partitioning dataset.")
    subprocess.call(["python", "partition_dataset.py", "-i", resized_dir, "-x", "-r", str(ratio)])
    print("Done.")
    print("Converting Pascal VOC to Darknet YOLO annotation files.")
    train_labels_dir = os.path.join(train_dir, "labels")
    os.mkdir(train_labels_dir)
    copy_files(train_dir, train_labels_dir, "*.xml")
    subprocess.call(["python", "voc_to_yolo/example.py", "--datasets", "VOC", "--img_path", train_dir, "--label", train_labels_dir, "--convert_output_path", yolo_labels_train_dir, "--img_type" ,'.jpg', "--cls_list_file", "voc_to_yolo/names.txt"])
    copy_files(train_dir, yolo_images_train_dir, "*.jpg")
    test_labels_dir = os.path.join(test_dir, "labels")
    os.mkdir(test_labels_dir)
    copy_files(test_dir, test_labels_dir, "*.xml")
    subprocess.call(["python", "voc_to_yolo/example.py", "--datasets", "VOC", "--img_path", test_dir, "--label", test_labels_dir, "--convert_output_path", yolo_labels_test_dir, "--img_type", '.jpg', "--cls_list_file", "voc_to_yolo/names.txt"])
    copy_files(test_dir, yolo_images_test_dir, "*.jpg")
    print("All done.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i',
                        '--input',
                        type=str,
                        required=True,
                        help='Input directory with images and xml annotation files.')
    parser.add_argument('-o',
                        '--output',
                        type=str,
                        required=True,
                        help='Output directory to write the processed data to.')
    parser.add_argument('-w',
                        '--width',
                        type=int,
                        required=False,
                        default=640,
                        help='Image width.')
    parser.add_argument('-d', # can't use -h because that's reserved for help
                        '--height',
                        type=int,
                        required=False,
                        default=640,
                        help='Image height.')
    parser.add_argument('-r',
                        '--ratio',
                        type=float,
                        required=False,
                        default=0.20,
                        help='Validation to training data split ratio.')
    parser.add_argument('-p',
                        '--prefix',
                        type=str,
                        required=True,
                        default="any",
                        help='The prefix for the filenames of the augmented images.')
    FLAGS = parser.parse_args()
    execute(FLAGS.input, FLAGS.output, FLAGS.width, FLAGS.height, FLAGS.ratio, FLAGS.prefix)

    
