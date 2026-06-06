import logging

import cv2
import numpy as np

logger = logging.getLogger(__name__)


class LaMaInpainter:
    def __init__(self, device="cpu"):
        self.device = device

    def inpaint(self, image: np.ndarray, mask: np.ndarray = None) -> np.ndarray:
        if mask is not None:
            inpainted = cv2.inpaint(image, mask, 3, cv2.INPAINT_TELEA)
            return inpainted

        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        mask = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)[1]
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=1)

        if cv2.countNonZero(mask) == 0:
            return image

        inpainted = cv2.inpaint(image, mask, 3, cv2.INPAINT_TELEA)
        return inpainted
