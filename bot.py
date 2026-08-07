import asyncio
import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import Message
import aiosqlite
from config import settings
from core.fetcher import AsyncFetcher
from core.parser import DataParser
from database.db import AsyncDatabase
from config import settings

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

BOT_TOKEN = settings.BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
db_service = AsyncDatabase(settings.DB_PATH)

@dp.message(Command("start"))
async def cmd_start(message: Message):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="🚀 start"), types.KeyboardButton(text="📊 status")]
        ],
        resize_keyboard=True
    )
    await message.answer(
        "choose option:",
        reply_markup=keyboard
    )

@dp.message(F.text == "📊 status")
async def get_db_status(message: Message):
    async with aiosqlite.connect(db_service.db_path) as db:
        async with db.execute("SELECT COUNT(*) FROM items") as cursor:
            row = await cursor.fetchone()
            count = row[0] if row else 0
    
    await message.answer(f"db status:\n• objects: {count}\n• path: {settings.DB_PATH}")

@dp.message(F.text == "🚀 start")
async def run_scraping(message: Message):
    await message.answer("init of async collection...")
    
    try:
        urls = [f"https://jsonplaceholder.typicode.com/posts/{i}" for i in range(1, 11)]
        fetcher = AsyncFetcher(
            max_concurrent_requests=settings.MAX_CONCURRENT_REQUESTS, 
            timeout_seconds=settings.TIMEOUT_SECONDS
        )
        await db_service.init_db()
        
        raw_data = await fetcher.fetch_all(urls)
        valid_raw = [item for item in raw_data if isinstance(item, dict)]
        clean_items = DataParser.parse_batch(valid_raw)
        await db_service.save_items(clean_items)
        
        await message.answer(f"completed. processed and saved: {len(clean_items)} objs")
    except Exception as e:
        logging.error(f"сбой в боте: {e}")
        await message.answer("critical error")

async def main():
    logging.info("starting tg bot...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())