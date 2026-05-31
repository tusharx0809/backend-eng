from datetime import datetime
from db_manager import DatabaseConnection
from models.ParkingLot import ParkingLot
import os

def main():
    parking_lot = ParkingLot(5, 20)
    with DatabaseConnection.PostgresConnection(os.getenv("DATABASE")) as connection:
        with connection.cursor() as cursor:
            cursor.execute("select * from test")
            print(cursor.fetchone())

    

if __name__ == "__main__":
    main()