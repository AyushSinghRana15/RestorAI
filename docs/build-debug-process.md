# RestorAI Build & Debug Process

## Initial State

- Frontend built successfully with `npm run build` (665ms, no errors)
- Backend `venv/` existed but had **broken paths** — shebangs pointed to `/Users/ayushsingh/Practical/RestorAI/venv/bin/python3.11` instead of the current location `/Users/ayushsingh/Projects/RestorAI/venv/bin/python3.11`
- Model weight files existed at `gfpgan/weights/` (GFPGANv1.3.pth, RealESRGAN_x4plus.pth, detection_Resnet50_Final.pth, parsing_parsenet.pth)
- `samples/` directory had `.gitkeep` and `oil-124_og.jpg`

---

## Issues Found & Fixed

### 1. Broken Venv Paths

**Problem:** Virtual environment was moved from `/Users/ayushsingh/Practical/RestorAI/` to `/Users/ayushsingh/Projects/RestorAI/`, breaking all shebangs.

**Fix:** Patched shebangs in `venv/bin/pip`, `venv/bin/pip3`, `venv/bin/pip3.11` with `sed` to point to the new location.

**Files affected:** `venv/bin/pip`, `venv/bin/pip3`, `venv/bin/pip3.11`, `venv/bin/activate`

---

### 2. Torchvision Compat Shim Not Auto-Applied

**Problem:** `backend/compat.py` provides a shim for `torchvision.transforms.functional_tensor` (needed by GFPGAN/Real-ESRGAN with newer torchvision), but was only imported in `backend/main.py`. Standalone scripts and model loaders failed with:

```
No module named 'torchvision.transforms.functional_tensor'
```

**Fix (commit `f1a763f`):**
- Added `import backend.compat` to `backend/__init__.py` — this auto-runs whenever any `backend` package is imported
- Removed the redundant `import backend.compat` from `backend/main.py`
- Wrapped the compat import in `try/except` for robustness

**Files changed:**
- `backend/__init__.py` — added import
- `backend/compat.py` — added try/except
- `backend/main.py` — removed redundant import

---

### 3. Pipeline `models_loaded` Flag Blocked Late Model Loading

**Problem:** `RestorationPipeline._ensure_models()` set `models_loaded = True` after loading core models. If `colorize=False` on the first call, DeOldify was never loaded even if `colorize=True` on a subsequent call, because the flag prevented re-entry.

**Fix (commit `78e2643`):**
- Removed `_ensure_models()` entirely
- Rely solely on `ModelLoader`'s singleton pattern — each `get_*()` method caches its model instance, so calling them is idempotent
- DeOldify is only loaded when `colorize=True`

**Files changed:**
- `backend/pipelines/restoration.py`

---

### 4. LaMa Wrapper — Only Detected Bright Scratches

**Problem:** The inpainter only detected bright pixels (threshold > 250) as damage. Old photos primarily have **dark cracks** (low pixel values), which were completely missed. The mask was empty for dark-damaged images, so no inpainting occurred.

```
mask = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)[1]  # Only bright spots
```

**Fix (commit `23f316f`):**
- Added **blackhat morphology** to detect dark cracks (dark features on light background)
- Added **tophat morphology** to detect bright scratches
- Added **Canny edge detection** for crack lines
- Combined all three into a single mask
- Dilated the mask for better coverage

```python
dark_mask = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, kernel)
bright_mask = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, kernel)
edges = cv2.Canny(gray, 30, 100)
mask = cv2.bitwise_or(dark_mask, bright_mask)
mask = cv2.bitwise_or(mask, edge_mask)
```

**Files changed:**
- `backend/models/lama_wrapper.py`

---

### 5. DeOldify Wrapper — Stub With Wrong Paths

**Problem:** The DeOldify wrapper was a complete stub:
- Model path was wrong: looked at `backend/models/../models/deoldify.pt` instead of `gfpgan/weights/`
- No actual model was ever loaded — `colorize()` returned the original image unchanged
- Download URLs for the OpenCV DNN colorization model were outdated (all returned 404/403)

**Fix (commit `23f316f`):**
- Changed model download URLs to working sources:
  - Prototxt: `https://raw.githubusercontent.com/richzhang/colorization/caffe/models/colorization_deploy_v2.prototxt`
  - Caffemodel: `https://huggingface.co/spaces/viveknarayan/Image_Colorization/resolve/main/colorization_release_v2.caffemodel`
- Implemented proper `pts_in_hull.npy` generation from OpenCV source (auto-downloaded and generated if missing)
- Implemented full `colorize()` using OpenCV DNN:
  1. Convert RGB → LAB
  2. Resize to 224×224
  3. Run through the colorization DNN
  4. Resize AB channels back to original dimensions
  5. Combine with original L channel
  6. Convert LAB → RGB

**Files changed:**
- `backend/models/deoldify_wrapper.py`

---

### 6. Large Model Weights Accidental Commit

**Problem:** `git add -A` picked up `gfpgan/weights/*.pth` (~610MB total) and sample restored images. These should never be in the repository.

**Fix (commit `f1a763f`):**
- Added `gfpgan/weights/` and `samples/*.png`/`samples/*.jpg` to `.gitignore`
- Used `git rm --cached` to untrack large files
- Amended the commit to exclude them

**Files changed:**
- `.gitignore`

---

## Final Pipeline Result

The restoration pipeline now runs successfully with all 4 models:

```text
Input:  samples/oil-124_og.jpg  (940×1175, color JPG)
LaMa:   ✓ (OpenCV inpainting with dark+bright+edge mask)
GFPGAN: ✓ (face restoration)
Real-ESRGAN: ✓ (2× super-resolution, tile 9/9)
DeOldify: ✓ (OpenCV DNN colorization)
Output: samples/oil-124_restored.png (1880×2350, color PNG)
Time:   ~229 seconds (first run, includes model loading)
Models: ['LaMa', 'GFPGAN', 'Real-ESRGAN', 'DeOldify']
```

## How to Run

```bash
# Activate venv (after fixing paths if moved)
source venv/bin/activate

# Single image restoration
cd /Users/ayushsingh/Projects/RestorAI
PYTHONPATH=. python -c "
from backend.pipelines.restoration import RestorationPipeline
pipeline = RestorationPipeline()
result = pipeline.run(
    input_path='samples/oil-124_og.jpg',
    output_path='samples/oil-124_restored.png',
    colorize=True
)
print(result)
"

# Start the API server
python -m backend.run
# Then POST to http://localhost:8000/api/upload + /api/restore/{job_id}
```

## Git History

```
23f316f fix: improve LaMa crack detection, fix DeOldify URLs and hull pts
78e2643 fix: remove models_loaded flag, rely on ModelLoader singleton
c6a2152 fix: only load DeOldify model when colorize=True
014f369 fix: DeOldify wrapper - correct path + OpenCV DNN implementation
f1a763f fix: auto-apply torchvision compat shim on backend import
```
