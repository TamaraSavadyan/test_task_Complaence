from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import yaml


with open("config.yml", "r") as config_file:
    config = yaml.safe_load(config_file)

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
    db = Async_session()
    try:
        yield db
    finally:
        db.close()
