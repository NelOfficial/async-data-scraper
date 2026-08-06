from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Optional
import aiosqlite
from core.schemas import ParsedItem
from core.fetcher import AsyncFetcher
from core.parser import DataParser
from database.db import AsyncDatabase
from config import settings

router = APIRouter(prefix="/api/v1", tags=["parser"])
db_service = AsyncDatabase(settings.DB_PATH)

@router.get("/items", response_model=List[ParsedItem])
async def get_all_items(limit: int = 50, offset: int = 0):
    async with aiosqlite.connect(db_service.db_path) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT id, user_id as userId, title, body FROM items LIMIT ? OFFSET ?",
            (limit, offset)
        ) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

@router.get("/items/{item_id}", response_model=ParsedItem)
async def get_item_by_id(item_id: int):
    async with aiosqlite.connect(db_service.db_path) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT id, user_id as userId, title, body FROM items WHERE id = ?",
            (item_id,)
        ) as cursor:
            row = await cursor.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="объект не найден в базе")
            return dict(row)

async def _background_parse_task(count: int):
    urls = [f"https://jsonplaceholder.typicode.com/posts/{i}" for i in range(1, count + 1)]
    fetcher = AsyncFetcher(max_concurrent_requests=5, timeout_seconds=5)
    await db_service.init_db()
    
    raw_data = await fetcher.fetch_all(urls)
    valid_raw = [item for item in raw_data if isinstance(item, dict)]
    clean_items = DataParser.parse_batch(valid_raw)
    await db_service.save_items(clean_items)

@router.post("/parse/run")
async def trigger_parsing(background_tasks: BackgroundTasks, count: int = 20):
    if count < 1 or count > 100:
        raise HTTPException(status_code=400, detail="from 1 to 100")
    
    background_tasks.add_task(_background_parse_task, count)
    return {"status": "ok", "message": f"task {count} objects has been launched in bg"}