from PIL import Image
from imgaug.augmenters.meta import Sequential
import numpy as np
from pascalvoc import *
import imgaug.augmenters as iaa
import imageio
from imgaug.augmentables.bbs import BoundingBox, BoundingBoxesOnImage
import glob
import os
import ntpath
import math
import cv2

def augment(
    dataset_dir,
    output_dir,
    image_suffix,
    augmentation: List[Sequential],
    new_width: int = None,
    new_height: int = None,
) -> None:
    all_data = glob.glob(os.path.join(dataset_dir, "*.jpg"))
    counter = 0
    for datum in all_data:
        filename_no_ext = os.path.splitext(ntpath.basename(datum))[0]
        bb_filepath = os.path.join(dataset_dir, filename_no_ext + ".xml")
        arr = cv2.imread(datum, 1)
        arr = cv2.cvtColor(arr, cv2.COLOR_BGR2RGB)
        vocfile = VOCFile(bb_filepath)
        annotation = vocfile.load()
        bbs = []
        for vocbb in annotation.bounding_boxes:
            bbs.append(
                BoundingBox(x1=vocbb.xmin, y1=vocbb.ymin, x2=vocbb.xmax, y2=vocbb.ymax)
            )
        bbimage = BoundingBoxesOnImage(bbs, shape=arr.shape)
        seq = iaa.Sequential(augmentation)
        img_aug, bbs_aug = seq(image=arr, bounding_boxes=bbimage)
        output_image_filename = filename_no_ext + ".jpg"
        output_image_filepath = os.path.join(output_dir, output_image_filename)
        output_bb_filename = filename_no_ext + ".xml"
        output_bb_filepath = os.path.join(output_dir, output_bb_filename)
        imageio.imwrite(output_image_filepath, img_aug)
        bbs = []
        i = 0
        for bb_aug in bbs_aug:
            bbs.append(
                VOCBoundingBox(
                    annotation.bounding_boxes[i].name,
                    math.floor(bb_aug.x1),
                    math.floor(bb_aug.y1),
                    math.floor(bb_aug.x2),
                    math.floor(bb_aug.y2),
                )
            )
            i = i + 1
        annotation.bounding_boxes = []
        for bb in bbs:
            annotation.add_bounding_box(bb)
        if new_width is not None:
            annotation.width = new_width
        if new_height is not None:
            annotation.height = new_height
        annotation.filename = output_image_filename
        vocfile.save(annotation, output_bb_filepath)
        counter = counter + 1


def rename_all(dir, suffix):
    all_data = glob.glob(os.path.join(dir, "*.jpg"))
    for datum in all_data:
        filename_no_ext = os.path.splitext(ntpath.basename(datum))[0]
        bb_filepath = os.path.join(dir, filename_no_ext + ".xml")
        filename_new = os.path.join(dir, filename_no_ext + suffix + ".jpg")
        bb_filename_new = os.path.join(dir, filename_no_ext + suffix + ".xml")
        os.rename(datum, filename_new)
        os.rename(bb_filepath, bb_filename_new)

def apply_augmentations(image_dir, prefix):
    augment(
        image_dir,
        image_dir,
        prefix + "-random1-",
        [
            iaa.GaussianBlur(sigma=(0.0, 3.0)),
            iaa.Fliplr(0.5),
            iaa.Rotate((-3, 3)),
            iaa.GammaContrast((0.5, 2.0))
        ]
    )
    augment(
        image_dir,
        image_dir,
        prefix + "-random2-",
        [
            iaa.GaussianBlur(sigma=(0.0, 3.0)),
            iaa.Flipud(0.5),
            iaa.Rotate((-3, 3)),
            iaa.GammaContrast((0.5, 2.0))
        ]
    )

def resize_all(image_dir, output_dir, new_width, new_height, prefix):
    augment(
        image_dir,
        output_dir,
        "",
        [iaa.CenterPadToSquare(), iaa.Resize({"height": new_height, "width": new_width})],
        new_width, new_height
    )