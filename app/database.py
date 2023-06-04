from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.utils import load_config

config  = load_config()

user = config["database"]["user"]
password = config["database"]["password"]
host = config["database"]["host"]
port = config["database"]["port"]
database = config["database"]["database"]


DATABASE_URL = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"
engine = create_async_engine(DATABASE_URL)

Async_session = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

Base = declarative_base()


async def get_db():
    async with Async_session() as db:
        yield db
