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
    async def enterVehicle(self, parking_entry_request: ParkingEntryRequest, connection: PostgresConnectionPool) -> ParkingEntryResponse:
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
                print("Parking Lot Full!")
                return ParkingEntryResponse(
                    success=False,
                    status="failed",
                    message="Parking Lot Full!",
                    timestamp=datetime.now().isoformat()
                )
            
        
            check_query: str = f"""
                SELECT license_plate from floor_{parking_entry_request.floor} WHERE parking_number = $1
                """                  
            query: str = f"""
                UPDATE floor_{parking_entry_request.floor} 
                SET license_plate = $1, vehicle_type = $2, entry_time = NOW(), entry_date = CURRENT_DATE, is_occupied = $3
                WHERE parking_number = $4
            """
            async with connection.transaction():
                
                license_plate = await connection.fetchval(
                    check_query,
                    parking_entry_request.parking_number
                )

                if license_plate is not None:
                    return ParkingEntryResponse(
                        success=False,
                        status="failed",
                        message=f"Parking Number: {parking_entry_request.parking_number} at floor: {parking_entry_request.floor} already taken",
                        timestamp=datetime.now().isoformat()
                    )
                        
                
                await connection.execute(
                    query,
                    parking_entry_request.license_plate,
                    f"{parking_entry_request.vehicle_type[0].capitalize()}{parking_entry_request.vehicle_type[1:len(parking_entry_request.vehicle_type)]}",
                    True,
                    parking_entry_request.parking_number
                )
                return ParkingEntryResponse(
                    success=True,
                    status="success",
                    message=f"Vehice: {parking_entry_request.vehicle_type} parked at number: {parking_entry_request.parking_number}, floor: {parking_entry_request.floor}",
                    timestamp=datetime.now().isoformat()
                )
                
        except Exception as e:
            return ParkingEntryResponse(
                success=True,
                status=f"failed: {e}",
                message=f"{traceback.format_exc()}",
                timestamp=datetime.now().isoformat()
            )            


    async def exitVehicle(self, parking_exit_request: ParkingExitRequest, connection: PostgresConnectionPool) -> ParkingExitResponse:
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
                    ROUND((EXTRACT(EPOCH FROM (SELECT NOW() - entry_time FROM floor_{current_floor} WHERE license_plate = '{parking_exit_request.license_plate}')) / 60)::numeric, 2) as minutes from floor_{current_floor} WHERE license_plate = $1""",
                    parking_exit_request.license_plate
                )
                
                if row is None:
                    current_floor = current_floor + 1
                    if current_floor == self.floors-1:
                        return ParkingExitResponse(
                            success=False,
                            message="Vehicle Not found",
                            license_plate="",
                            charges=0.00,
                            minutes_parked=0.00
                        )
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
                            parking_exit_request.license_plate
                        )
                    return ParkingExitResponse(
                        success=True,
                        message="Vehicle Unparked",
                        license_plate=parking_exit_request.license_plate,
                        charges=charges,
                        minutes_parked=row['minutes']
                    )
                        
                    
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