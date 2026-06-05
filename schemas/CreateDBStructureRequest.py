from pydantic import BaseModel, Field

class ParkitLotStructureRequest(BaseModel):
    floors: int = Field(gt=0)
    number_of_parkings: int = Field(gt=0)

class ParkingLotStructureResponse(BaseModel):
    success: bool
    message: str