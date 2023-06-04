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
            print("Database connected")
        
    except Exception as error:
            print("Connecting to Database failed")
            print("Error:", error)


@app.on_event("shutdown")
async def shutdown():
    try:
        async with engine.begin() as conn:
            await conn.close()
            print("Database disconnected") 
                
        # async with await get_db() as db:
        #     await db.disconnect()
        #     print("Database disconnected")

    except Exception as error:
            print("Disconnecting from Database failed")
            print("Error:", error) 


@app.get("/")
def root():
    return {"message": "Welcome to test task API"}

app.include_router(files_process.router)
app.include_router(user.router)