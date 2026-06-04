from pydantic import BaseModel

class Vehicle(BaseModel):
    license_plate: str
    def get_vehicle_type(self) -> str:
        return self.__class__.__name__

