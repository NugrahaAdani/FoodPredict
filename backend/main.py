from pathlib import Path
from uuid import uuid4
from typing import List, Dict, Optional

from fastapi import FastAPI, File, HTTPException, UploadFile, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from PIL import UnidentifiedImageError
from pydantic import BaseModel


app = FastAPI(title="Food Ingredient Classifier API", version="2.0.0")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"
FRONTEND_INDEX_PATH = FRONTEND_DIR / "index.html"
FRONTEND_SRC_DIR = FRONTEND_DIR / "src"
UPLOAD_DIR = Path(__file__).resolve().parent / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/src", StaticFiles(directory=FRONTEND_SRC_DIR), name="frontend-src")


# Pydantic models for nutrition endpoints
class RecipeIngredient(BaseModel):
    name: str
    amount_g: float = 100.0


class RecipeNutritionRequest(BaseModel):
    ingredients: List[RecipeIngredient]


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


@app.get("/")
def frontend_index():
    return FileResponse(FRONTEND_INDEX_PATH)


@app.get("/health")
def health_check():
    import os
    return {
        "status": "ok",
        "port": os.getenv("PORT", "not_set"),
        "host": "0.0.0.0",
        "message": "Food Classifier API is running"
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File harus berupa gambar.")

    content = await file.read()
    saved_path = _persist_upload(file.filename or "upload", content)

    try:
        prediction = predict_uploaded_image(saved_path)
        recommendation = generate_recommendation(prediction["predicted_class"])
        
        # Get nutrition info for predicted ingredient
        from backend.services.nutrition import nutrition_service
        nutrition_info = nutrition_service.get_nutrition_info(prediction["predicted_class"])
        
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
        "nutrition": nutrition_info,  # Added nutrition info
    }


# New nutrition endpoints
@app.get("/nutrition/{ingredient_name}")
def get_nutrition_info(ingredient_name: str):
    """Get nutrition information for a specific ingredient"""
    from backend.services.nutrition import nutrition_service
    
    nutrition_info = nutrition_service.get_nutrition_info(ingredient_name)
    
    if nutrition_info is None:
        raise HTTPException(
            status_code=404, 
            detail=f"Nutrition data not found for ingredient: {ingredient_name}"
        )
    
    return {
        "ingredient": ingredient_name,
        "nutrition": nutrition_info,
        "status": "success"
    }


@app.get("/nutrition/search")
def search_ingredients(
    q: str = Query(..., description="Search query for ingredient names"),
    limit: int = Query(10, ge=1, le=50, description="Maximum number of results")
):
    """Search ingredients by name"""
    from backend.services.nutrition import nutrition_service
    
    results = nutrition_service.search_ingredients(q, limit)
    
    return {
        "query": q,
        "results": results,
        "count": len(results),
        "status": "success"
    }


@app.get("/nutrition/summary")
def get_nutrition_summary():
    """Get nutrition data summary statistics"""
    from backend.services.nutrition import nutrition_service
    
    summary = nutrition_service.get_nutrition_summary()
    
    return {
        "summary": summary,
        "status": "success"
    }


@app.get("/nutrition/ingredients")
def list_all_ingredients():
    """Get list of all available ingredients"""
    from backend.services.nutrition import nutrition_service
    
    ingredients = nutrition_service.get_all_ingredients()
    
    return {
        "ingredients": ingredients,
        "count": len(ingredients),
        "status": "success"
    }


@app.post("/nutrition/recipe")
def calculate_recipe_nutrition(request: RecipeNutritionRequest):
    """Calculate total nutrition for a recipe"""
    from backend.services.nutrition import nutrition_service
    
    ingredients_data = [
        {"name": ing.name, "amount_g": ing.amount_g} 
        for ing in request.ingredients
    ]
    
    nutrition_totals = nutrition_service.calculate_recipe_nutrition(ingredients_data)
    
    return {
        "recipe_nutrition": nutrition_totals,
        "status": "success"
    }
