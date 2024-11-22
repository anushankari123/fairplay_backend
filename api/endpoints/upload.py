import os
import uuid
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse

upload_router = APIRouter(prefix="/uploads")

# Ensure upload directory exists
UPLOAD_DIRECTORY = "uploads/"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

@upload_router.post("")  # Change from "/image" to empty string
async def upload_image(file: UploadFile = File(...)):
    try:
        # Generate unique filename
        file_extension = file.filename.split('.')[-1]
        filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(UPLOAD_DIRECTORY, filename)

        # Save file
        content = await file.read()
        with open(file_path, "wb") as buffer:
            buffer.write(content)

        return JSONResponse(content={
            "image_url": f"/uploads/{filename}"
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))