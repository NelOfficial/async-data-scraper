import aiosqlite
import logging
from typing import List
from core.schemas import ParsedItem
from config import settings

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

class AsyncDatabase:
    def __init__(self, db_path: str = settings.DB_PATH):
        self.db_path = db_path

    async def init_db(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    title TEXT,
                    body TEXT
                )
            """)
            await db.commit()
            logging.info("db init")

    async def save_items(self, items: List[ParsedItem]):
        async with aiosqlite.connect(self.db_path) as db:
            for item in items:
                await db.execute(
                    "INSERT OR REPLACE INTO items (id, user_id, title, body) VALUES (?, ?, ?, ?)",
                    (item.id, item.user_id, item.title, item.body)
                )
            await db.commit()
            logging.info(f"saved to base: {len(items)}")