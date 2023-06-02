from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

app = FastAPI()
security = HTTPBearer()

# Секретный ключ для подписи токена
SECRET_KEY = "your-secret-key"

# Роль администратора
ADMIN_ROLE = "admin"

# Функция проверки аутентификации администратора
async def is_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        # Расшифровка и проверка токена
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("username")
        roles = payload.get("roles")

        if not username or ADMIN_ROLE not in roles:
            raise HTTPException(status_code=403, detail="Unauthorized")

        return username

    except JWTError:
        raise HTTPException(status_code=403, detail="Unauthorized")


@app.get("/admin")
async def admin_route(username: str = Depends(is_admin)):
    return {"message": f"Welcome, {username}! You are an admin."}




from fastapi import FastAPI, UploadFile, File
import pandas as pd

app = FastAPI()

# Список загруженных файлов
uploaded_files = []


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Загрузка файла
    contents = await file.read()

    # Преобразование содержимого файла в объект DataFrame с помощью pandas
    df = pd.read_csv(contents)

    # Сохранение информации о загруженном файле
    uploaded_files.append({
        'filename': file.filename,
        'columns': df.columns.tolist()
    })

    return {"message": "File uploaded successfully"}


@app.get("/files")
async def get_files():
    # Возвращение списка файлов с информацией о колонках
    return uploaded_files


@app.get("/data/{filename}")
async def get_data(filename: str, filters: str = None, sort_by: str = None):
    # Получение данных из конкретного файла с опциональными фильтрацией и сортировкой

    # Находим файл по имени
    file_data = next((f for f in uploaded_files if f['filename'] == filename), None)
    if file_data is None:
        return {"message": "File not found"}

    # Загружаем файл в DataFrame
    df = pd.read_csv(filename)

    # Применяем фильтры, если они указаны
    if filters:
        # Пример: фильтрация по столбцу "column_name" со значением "filter_value"
        df = df[df['column_name'] == filter_value]

    # Сортируем, если указан столбец для сортировки
    if sort_by:
        df = df.sort_values(by=sort_by)

    # Возвращаем результат в виде списка словарей
    return df.to_dict('records')



from fastapi import FastAPI, HTTPException, Depends
from starlette import status
from starlette.requests import Request

import settings
from router import api_router
from utils import check_auth

docs_kwargs = {}  # noqa: pylint=invalid-name
if settings.ENVIRONMENT == 'production':
    docs_kwargs = dict(docs_url=None, redoc_url=None)  # noqa: pylint=invalid-name

app = FastAPI(**docs_kwargs)  # noqa: pylint=invalid-name

async def check_auth_middleware(request: Request):
    if settings.ENVIRONMENT in ('production', 'test'):
        body = await request.body()
        if not check_auth(body, request.headers.get('X-Hub-Signature', '')):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

app.include_router(api_router, dependencies=[Depends(check_auth_middleware)])

# from fastapi import FastAPI
# from starlette import status
# from starlette.responses import Response

# from models import Body

# app = FastAPI()  # noqa: pylint=invalid-name

# @app.post("/release/")
# async def release(*,
#                   body: Body,
#                   chat_id: str = None):
#     await proceed_release(body, chat_id)
#     return Response(status_code=status.HTTP_200_OK)