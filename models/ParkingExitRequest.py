from pydantic import BaseModel

class ParkingExitRequest(BaseModel):
    license_plate: str

class ParkingExitResponse(BaseModel):
    success: bool
    message: str
    license_plate: str
    charges: float
    minutes_parked: float