from .Vehicle import Vehicle

class Car(Vehicle):
    def __init__(self, license_plate):
        super().__init__(license_plate)
