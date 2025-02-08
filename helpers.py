import os
from fastapi import HTTPException
import uuid

# Supported image formats
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}

# 📌 Unique file name generation function with UUID
def generate_unique_filename(filename: str) -> str:
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file format! Only .jpg, .jpeg and .png are supported.")
    return f"{uuid.uuid4()}{ext}"