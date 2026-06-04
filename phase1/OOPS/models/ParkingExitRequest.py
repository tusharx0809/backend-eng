from pydantic import BaseModel

class ParkingExitRequest(BaseModel):
    license_plate: str