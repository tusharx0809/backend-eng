from datetime import datetime
from db_manager import DatabaseConnection
from models.ParkingLot import ParkingLot
import os

def main():
    with DatabaseConnection.PostgresConnection(os.getenv("DATABASE")) as connection:
        try:
            parking_lot = ParkingLot(4,15,connection)
            print("Parking Lot on database created")
        except connection.OperationalError as e:
            print("Error: {e}")
    

if __name__ == "__main__":
    main()