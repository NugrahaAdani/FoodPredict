from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import UnidentifiedImageError


app = FastAPI(title="Food Ingredient Classifier API", version="2.0.0")

# CORS untuk frontend terpisah
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://localhost:8080"],  # React, Vite, Vue
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path(__file__).resolve().parent / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def _persist_upload(filename: str, content: bytes) -> Path:
    suffix = Path(filename or "").suffix or ".bin"
    target = UPLOAD_DIR / f"{uuid4().hex}{suffix}"
    target.write_bytes(content)
    return target


def predict_uploaded_image(image_path: Path):
    from backend.services.predict import predict_uploaded_image as predict_impl
    return predict_impl(image_path)


def generate_recommendation(predicted_class: str):
    from backend.services.recommendation import generate_recommendation as recommendation_impl
    return recommendation_impl(predicted_class)


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Food Classifier API is running"}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File harus berupa gambar.")

    content = await file.read()
    saved_path = _persist_upload(file.filename or "upload", content)

    try:
        prediction = predict_uploaded_image(saved_path)
        recommendation = generate_recommendation(prediction["predicted_class"])
    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except UnidentifiedImageError as exc:
        raise HTTPException(status_code=400, detail="File gambar tidak valid.") from exc

    return {
        "filename": file.filename,
        "prediction": {
            "label": prediction["predicted_class"],
            "confidence": prediction["confidence"],
        },
        "recommendation": recommendation,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)