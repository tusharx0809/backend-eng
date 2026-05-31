from . import Vehicle

class ParkingLot:
    def __init__(self, floors, parkings_per_floors):
        self.floors = floors
        self.parkings_per_floors = parkings_per_floors

        self.slots = [
            [None for _ in range(parkings_per_floors)]
            for _ in range(floors)
        ]

    def enterVehicle(self, vehicle: Vehicle):
        total_slots = self.floors * self.parkings_per_floors

        for i in range(total_slots):
            floor = i // self.parkings_per_floors
            slot = i % self.parkings_per_floors

            if self.slots[floor][slot] is None:
                self.slots[floor][slot] = vehicle
                return

        print("Parking Lot Full") 

    def removeVehicle(self, vehicle: Vehicle):
        total_slots = self.floors * self.parkings_per_floors

        for i in range(total_slots):
            floor = i // self.parkings_per_floors
            slot = i % self.parkings_per_floors

            if self.slots[floor][slot] == vehicle:
                self.slots[floor][slot] = None
                print(Vehicle.get_vehicle_type(self), vehicle.license_plate, "left the parking lot")
                return
            
    def printParkingLot(self):
        for i in range(self.floors):
            print("Ground Floor" if i == 0 else f"Floor Number: {i}")
            for j in range(self.parkings_per_floors):
                if self.slots[i][j] == None:                    
                    print(f"Parking Number {j+1}: Empty Parking")
                else:
                    v = self.slots[i][j]
                    print("Parking Number",j+1,":",v.license_plate)
            print("\n")