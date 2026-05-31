from . import Vehicle
from db_manager.DatabaseConnection import PostgresConnection

class ParkingLot:
    def __init__(self, floors, parkings_per_floors, connection: PostgresConnection):
        self.floors = floors
        self.parkings_per_floors = parkings_per_floors
        cursor = connection.cursor()
        for floor in range(floors):
            table_name = f"Floor_{floor}"
            cursor.execute(
                f"CREATE TABLE IF NOT EXISTS {table_name} ("
                "parking_number SERIAL PRIMARY KEY,"
                "license_plate VARCHAR(100),"
                "entry_time TIMESTAMP," 
                "entry_date DATE)"
            )
            cursor.execute(f"SELECT count(1) from  {table_name};")
            if cursor.fetchone()[0] == 0:
                cursor.execute(
                    f"INSERT INTO {table_name} (parking_number)"
                    f"SELECT generate_series(1, %s)",
                    (parkings_per_floors,)
                )


    def enterVehicle(self, vehicle: Vehicle, connection: PostgresConnection):
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