import torch
import logging
import numpy as np
from datetime import datetime


class CoreHDF:
    def __init__(self, conf_thres=0.25, iou_thres=0.45, classes=None,
                 repo='ultralytics/yolov5',
                 model='yolov5s',
                 log_dst='log.txt'):
        self.model = torch.hub.load(repo, model)
        self.model.conf_thres = conf_thres
        self.model.iou_thres = iou_thres
        self.model.classes = classes

        self.logger = logging.getLogger("CoreHDF")
        self.logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(log_dst, 'a+')
        fh.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter('[%(levelname)s/%(asctime)s] %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

        self.logger.debug("Created CoreHDF instance")

    def predict(self, image):
        return self.model(image)

    def record(self, image, img_dst='image_logs/', render=True):
        results = self.model(image)
        results.files = [datetime.strftime(datetime.now(), f'%Y-%m-%d %H-%M-%S [{i}].jpg')
                         for i in range(len(results.files))]
        pred = torch.stack(results.pred)
        mask = pred[:, :, -1] == results.names.index('person')
        persons_count = torch.sum(mask)
        if render:
            results.render()

        if not persons_count:
            self.logger.debug(f'No person detected out of '
                              f'{len(pred[:, :, -1])} detected objects')
        else :
            self.logger.info(f'Detected {persons_count} person{"s" * (persons_count > 1)}')
            self.logger.debug(f'Saving image')
            results.save(img_dst)


