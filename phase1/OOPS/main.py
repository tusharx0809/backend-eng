from datetime import datetime
from models.ParkingLot import ParkingLot
from models.Bike import Bike
from models.Car import Car
from models.Vehicle import Vehicle
from fastapi import FastAPI, HTTPException, Request
from typing import Any,Dict
from models.ParkingEntryRequest import ParkingEntryRequest, ParkingEntryResponse
from models.ParkingExitRequest import ParkingExitRequest
from lifespan import lifespan


ParkingApp = FastAPI(lifespan=lifespan)

@ParkingApp.post("/enterVehicle", response_model=ParkingEntryResponse)
async def enterVehice(payload: ParkingEntryRequest, request: Request) -> Dict[str,Any]:
    current_lot: ParkingLot = request.app.state.parking_lot
    db_pool = request.app.state.db_pool

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


    async with db_pool as db_connection:
        if await current_lot.checkParkinglot(db_connection):
            raise HTTPException(status_code=400, detail="Parking Lot Full")
        
        response: ParkingEntryResponse = await current_lot.enterVehicle(
            vehicle=vehicle,
            floor=floor,
            parking_number=parking_number,
            connection=db_connection
        )

        if not response.success:
            raise HTTPException(
                status_code=400,
                detail=response.message
            )
        
        return response


@ParkingApp.put("/exitVehicle")
async def exitVehice(payload: ParkingExitRequest, request: Request) -> Dict[str,Any]:
    vehicle = Vehicle(license_plate=payload.license_plate)
    current_lot: ParkingLot = request.app.state.parking_lot

    db_pool = request.app.state.db_pool
    
    async with db_pool as db_connection:
        result = await current_lot.exitVehicle(vehicle, db_connection)

    if result is None:
        raise HTTPException(
            status_code=404, 
            detail=f"Vehicle with license plate {payload.license_plate} not found in the parking lot."
        )
    
    return result