# YOLOv5 🚀 by Ultralytics, GPL-3.0 license
import argparse
import os
import sys
from pathlib import Path
import numpy as np

from utils.augmentations import letterbox
import cv2
import torch
import torch.backends.cudnn as cudnn

from models.common import DetectMultiBackend
from utils.general import (
    check_img_size,
    non_max_suppression,
    print_args,
    scale_coords,
)
from utils.torch_utils import select_device, time_sync


class object_detection:
    def __init__(self, weights):
        # fmt: off
        self.data="data/coco128.yaml"
        self.weights = weights
        self.imgsz=(640, 640)  # inference size (height, width)
        self.conf_thres=0.25  # confidence threshold
        self.iou_thres=0.45  # NMS IOU threshold
        self.max_det=1000  # maximum detections per image
        self.device= select_device("")  # cuda device, i.e. 0 or 0,1,2,3 or cpu
        self.view_img=False  # show results
        self.save_txt=False  # save results to *.txt
        self.save_conf=False  # save confidences in --save-txt labels
        self.save_crop=False  # save cropped prediction boxes
        self.nosave=False  # do not save images/videos
        self.classes=None  # filter by class: --class 0, or --class 0 2 3
        self.agnostic_nms=False  # class-agnostic NMS
        self.augment=False  # augmented inference
        self.visualize=False  # visualize features
        self.update=False  # update all models
        self.project="runs/detect"  # save results to project/name
        self.name="exp"  # save results to project/name
        self.exist_ok=False  # existing project/name ok, do not increment
        self.line_thickness=3  # bounding box thickness (pixels)
        self.hide_labels=False  # hide labels
        self.hide_conf=False  # hide confidences
        self.half=False  # use FP16 half-precision inference
        self.dnn=False  # use OpenCV DNN for ONNX inference
        # fmt: on

        print(self.weights, self.device, self.dnn, self.data)
        self.model = DetectMultiBackend(
            self.weights, device=self.device, dnn=self.dnn, data=self.data
        )
        stride, self.cls, pt, jit, onnx, engine = (
            self.model.stride,
            self.model.names,
            self.model.pt,
            self.model.jit,
            self.model.onnx,
            self.model.engine,
        )

        self.imgsz = check_img_size(self.imgsz, s=stride)

        # Half
        self.half &= (
            pt or jit or onnx or engine
        ) and self.device.type != "cpu"  # FP16 supported on limited backends with CUDA
        if pt or jit:
            self.model.model.half() if self.half else self.model.model.float()

        self.model.warmup(imgsz=(1, 3, *self.imgsz), half=self.half)

    @torch.no_grad()
    def bounding_box(self, image):
        im = letterbox(image)[0]
        im = np.ascontiguousarray(im.transpose((2, 0, 1))[::-1])
        im = torch.from_numpy(im).to(self.device)
        im = im.half() if self.half else im.float()
        im /= 255
        if len(im.shape) == 3:
            im = im[None]
        pred = self.model(im)
        # print(pred)
        pred = non_max_suppression(
            pred,
            self.conf_thres,
            self.iou_thres,
            self.classes,
            self.agnostic_nms,
            max_det=self.max_det,
        )

        pred[0][:, :4] = scale_coords(im.shape[2:], pred[0][:, :4], image.shape).round()

        result = []
        for *xyxy, conf, cls in reversed(pred[0]):
            p1, p2, conf = (
                (int(xyxy[0]), int(xyxy[1])),
                (int(xyxy[2]), int(xyxy[3])),
                float(conf),
            )
            result.append((p1, p2, conf, self.cls[int(cls)]))

        return result

