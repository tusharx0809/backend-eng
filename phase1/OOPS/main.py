from datetime import datetime
from db_manager import DatabaseConnection
from models.ParkingLot import ParkingLot
from models.Bike import Bike
from models.Car import Car
from models.Vehicle import Vehicle
import os
import random

def main():
    with DatabaseConnection.PostgresConnection(os.getenv("DATABASE")) as connection:
        try:
            parking_lot = ParkingLot(4,15,connection)
            print("Parking Lot on database created")
            
            # vehicles: list = [
            #         Car(f"CAR{i:04d}") for i in range(30)
            #     ] + [
            #         Bike(f"BIKE{i:04d}") for i in range(30)
            #     ]

            # if not parking_lot.checkParkinglot(connection):
            # # Loop through the list to enter each vehicle automatically
            #     for vehicle in vehicles:
            #         parking_lot.enterVehicle(vehicle, connection)
            # else:
            #     return

            parking_lot.exitVehicle(Car("HR03K4061"), connection)
            

        except connection.OperationalError as e:
            print("Error: {e}")
    

if __name__ == "__main__":
    main()