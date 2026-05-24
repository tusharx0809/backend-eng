from datetime import datetime

class Vehicle:
    def __init__(self, license_plate):
        self.license_plate = license_plate

    def get_vehicle_type(self):
        return self.__class__.__name__

class Car(Vehicle):
    pass
class Bike(Vehicle):
    pass


def main():
    pass

if __name__ == "__main__":
    main()