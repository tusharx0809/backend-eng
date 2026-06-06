from db_manager.DatabaseConnection import PostgresConnectionPool
from decimal import Decimal
import traceback
from schemas.ParkingEntryRequest import ParkingEntryRequest, ParkingEntryResponse
from schemas.ParkingExitRequest import ParkingExitRequest, ParkingExitResponse
from schemas.CreateDBStructureRequest import ParkitLotStructureRequest, ParkingLotStructureResponse
from datetime import datetime

class ParkingLot:
    def __init__(self, floors: int, parkings_per_floor: int):
        self.floors: int = floors
        self.parkings_per_floors: int = parkings_per_floor

    async def initialize_schema(self, connection) -> ParkingLotStructureResponse:
        try:
            
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
                await connection.execute(
                    f"CREATE TABLE IF NOT EXISTS parking_lot_config ("
                    "    id INTEGER PRIMARY KEY,"
                    "    floors INTEGER NOT NULL,"
                    "    parkings_per_floor INTEGER NOT NULL,"
                    "    created_at TIMESTAMP DEFAULT NOW()"
                    ");"
                )
                await connection.execute("""
                    INSERT INTO parking_lot_config (
                        id,
                        floors,
                        parkings_per_floor
                    )
                    VALUES (1, $1, $2)
                    ON CONFLICT (id)
                    DO UPDATE SET
                        floors = EXCLUDED.floors,
                        parkings_per_floor = EXCLUDED.parkings_per_floor
                """,
                self.floors,
                self.parkings_per_floors)
            return ParkingLotStructureResponse(
                success=True,
                message="Database strucutre created..."
            )
        except Exception as e:
            return ParkingLotStructureResponse(
                success=False,
                message=traceback.format_exc()
            )
    async def enterVehicle(self, license_plate: str, vehicle_type: str, floor: int, parking_number: int, connection: PostgresConnectionPool) -> list[bool, str]:
        try:
            parkings_occupied: int = 0
            total_parkings: int = self.floors * self.parkings_per_floors
            current_floor: int = 0
            while current_floor < self.floors:
                count = await connection.fetchval(
                    f"SELECT count(license_plate) FROM floor_{current_floor}"
                )
                parkings_occupied += count
                current_floor += 1
            if parkings_occupied == total_parkings:
                return [False,"Parking Lot Full.."]
            
        
            check_query: str = f"""
                SELECT license_plate from floor_{floor} WHERE parking_number = $1
                """                  
            query: str = f"""
                UPDATE floor_{floor} 
                SET license_plate = $1, vehicle_type = $2, entry_time = NOW(), entry_date = CURRENT_DATE, is_occupied = $3
                WHERE parking_number = $4
            """
            async with connection.transaction():
                
                license_plate_currently_parked = await connection.fetchval(
                    check_query,
                    parking_number
                )

                if license_plate_currently_parked is not None:
                    return [False, f"Parking: {parking_number} at floor: {floor} is already occupied"]
                        
                
                await connection.execute(
                    query,
                    license_plate,
                    f"{vehicle_type[0].capitalize()}{vehicle_type[1:len(vehicle_type)]}",
                    True,
                    parking_number
                )
            return [True,f"Vehicle Parked at numeber: {parking_number}, floor: {floor}"]
                
        except Exception as e:
            return [False,traceback.format_exc()]           


    async def exitVehicle(self, license_plate: str, connection: PostgresConnectionPool) -> list[bool,str,float,float]:
        try:
            license_plate_parked: str = None
            vehicle_type: str = None
            entry_time: str = None
            exit_time: str = None
            entry_date: str = None
            charges: Decimal = None
            current_floor: int = 0
            while license_plate_parked is None and current_floor < self.floors:
                row = await connection.fetchrow(
                    f"""SELECT license_plate, vehicle_type, entry_time, entry_date, NOW()::timestamp as current_now,
                    ROUND((EXTRACT(EPOCH FROM (SELECT NOW() - entry_time FROM floor_{current_floor} WHERE license_plate = '{license_plate}')) / 60)::numeric, 2) as minutes from floor_{current_floor} WHERE license_plate = $1""",
                    license_plate
                )
                
                if row is None:
                    current_floor = current_floor + 1
                    if current_floor == self.floors-1:
                        return [False, f"Vehicle: {license_plate} not found!", 0.00,0.00]
                else:
                    license_plate_parked = row['license_plate']
                    vehicle_type = row['vehicle_type']
                    entry_time = row['entry_time']
                    entry_date = row['entry_date']
                    exit_time = row['current_now']
                    rate = Decimal('0.50') if vehicle_type == 'Car' else Decimal('0.25')
                    charges = row['minutes'] * rate
                    query: str = f"""INSERT INTO History(license_plate, entry_date, entry_time, exit_time, charges)
                                VALUES($1,$2,$3,$4,$5)"""
                    async with connection.transaction():
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
                            license_plate_parked
                        )
                    return [True, f"Vehicle: {license_plate_parked}, left the parking", charges, row['minutes']]
                        
                    
        except Exception as e:
            return [False,traceback.format_exc(),0.00,0.00]
                

            
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