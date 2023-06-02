from fastapi import FastAPI
import databases
import sqlalchemy

# Параметры подключения к базе данных
DATABASE_URL = "postgresql://username:password@localhost/database_name"

app = FastAPI()

# Создание объекта базы данных
database = databases.Database(DATABASE_URL)

# Создание объекта метаданных для моделей
metadata = sqlalchemy.MetaData()


# Определение модели данных
users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("email", sqlalchemy.String),
)


@app.on_event("startup")
async def connect_to_database():
    # Подключение к базе данных при запуске приложения
    await database.connect()


@app.on_event("shutdown")
async def disconnect_from_database():
    # Отключение от базы данных при остановке приложения
    await database.disconnect()


@app.get("/users")
async def get_users():
    # Выполнение запроса к базе данных
    query = users.select()
    return await database.fetch_all(query)


@app.post("/users")
async def create_user(name: str, email: str):
    # Выполнение запроса на создание пользователя
    query = users.insert().values(name=name, email=email)
    await database.execute(query)
    return {"message": "User created successfully"}
