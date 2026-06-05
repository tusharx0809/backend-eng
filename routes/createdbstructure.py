from fastapi import APIRouter, HTTPException, Request
from schemas.CreateDBStructureRequest import ParkitLotStructureRequest, ParkingLotStructureResponse
from models.ParkingLot import ParkingLot
from typing import Dict,Any

router = APIRouter()

@router.post("/createDBStructure", response_model=ParkingLotStructureResponse)
async def createDBStrucutre(structure: ParkitLotStructureRequest, request: Request) -> Dict[str,Any]:
    db_pool= request.app.state.db_pool

    current_lot: ParkingLot = ParkingLot(structure.floors, structure.number_of_parkings)

    async with db_pool as db_connection:
        response = await current_lot.initialize_schema(db_connection)

    if not response.success:
        raise HTTPException(
            status_code=400,
            detail={
                "success": response.success,
                "message": response.message
            }
        )

    return response