#!/usr/bin/env python2

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from collections import defaultdict
import argparse
import cv2  # NOQA (Must import before importing caffe2 due to bug in cv2)
import glob
import logging
import os
import sys
import time

from caffe2.python import workspace

from core.config import assert_and_infer_cfg
from core.config import cfg
from core.config import merge_cfg_from_file
from utils.io import cache_url
from utils.timer import Timer
import core.test_engine as infer_engine
import datasets.dummy_datasets as dummy_datasets
import utils.c2 as c2_utils
import utils.logging
import utils.vis_k2m30 as vis_utils

c2_utils.import_detectron_ops()
# OpenCL may be enabled by default in OpenCV3; disable it because it's not
# thread safe and causes unwanted GPU memory allocations.
cv2.ocl.setUseOpenCL(False)


def main():
    logger = logging.getLogger(__name__)
    merge_cfg_from_file('/detectron/e2e_mask_rcnn_R-101-FPN_2x.yaml')
    cfg.NUM_GPUS = 1
    assert_and_infer_cfg()
    model = infer_engine.initialize_model_from_cfg('/detectron/models/model_final.pkl')
    dummy_coco_dataset = dummy_datasets.get_coco_dataset()
    # cam = cv2.VideoCapture("rtsp://192.168.128.12:554/mpeg4cif")
    cam = cv2.VideoCapture("rtsp://192.168.128.11:554/av0_1")
    n = 0
    tmp_file_name = '/tmp/tmp.jpg'
    im0 = 0
    im1 = 0
    while True:

        ret_val, im = cam.read()
        cv2.imwrite(tmp_file_name, im)
        im = cv2.imread(tmp_file_name)
        timers = defaultdict(Timer)
        with c2_utils.NamedCudaScope(0):
            cls_boxes, cls_segms, cls_keyps = infer_engine.im_detect_all(
                model, im, None, timers=timers
            )
        data = vis_utils.vis_one_image_opencv(
            im[:, :, ::-1],  # BGR -> RGB for visualization
            cls_boxes,
            cls_segms,
            cls_keyps,
            dataset=dummy_coco_dataset,
            # box_alpha=0.3,
            show_class=True,
            thresh=0.7,
            kp_thresh=2,
            # ext='png'
        )
        # time.sleep(0.1)
        # if data == None:
        #     logger.info(cls_boxes)
        #
        # else:
        n += 1
        n = n % 10

        logger.info(data)
        cv2.imwrite('/tmp/' + str(n) + '.jpg', data)


if __name__ == '__main__':
    workspace.GlobalInit(['caffe2', '--caffe2_log_level=0'])
    utils.logging.setup_logging(__name__)
    main()
