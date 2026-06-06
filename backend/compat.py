import sys

try:
    import torchvision.transforms._functional_tensor as _ft

    if "torchvision.transforms.functional_tensor" not in sys.modules:
        sys.modules["torchvision.transforms.functional_tensor"] = _ft
except ImportError:
    pass
