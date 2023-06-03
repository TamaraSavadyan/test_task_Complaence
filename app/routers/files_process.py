from typing import List
from fastapi import APIRouter, File, UploadFile


router = APIRouter(
    prefix = "/files",
    tags=['Files']
)



@router.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    for file in files:
        file_info = []
        contents = await file.read()
        # Обработка содержимого файла, например, сохранение в базу данных или выполнение других операций
        info = {
            "filename": file.filename,
            "content_type": file.content_type,
        }
        file_info.append(info)
        # Process the file contents (e.g., parse CSV data)
        # Do something with the contents of each file
    return {"files": file_info}



@router.get("/")
async def get_files(files: List[UploadFile] = File(...)):
    
    return {"files": 'your files'}