from db_manager.DatabaseConnection import PostgresConnectionPool
from contextlib import asynccontextmanager
from models.ParkingLot import ParkingLot
from fastapi import FastAPI

FLOORS = 4
PARKINGS_PER_FLOOR = 10
pg_pool = PostgresConnectionPool("ParkingLot", min_size=2, max_size=20)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await pg_pool.initialize_pool()

    app.state.db_pool = pg_pool

    parking_lot: ParkingLot = ParkingLot(FLOORS,PARKINGS_PER_FLOOR)

    async with pg_pool as connection_pool:
        await parking_lot.initialize_schema(connection_pool)

    app.state.parking_lot = parking_lot

    yield

    await pg_pool.close_pool()
