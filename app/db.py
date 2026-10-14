import asyncpg

from app.config import DATABASE_URL

async def make_pool():
    return await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=10)