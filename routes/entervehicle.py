from fastapi import APIRouter, HTTPException, Request
from schemas.ParkingEntryRequest import ParkingEntryRequest,ParkingEntryResponse
from typing import Dict, Any
from models.ParkingLot import ParkingLot
from datetime import datetime

router = APIRouter()

@router.post("/enterVehicle", response_model=ParkingEntryResponse)
async def enterVehice(payload: ParkingEntryRequest, request: Request) -> Dict[str,Any]:
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

        if payload.floor < 0 or payload.floor >= current_lot.floors:
            raise HTTPException(status_code=400, detail="Invalid parking!")
    

        if payload.vehicle_type.strip().lower() not in ["car","bike"]:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid vehicle_type '{payload.vehicle_type}'. Must be 'Car' or 'Bike'."
            )

        response: list = await current_lot.enterVehicle(
            license_plate=payload.license_plate,
            vehicle_type=payload.vehicle_type,
            floor=payload.floor,
            parking_number=payload.parking_number,
            connection=db_connection
        )

        if not response[0]:
            raise HTTPException(
                status_code=400,
                detail={
                    "success": response[0],
                    "message": response[1]
                }
            )
        
        return ParkingEntryResponse(
            success=response[0],
            message=response[1],
            timestamp=datetime.now().isoformat()
        )