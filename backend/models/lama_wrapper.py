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
        kernel = np.ones((5, 5), np.uint8)

        dark_mask = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, kernel)
        _, dark_mask = cv2.threshold(dark_mask, 20, 255, cv2.THRESH_BINARY)

        bright_mask = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, kernel)
        _, bright_mask = cv2.threshold(bright_mask, 20, 255, cv2.THRESH_BINARY)

        edges = cv2.Canny(gray, 30, 100)
        edge_mask = cv2.dilate(edges, np.ones((2, 2), np.uint8), iterations=1)

        mask = cv2.bitwise_or(dark_mask, bright_mask)
        mask = cv2.bitwise_or(mask, edge_mask)
        mask = cv2.dilate(mask, kernel, iterations=1)

        if cv2.countNonZero(mask) == 0:
            return image

        inpainted = cv2.inpaint(image, mask, 3, cv2.INPAINT_TELEA)
        return inpainted
