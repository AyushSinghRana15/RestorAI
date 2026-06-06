import logging
import time

import cv2
import numpy as np

from backend.models.loader import ModelLoader

logger = logging.getLogger(__name__)


class RestorationPipeline:
    def __init__(self):
        pass

    def run(self, input_path: str, output_path: str, colorize: bool = False) -> dict:
        start = time.time()
        models_used = []

        image = cv2.imread(input_path)
        if image is None:
            raise ValueError(f"Could not read image: {input_path}")
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # scratch removal
        lama = ModelLoader.get_lama()
        if lama:
            image_rgb = lama.inpaint(image_rgb)
            models_used.append("LaMa")

        # face restoration
        gfpgan = ModelLoader.get_gfpgan()
        if gfpgan:
            try:
                _, _, image_rgb = gfpgan.enhance(
                    image_rgb,
                    has_aligned=False,
                    only_center_face=False,
                    paste_back=True,
                )
                models_used.append("GFPGAN")
            except Exception as e:
                logger.warning("GFPGAN failed: %s", e)

        # super resolution
        realesrgan = ModelLoader.get_realesrgan()
        if realesrgan:
            try:
                image_rgb, _ = realesrgan.enhance(image_rgb, outscale=2)
                models_used.append("Real-ESRGAN")
            except Exception as e:
                logger.warning("Real-ESRGAN failed: %s", e)

        # colorization
        if colorize:
            deoldify = ModelLoader.get_deoldify()
            if deoldify:
                image_rgb = deoldify.colorize(image_rgb)
                models_used.append("DeOldify")

        output_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
        cv2.imwrite(output_path, output_bgr)

        elapsed = round(time.time() - start, 2)

        return {
            "processing_time": elapsed,
            "models_used": models_used,
        }
