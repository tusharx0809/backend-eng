from .Vehicle import Vehicle
from db_manager.DatabaseConnection import PostgresConnection
from decimal import Decimal
import asyncpg
import traceback

class ParkingLot:
    def __init__(self, floors: int, parkings_per_floors: int):
        self.floors: int = floors
        self.parkings_per_floors: int = parkings_per_floors

    async def initialize_schema(self, connection):
        for floor in range(self.floors):
            table_name: str = f"Floor_{floor}"
            await connection.execute(
                f"CREATE TABLE IF NOT EXISTS {table_name} ("
                "parking_number SERIAL PRIMARY KEY,"
                "license_plate VARCHAR(100),"
                "vehicle_type VARCHAR(50),"
                "entry_time TIMESTAMP," 
                "entry_date DATE,"
                "is_occupied BOOL DEFAULT FALSE)"
            )
            count = await connection.fetchval(f"SELECT count(1) from  {table_name};")
            if count == 0:
                await connection.execute(
                    f"INSERT INTO {table_name} (parking_number)"
                    f"SELECT generate_series(1, $1)",
                    self.parkings_per_floors
                )
            await connection.execute(
                f"CREATE TABLE IF NOT EXISTS History ("
                "id_number SERIAL PRIMARY KEY,"
                "license_plate VARCHAR(100),"
                "entry_date DATE,"
                "entry_time TIMESTAMP,"
                "exit_time TIMESTAMP,"
                "charges DECIMAL(10,2))"
            )
    async def checkParkinglot(self, connection: PostgresConnection) -> bool:
        try:
            parkings_occupied: int = 0
            total_parkings: int = self.floors * self.parkings_per_floors
            current_floor: int = 0
            while current_floor < self.floors:
                count = await connection.execute(
                    f"SELECT count(license_plate) FROM floor_{current_floor}"
                )
                parkings_occupied += count
                current_floor += 1
            if parkings_occupied == total_parkings:
                print("Parking Lot Full!")
                return True
            return False
        except Exception as e:
            print(f"Error: {e}")
            print(traceback.format_exc())
            return False
    async def enterVehicle(self, vehicle: Vehicle, floor: int, parking_number: int, connection: PostgresConnection) -> bool:
        try:                  
            query: str = f"""
                UPDATE floor_{floor} 
                SET license_plate = $1, vehicle_type = $2, entry_time = NOW(), entry_date = CURRENT_DATE, is_occupied = $3
                WHERE parking_number = $4
            """
            await connection.execute(
                query,
                vehicle.license_plate,
                vehicle.get_vehicle_type(),
                True,
                parking_number
            )
            print(f"{vehicle.license_plate} Parked at floor: {floor}, number {parking_number}")
                
            return True
        except Exception as e:
            print(f"Error: {e}")
            print(traceback.format_exc())
            return False             


    async def exitVehicle(self, vehicle: Vehicle, connection: PostgresConnection) -> dict | None:
        try:
            license_plate: str = None
            vehicle_type: str = None
            entry_time: str = None
            exit_time: str = None
            entry_date: str = None
            charges: Decimal = None
            current_floor: int = 0
            while license_plate is None and current_floor < self.floors:
                row = await connection.fetchrow(
                    f"""SELECT license_plate, vehicle_type, entry_time, entry_date, NOW()::timestamp as current_now,
                    ROUND((EXTRACT(EPOCH FROM (SELECT NOW() - entry_time FROM floor_{current_floor} WHERE license_plate = '{vehicle.license_plate}')) / 60)::numeric, 2) as minutes from floor_{current_floor} WHERE license_plate = $1""",
                    vehicle.license_plate
                )
                
                if row is None:
                    current_floor = current_floor + 1
                else:
                    license_plate = row['license_plate']
                    vehicle_type = row['vehicle_type']
                    entry_time = row['entry_time']
                    entry_date = row['entry_date']
                    exit_time = row['current_now']
                    rate = Decimal('0.50') if vehicle_type == 'Car' else Decimal('0.25')
                    charges = row['minutes'] * rate
                    query: str = f"""INSERT INTO History(license_plate, entry_date, entry_time, exit_time, charges)
                                VALUES($1,$2,$3,$4,$5)"""
                    await connection.execute(
                        query,
                        license_plate, 
                        entry_date, 
                        entry_time, 
                        exit_time, 
                        charges
                    )
                    query: str = f"""UPDATE floor_{current_floor}
                                SET license_plate = NULL, vehicle_type = NULL, entry_time = NULL, entry_date = NULL, is_occupied = {False}
                                WHERE license_plate = $1;
                            """
                    await connection.execute(
                        query,
                        vehicle.license_plate
                    )
                    return {
                        "license_plate": license_plate,
                        "charges": float(charges),
                        "minutes_parked": float(row['minutes'])
                    }
        except Exception as e:
            print(f"Error: {e}")
            print(traceback.format_exc())
                

            
    # def printParkingLot(self):
    #     for i in range(self.floors):
    #         print("Ground Floor" if i == 0 else f"Floor Number: {i}")
    #         for j in range(self.parkings_per_floors):
    #             if self.slots[i][j] == None:                    
    #                 print(f"Parking Number {j+1}: Empty Parking")
    #             else:
    #                 v = self.slots[i][j]
    #                 print("Parking Number",j+1,":",v.license_plate)
    #         print("\n")