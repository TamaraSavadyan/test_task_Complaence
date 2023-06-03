import jwt
from fastapi import FastAPI, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta

app = FastAPI()
security = HTTPBearer()

# Секретный ключ для подписи токена
SECRET_KEY = "your-secret-key"

# Время жизни токена (30 минут)
TOKEN_EXPIRATION = timedelta(minutes=30)

# Функция генерации токена
def generate_token(username: str):
    payload = {
        "username": username,
        "exp": datetime.utcnow() + TOKEN_EXPIRATION
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

# Функция проверки валидности токена
def validate_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload.get("username")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


@app.get("/login")
async def login(username: str):
    token = generate_token(username)
    return {"token": token}


@app.get("/protected")
async def protected_route(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    username = validate_token(token)
    return {"message": f"Welcome, {username}! This is a protected route."}



from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

def is_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    # Расшифровка и проверка токена, получение информации о пользователе
    # ...
    # Проверка роли пользователя
    if user.role != 'admin':
        raise HTTPException(status_code=403, detail="Access denied. You must be an admin.")

@app.get("/admin/protected")
async def admin_protected_route(user: User = Depends(is_admin)):
    # Код для доступа к защищенному маршруту для администратора
    # ...
