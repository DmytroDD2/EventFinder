import os
import uuid
from pathlib import Path
import filetype
from fastapi import HTTPException, status, UploadFile

UPLOAD_DIR = "uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

UPLOAD_DIR = "uploads"
MAX_SIZE_MB = 5
MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024


async def save_file(file: UploadFile):
    await validate_file_size(file)
    extension = await validate_file_type(file)

    file.filename = f"{uuid.uuid4()}.{extension}"
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        while chunk := await file.read(4096):
            f.write(chunk)

    return f"http://0.0.0.0:8000/uploads/{file.filename}"



def delete_file(filename: str):
    new_filename = filename.strip("http://0.0.0.0:8000/uploads/")
    file_path = os.path.join(UPLOAD_DIR, new_filename)

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail=f"File {new_filename} not found"
        )

    os.remove(file_path)
    return {"detail": f"File {filename} deleted successfully"}




async def validate_file_size(file: UploadFile):
    total_size = 0

    while chunk := await file.read(4096):
        total_size += len(chunk)
        if total_size > MAX_SIZE_BYTES:
            raise HTTPException(
                status_code=413,
                detail=f"File exceeds maximum size of {MAX_SIZE_MB}MB"
            )

    file.file.seek(0)



async def validate_file_type(file: UploadFile):
    ACCEPTED_TYPES = {
        "png": "image/png",
        "jpg": "image/jpeg",
        "heic": "image/heic",
        "heif": "image/heif",
        "heics": "image/heics",
    }

    file_info = filetype.guess(file.file)
    if file_info is None:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unable to determine file type",
        )

    detected_mime = file_info.mime.lower()
    detected_extension = file_info.extension.lower()

    if (
            detected_extension not in ACCEPTED_TYPES
            or detected_mime !=  ACCEPTED_TYPES.get(detected_extension)

    ):
        raise HTTPException(
            status_code=415,
            detail=f"File {detected_mime}/{detected_extension} unsupported",
        )

    return detected_extension

