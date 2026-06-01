from .Vehicle import Vehicle
from db_manager.DatabaseConnection import PostgresConnection
from decimal import Decimal

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
                "vehicle_type VARCHAR(50),"
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

            cursor.execute(
                f"CREATE TABLE IF NOT EXISTS History ("
                "id_number SERIAL PRIMARY KEY,"
                "license_plate VARCHAR(100),"
                "entry_date DATE,"
                "entry_time TIMESTAMP,"
                "exit_time TIMESTAMP,"
                "charges DECIMAL(10,2))"
            )

    def enterVehicle(self, vehicle: Vehicle, connection: PostgresConnection):
        cursor = connection.cursor()
        max_parking_number = None
        current_floor = 0
        while max_parking_number is None and current_floor < self.floors:
            cursor.execute(
                f"SELECT min(parking_number) from floor_{current_floor} WHERE license_plate IS NULL"
            )

            max_parking_number = cursor.fetchone()[0]
            if max_parking_number is None:
                current_floor = current_floor + 1
        
        if current_floor + 1 == self.floors and max_parking_number is None:
            print("PARKING LOT FULL")
            return
        else:
            query = f"""
                UPDATE floor_{current_floor} 
                SET license_plate = %s, vehicle_type = %s, entry_time = NOW(), entry_date = CURRENT_DATE
                WHERE parking_number = {max_parking_number}
            """

            cursor.execute(
                query,
                (vehicle.license_plate,vehicle.get_vehicle_type())
            )
            
                      


    def exitVehicle(self, vehicle: Vehicle, connection: PostgresConnection):
        license_plate = None
        entry_time = None
        exit_time = None
        entry_date = None
        charges = None
        current_floor = 0
        cursor = connection.cursor()
        while license_plate is None and current_floor < self.floors:
            cursor.execute(
                f"""SELECT license_plate, entry_time, entry_date, NOW(),
                ROUND((EXTRACT(EPOCH FROM (SELECT NOW() - entry_time FROM floor_{current_floor} WHERE license_plate = '{vehicle.license_plate}')) / 60)::numeric, 2) as minutes from floor_{current_floor} WHERE license_plate = '{vehicle.license_plate}'"""
            )
            row = cursor.fetchone()
            if row is None:
                current_floor = current_floor + 1
            else:
                license_plate = row[0]
                entry_time = row[1]
                entry_date = row[2]
                exit_time = row[3]
                rate = Decimal('0.50') if vehicle.get_vehicle_type() == 'Car' else Decimal('0.25')
                charges = row[4] * rate

                query = f"""INSERT INTO History(license_plate, entry_date, entry_time, exit_time, charges)
                            VALUES(%s,%s,%s,%s,%s)"""
                cursor.execute(
                    query,
                    (license_plate, entry_date, entry_time, exit_time, charges,)
                )

                query = f"""UPDATE floor_{current_floor}
                            SET license_plate = NULL, vehicle_type = NULL, entry_time = NULL, entry_date = NULL
                            WHERE license_plate = %s;
                        """
                cursor.execute(
                    query,
                    (vehicle.license_plate,)
                )
                

            
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