from fastapi import APIRouter, HTTPException, Request
from schemas.ParkingExitRequest import ParkingExitRequest, ParkingExitResponse
from typing import Dict, Any
from models.ParkingLot import ParkingLot

router = APIRouter()

@router.put("/exitVehicle", response_model=ParkingExitResponse)
async def exitVehice(payload: ParkingExitRequest, request: Request) -> Dict[str,Any]:
    db_pool = request.app.state.db_pool


    async with db_pool as db_connection:
        row = await db_connection.fetchrow("""
                SELECT floors, parkings_per_floor
                FROM parking_lot_config
                WHERE id = 1
            """)

        if row is None:
            raise HTTPException(
                status_code=400,
                detail={
                    "success": False,
                    "message": "Strucutre not initialized..."
                }
            )

        current_lot = ParkingLot(
            row['floors'],
            row['parkings_per_floor']
        )
    
    async with db_pool as db_connection:
        response: list = await current_lot.exitVehicle(payload.license_plate, db_connection)

    if not response[0]:
        raise HTTPException(
            status_code=400,
            detail={
                "success":response[0],
                "message":response[1]
            }
        )
    
    return ParkingExitResponse(
        success=response[0],
        message=response[1],
        license_plate=payload.license_plate,
        charges=response[2],
        minutes_parked=response[3]
    )