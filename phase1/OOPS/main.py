from datetime import datetime
from db_manager.DatabaseConnection import PostgresConnection
from models.ParkingLot import ParkingLot
from models.Bike import Bike
from models.Car import Car
from models.Vehicle import Vehicle
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from typing import Any,Dict
from models.ParkingEntryRequest import ParkingEntryRequest
from models.ParkingExitRequest import ParkingExitRequest

FLOORS = 4
PARKINGS_PER_FLOOR = 10

pg_connection = PostgresConnection("ParkingLot")
parking_lot = ParkingLot(FLOORS,PARKINGS_PER_FLOOR)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"Creating tables if not existing...")
    try:
        async with pg_connection as db_connection:
            await parking_lot.initialize_schema(db_connection)
        app.state.parking_lot = parking_lot
        print("Database schema created!")
    except Exception as e:
        print(f"Failed to initilize DB: {e}")
        raise e
    yield

ParkingApp = FastAPI(lifespan=lifespan)

@ParkingApp.post("/enterVehicle")
async def enterVehice(payload: ParkingEntryRequest) -> Dict[str,Any]:
    current_lot: ParkingLot = ParkingApp.state.parking_lot

    floor = payload.floor
    parking_number = payload.parking_number

    if floor < 0 or floor >= current_lot.floors:
        raise HTTPException(status_code=400, detail="Invalid parking!")
    
    vehicle_type = payload.vehicle_type.strip().lower()

    if vehicle_type == "car":
        vehicle = Car(license_plate=payload.license_plate)
    elif vehicle_type == "bike":
        vehicle = Bike(license_plate=payload.license_plate)
    else:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid vehicle_type '{payload.vehicle_type}'. Must be 'Car' or 'Bike'."
        )    


    async with pg_connection as db_connection:
        if await current_lot.checkParkinglot(db_connection):
            raise HTTPException(status_code=400, detail="Parking Lot Full")
        
        success = await current_lot.enterVehicle(
            vehicle=vehicle,
            floor=floor,
            parking_number=parking_number,
            connection=db_connection
        )

        if not success:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to occupy {parking_number} on floor {floor}"
            )
        
        return {
            "status":"success",
            "message":f"Vehicle {vehicle.license_plate} parked on floor {floor}",
            "timestamp":datetime.now().isoformat()
        }


@ParkingApp.put("/exitVehicle")
async def exitVehice(payload: ParkingExitRequest) -> Dict[str,Any]:
    vehicle = Vehicle(license_plate=payload.license_plate)
    current_lot: ParkingLot = ParkingApp.state.parking_lot
    
    async with pg_connection as db_connection:
        result = await current_lot.exitVehicle(vehicle, db_connection)

    if result is None:
        raise HTTPException(
            status_code=404, 
            detail=f"Vehicle with license plate {payload.license_plate} not found in the parking lot."
        )
    
    return result