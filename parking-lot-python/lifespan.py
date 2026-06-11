from db_manager.DatabaseConnection import PostgresConnectionPool
from contextlib import asynccontextmanager
from models.ParkingLot import ParkingLot
from fastapi import FastAPI

pg_pool = PostgresConnectionPool("ParkingLot", min_size=2, max_size=20)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await pg_pool.initialize_pool()

    app.state.db_pool = pg_pool

    yield

    await pg_pool.close_pool()
