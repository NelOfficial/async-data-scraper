import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from api.endpoints import router as api_router
from database.db import AsyncDatabase

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = AsyncDatabase("parser.db")
    await db.init_db()
    yield

app = FastAPI(
    title="Async Data Scraper API",
    description="High-performance asynchronous parser and REST API core",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)