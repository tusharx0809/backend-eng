from fastapi import FastAPI
from lifespan import lifespan
from routes.entervehicle import router as enter_vehicle_router
from routes.exitvehicle import router as exit_vehicle_router
from routes.createdbstructure import router as create_db_structure

ParkingApp = FastAPI(lifespan=lifespan)

ParkingApp.include_router(create_db_structure)
ParkingApp.include_router(enter_vehicle_router)
ParkingApp.include_router(exit_vehicle_router)



    