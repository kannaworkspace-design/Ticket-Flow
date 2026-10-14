from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db import make_pool
from app.routers import events,bookings


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pool = await make_pool()
    yield
    await app.state.pool.close()
    
app = FastAPI(lifespan=lifespan)
app.include_router(events.router)
app.include_router(bookings.router)