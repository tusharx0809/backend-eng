from datetime import datetime
from models.ParkingLot import ParkingLot
from fastapi import FastAPI, HTTPException, Request
from typing import Any,Dict
from schemas.ParkingEntryRequest import ParkingEntryRequest, ParkingEntryResponse
from schemas.ParkingExitRequest import ParkingExitRequest, ParkingExitResponse
from lifespan import lifespan


ParkingApp = FastAPI(lifespan=lifespan)

@ParkingApp.post("/enterVehicle", response_model=ParkingEntryResponse)
async def enterVehice(payload: ParkingEntryRequest, request: Request) -> Dict[str,Any]:
    current_lot: ParkingLot = request.app.state.parking_lot
    db_pool = request.app.state.db_pool

    if payload.floor < 0 or payload.floor >= current_lot.floors:
        raise HTTPException(status_code=400, detail="Invalid parking!")
    

    if payload.vehicle_type.strip().lower() not in ["car","bike"]:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid vehicle_type '{payload.vehicle_type}'. Must be 'Car' or 'Bike'."
        )    


    async with db_pool as db_connection:
        
        response: ParkingEntryResponse = await current_lot.enterVehicle(
            payload,
            connection=db_connection
        )

        if not response.success:
            raise HTTPException(
                status_code=400,
                detail={
                    "success": response.success,
                    "message": response.message
                }
            )
        
        return response


@ParkingApp.put("/exitVehicle", response_model=ParkingExitResponse)
async def exitVehice(payload: ParkingExitRequest, request: Request) -> Dict[str,Any]:
    current_lot: ParkingLot = request.app.state.parking_lot

    db_pool = request.app.state.db_pool
    
    async with db_pool as db_connection:
        response: ParkingExitResponse = await current_lot.exitVehicle(payload, db_connection)

    if not response.success:
        raise HTTPException(
            status_code=400,
            detail={
                "success":response.success,
                "message":response.message
            }
        )
    
    return response
    