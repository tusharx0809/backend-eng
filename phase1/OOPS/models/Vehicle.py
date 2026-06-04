class Vehicle:
    def __init__(self, license_plate):
        self.license_plate: str = license_plate

    def get_vehicle_type(self):
        return self.__class__.__name__

