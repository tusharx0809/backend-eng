from pydantic import BaseModel, Field
from datetime import datetime

class ParkingEntryRequest(BaseModel):
    license_plate: str = Field(None, min_length=4)
    vehicle_type: str
    floor: int
    parking_number: int

class ParkingEntryResponse(BaseModel):
    success: bool
    message: str
    timestamp: datetime
