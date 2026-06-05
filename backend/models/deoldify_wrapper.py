import logging

import numpy as np

logger = logging.getLogger(__name__)


class DeOldifyColorizer:
    def __init__(self, device="cpu"):
        self.device = device
        self.model = None
        self._load_model()

    def _load_model(self):
        try:
            from os.path import exists, join, dirname, abspath

            model_path = join(dirname(abspath(__file__)), "..", "models", "deoldify.pt")
            if exists(model_path):
                logger.info("Loading DeOldify model from %s", model_path)
            else:
                logger.warning("DeOldify model weights not found at %s", model_path)
        except Exception as e:
            logger.warning("Could not initialize DeOldify model: %s", e)

    def colorize(self, image: np.ndarray) -> np.ndarray:
        if self.model is None:
            logger.info("DeOldify model unavailable — returning original image")
            return image

        return image
