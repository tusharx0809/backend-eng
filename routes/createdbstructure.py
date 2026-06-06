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
        response: list = await current_lot.initialize_schema(db_connection)

    if not response[0]:
        raise HTTPException(
            status_code=400,
            detail={
                "success": response[0],
                "message": response[1]
            }
        )

    return ParkingLotStructureResponse(
        success=response[0],
        message=response[1]
    )