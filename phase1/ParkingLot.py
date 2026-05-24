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

class ParkingLot:
    def __init__(self, floors, parkings_per_floors):
        self.floors = floors
        self.parkings_per_floors = parkings_per_floors

        self.slots = [
            [None for _ in range(parkings_per_floors)]
            for _ in range(floors)
        ]

    def enterVehicle(self, license_plate):
        total_slots = self.floors * self.parkings_per_floors

        for i in range(total_slots):
            floor = i // self.parkings_per_floors
            slot = i % self.parkings_per_floors

            if self.slots[floor][slot] is None:
                self.slots[floor][slot] = license_plate
                return

        print("Parking Lot Full")  


def main():
    pass

if __name__ == "__main__":
    main()