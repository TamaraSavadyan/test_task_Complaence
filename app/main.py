import asyncio
from fastapi import FastAPI
from routers import files_process, user
from database import engine, get_db
from models import Base

app = FastAPI(
    title='Test Task App'
)


@app.on_event("startup")
async def startup():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        async with get_db() as db:
            await db.connect()
            print("Database connected")
        
    except Exception as error:
            print("Connecting to Database failed")
            print("Error:", error)


@app.on_event("shutdown")
async def shutdown():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
            
    async with get_db() as db:
        await db.disconnect()
        print("Database disconnected") 


@app.get("/")
def root():
    return {"message": "Welcome to test task API"}

app.include_router(files_process.router)
app.include_router(user.router)