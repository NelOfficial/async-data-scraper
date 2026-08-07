# async data scraper & REST API core

a high-performance, asynchronous data collection and management pipeline built with **FastAPI**, **aiohttp**, and **Pydantic v2**

designed with modular architecture, strict type validation, and non-blocking I/O operations for commercial-grade scraping and data storage

## architecture & key features

- **asynchronous data ingestion (`aiohttp` + `asyncio`):** efficiently handles concurrent HTTP requests controlled by semaphores to prevent rate-limiting and connection overload
- **data integrity & schema validation (`Pydantic v2`):** strict runtime validation of incoming json payloads with alias mapping and error isolation
- **asynchronous storage (`aiosqlite`):** non-blocking sqlite database integration using connection pooling and async cursors
- **RESTful management interface (`FastAPI`):** auto-generated OpenAPI (Swagger) documentation, background task processing, and lifespan state management

## project structure

```
├── config.py         # environment variables & setting management
├── core/
│   ├── fetcher.py    # async HTTP fetcher with rate limiting
│   ├── pasrser.py    # pydantic parsing and validation layer
│   └── schemas.py    # pydantic data schemas
├── database/
│   └── db.py         # async SQLite controller
├── api/
│   └── endpoints.py  # fastAPI router & endpoint definitions
└── main.py           # application entry point & lifespan context
```

## quick start

1. clone the repository:
```git clone [https://github.com/NelOfficial/async-data-scraper.git](https://github.com/NelOfficial/async-data-scraper.git)
cd async-data-scraper
```

2. set up virtual environment & install dependencies:
```
python -m venv venv
source venv/bin/activate  # on windows: venv\Scripts\activate
pip install fastapi uvicorn aiohttp pydantic pydantic-settings aiosqlite
```

3. run api server:
```
python main.py
```

4. access swagger ui:
```
open http://127.0.0.1:8000/docs in your browser to trigger background scraping tasks and inspect stored data
```

5. (optional) telegram connection
```
create bot https://t.me/BotFather and put token in .env
```
