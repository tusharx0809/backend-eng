from pydantic import BaseModel

class ParkingEntryRequest(BaseModel):
    license_plate: str
    vehicle_type: str
    floor: int
    parking_number: int