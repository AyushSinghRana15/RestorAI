import logging
import urllib.request
from pathlib import Path

import cv2
import numpy as np

logger = logging.getLogger(__name__)

WEIGHTS_DIR = Path(__file__).resolve().parent.parent.parent / "gfpgan" / "weights"

PROTOTXT_URL = (
    "https://raw.githubusercontent.com/richzhang/colorization/caffe"
    "/models/colorization_deploy_v2.prototxt"
)
CAFFEMODEL_URL = (
    "https://huggingface.co/spaces/viveknarayan/Image_Colorization"
    "/resolve/main/colorization_release_v2.caffemodel"
)

PROTOTXT_PATH = WEIGHTS_DIR / "colorization_deploy_v2.prototxt"
CAFFEMODEL_PATH = WEIGHTS_DIR / "colorization_release_v2.caffemodel"

# 313 ab-space cluster centers from Zhang et al. colorization paper
PTS_PATH = WEIGHTS_DIR / "pts_in_hull.npy"


class DeOldifyColorizer:
    def __init__(self, device="cpu"):
        self.device = device
        self.net = None
        self._load_model()

    def _download(self, url: str, dest: Path):
        logger.info("Downloading %s to %s", url, dest)
        urllib.request.urlretrieve(url, dest)

    def _load_model(self):
        try:
            WEIGHTS_DIR.mkdir(parents=True, exist_ok=True)

            if not CAFFEMODEL_PATH.exists():
                self._download(CAFFEMODEL_URL, CAFFEMODEL_PATH)
            if not PROTOTXT_PATH.exists():
                self._download(PROTOTXT_URL, PROTOTXT_PATH)

            self.net = cv2.dnn.readNetFromCaffe(
                str(PROTOTXT_PATH), str(CAFFEMODEL_PATH)
            )

            if not PTS_PATH.exists():
                logger.warning("pts_in_hull.npy not found at %s", PTS_PATH)
            else:
                pts = np.load(str(PTS_PATH))
                pts = pts.reshape(2, 313, 1, 1).astype(np.float32)
                class8 = self.net.getLayerId("class8_ab")
                conv8 = self.net.getLayerId("conv8_313_rh")
                self.net.getLayer(class8).blobs = [pts]
                self.net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype=np.float32)]

            logger.info("DeOldify (OpenCV DNN colorization) model loaded")
        except Exception as e:
            logger.warning("Failed to load DeOldify colorization model: %s", e)

    def colorize(self, image: np.ndarray) -> np.ndarray:
        if self.net is None:
            logger.info("DeOldify model unavailable — returning original image")
            return image

        try:
            orig_h, orig_w = image.shape[:2]
            img_rgb = (image * 1.0).astype(np.uint8)
            img_lab = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2LAB)
            img_l = img_lab[:, :, 0]

            img_resized = cv2.resize(img_rgb, (224, 224))
            img_lab_resized = cv2.cvtColor(img_resized, cv2.COLOR_RGB2LAB)
            img_l_resized = img_lab_resized[:, :, 0]

            inp = img_l_resized.astype(np.float32) - 50
            inp = inp[np.newaxis, np.newaxis, :, :]

            self.net.setInput(inp)
            ab = self.net.forward("class8_ab")
            ab = ab.squeeze().transpose((1, 2, 0))
            ab = cv2.resize(ab, (orig_w, orig_h))
            ab = (ab * 255).astype(np.uint8)

            img_lab_out = np.zeros((orig_h, orig_w, 3), dtype=np.uint8)
            img_lab_out[:, :, 0] = img_l
            img_lab_out[:, :, 1:] = ab
            result = cv2.cvtColor(img_lab_out, cv2.COLOR_LAB2RGB)

            return result
        except Exception as e:
            logger.warning("DeOldify colorization failed: %s", e)
            return image
