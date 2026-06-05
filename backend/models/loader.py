import logging

from backend.config import DEVICE

logger = logging.getLogger(__name__)


class ModelLoader:
    _instances = {}

    @classmethod
    def get_gfpgan(cls):
        if "gfpgan" not in cls._instances:
            try:
                from gfpgan import GFPGANer

                cls._instances["gfpgan"] = GFPGANer(
                    model_path=None,
                    upscale=1,
                    arch="clean",
                    channel_multiplier=2,
                    bg_upsampler=None,
                    device=DEVICE,
                )
                logger.info("GFPGAN model loaded")
            except Exception as e:
                logger.warning("Failed to load GFPGAN: %s", e)
                cls._instances["gfpgan"] = None
        return cls._instances["gfpgan"]

    @classmethod
    def get_realesrgan(cls):
        if "realesrgan" not in cls._instances:
            try:
                from realesrgan import RealESRGANer
                from basicsr.archs.rrdbnet_arch import RRDBNet

                model = RRDBNet(
                    num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4
                )
                cls._instances["realesrgan"] = RealESRGANer(
                    scale=4,
                    model_path=None,
                    model=model,
                    tile=400,
                    tile_pad=10,
                    pre_pad=0,
                    half=DEVICE != "cpu",
                    device=DEVICE,
                )
                logger.info("Real-ESRGAN model loaded")
            except Exception as e:
                logger.warning("Failed to load Real-ESRGAN: %s", e)
                cls._instances["realesrgan"] = None
        return cls._instances["realesrgan"]

    @classmethod
    def get_lama(cls):
        if "lama" not in cls._instances:
            try:
                from backend.models.lama_wrapper import LaMaInpainter

                cls._instances["lama"] = LaMaInpainter(device=DEVICE)
                logger.info("LaMa model loaded")
            except Exception as e:
                logger.warning("Failed to load LaMa: %s", e)
                cls._instances["lama"] = None
        return cls._instances["lama"]

    @classmethod
    def get_deoldify(cls):
        if "deoldify" not in cls._instances:
            try:
                from backend.models.deoldify_wrapper import DeOldifyColorizer

                cls._instances["deoldify"] = DeOldifyColorizer(device=DEVICE)
                logger.info("DeOldify model loaded")
            except Exception as e:
                logger.warning("Failed to load DeOldify: %s", e)
                cls._instances["deoldify"] = None
        return cls._instances["deoldify"]

    @classmethod
    def clear(cls):
        cls._instances.clear()
        import torch
        torch.cuda.empty_cache()
        logger.info("All model instances cleared")
