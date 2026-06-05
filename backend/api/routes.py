import uuid
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from backend.config import OUTPUT_DIR, UPLOAD_DIR
from backend.pipelines.restoration import RestorationPipeline
from backend.utils.validation import validate_image

router = APIRouter()
pipeline = RestorationPipeline()


@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    try:
        validate_image(file)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    job_id = uuid.uuid4().hex[:12]
    ext = Path(file.filename).suffix.lower()
    filename = f"{job_id}{ext}"
    filepath = UPLOAD_DIR / filename

    content = await file.read()
    filepath.write_bytes(content)

    return {
        "job_id": job_id,
        "filename": filename,
        "filepath": str(filepath),
        "size": len(content),
    }


@router.post("/restore/{job_id}")
async def restore_image(job_id: str):
    input_path = None
    for ext in [".jpg", ".jpeg", ".png", ".webp"]:
        candidate = UPLOAD_DIR / f"{job_id}{ext}"
        if candidate.exists():
            input_path = candidate
            break

    if not input_path:
        raise HTTPException(status_code=404, detail="Image not found")

    output_path = OUTPUT_DIR / f"{job_id}_restored.png"

    try:
        result = pipeline.run(str(input_path), str(output_path))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "job_id": job_id,
        "original": str(input_path),
        "restored": str(output_path),
        "processing_time": result.get("processing_time", 0),
        "models_used": result.get("models_used", []),
    }


@router.get("/download/{job_id}")
async def download_image(job_id: str):
    for ext in [".png", ".jpg", ".jpeg", ".webp"]:
        candidate = OUTPUT_DIR / f"{job_id}_restored{ext}"
        if candidate.exists():
            return FileResponse(
                str(candidate),
                media_type="image/png",
                filename=f"restored_{job_id}.png",
            )

    raise HTTPException(status_code=404, detail="Restored image not found")


@router.get("/status/{job_id}")
async def get_status(job_id: str):
    original = None
    for ext in [".jpg", ".jpeg", ".png", ".webp"]:
        candidate = UPLOAD_DIR / f"{job_id}{ext}"
        if candidate.exists():
            original = str(candidate)
            break

    restored = None
    for ext in [".png", ".jpg", ".jpeg", ".webp"]:
        candidate = OUTPUT_DIR / f"{job_id}_restored{ext}"
        if candidate.exists():
            restored = str(candidate)
            break

    return {"job_id": job_id, "original": original, "restored": restored}
