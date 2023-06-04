from typing import List
from fastapi import APIRouter, File, HTTPException, UploadFile, status, Depends
from sqlalchemy import Column, Integer, String, Table
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from csv import reader
from chardet import detect
from .user import check_user_authorization
from models import User, File as UploadedFile

router = APIRouter(
    prefix = "/files",
    tags=['Files'],
)


@router.post("/upload")
async def upload_files(id: int, files: List[UploadFile] = File(...), db: AsyncSession = Depends(get_db)):

    user = await check_user_authorization(id, db)

    if not files:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Files were not uploaded")
    
    for file in files:
        
        contents = await file.read()
        encoding = detect(contents)['encoding']
        file_content = contents.decode(encoding)

        new_file = UploadedFile(
            filename=file.filename,
            filetype=file.content_type,
            file_data=file_content,
            user = user,
        )

        await db.add(new_file)
        await db.commit()
        await db.refresh(new_file)

        file_content.clear()

    return {"Ok": 'Files were uploaded successfully'}


@router.get("/")
async def get_files(id: int, db: AsyncSession = Depends(get_db)):
    user = await check_user_authorization(id, db)

    files = await db.query(UploadedFile).filter(UploadedFile.user_id == id).all()
    if not files:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Files were not found")

    file_list = []

    for file in files:

        if file.file_data:
            first_row = file.file_data.split("\n")[0]
            columns = first_row.split(",")

        file_info = {
            "filename": file.filename,
            "filetype": file.filetype,
            "uploaded_at": file.uploaded_at,
            "columns": columns
        }

        file_list.append(file_info)
    
    return {"Uploaded files": file_list}


@router.get("/{id}/filter")
async def get_filter_file_data(user_id: int, file_id: int, 
                               columns: List[str] = None, column_order_by: str = None,
                               sort_type: str = 'ASC',
                               db: AsyncSession = Depends(get_db)):
    
    user = await check_user_authorization(user_id, db)

    file = await db.query(UploadedFile).filter(UploadedFile.id == file_id).first()
    if not file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="File not found")
    
    file_data = file.file_data.split("\n")

    if columns:
        filtered_data = []
        for row in file_data:
            columns_data = row.split(",")
            filtered_row = [columns_data[i] for i, column in enumerate(file.columns) if column in columns]
            filtered_data.append(",".join(filtered_row))
        file_data = filtered_data

    response = FileDataResponse(file_id=file.id, file_data=file_data)

    return response
    


    


    
  