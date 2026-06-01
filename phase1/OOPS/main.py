from datetime import datetime
from db_manager import DatabaseConnection
from models.ParkingLot import ParkingLot
from models.Bike import Bike
from models.Car import Car
from models.Vehicle import Vehicle
import os

def main():
    with DatabaseConnection.PostgresConnection(os.getenv("DATABASE")) as connection:
        try:
            parking_lot = ParkingLot(4,15,connection)
            print("Parking Lot on database created")
            
            # vehicles = [
            #     Car("HRO3K4061"),
            #     Bike("HRO3V0478"),
            #     Car("DL3CAY8821"),
            #     Bike("MH12RN4509"),
            #     Car("KA03MM1142"),
            #     Bike("HR26CT8831"),
            #     Car("UP16BL0054"),
            #     Bike("DL1SAB7710"),
            #     Car("GJ01RE2290"),
            #     Bike("KA51X3311"),
            #     Car("MH02EF5567"),
            #     Bike("UP32JZ4482"),
            #     Car("WB02N8819"),
            #     Bike("GJ03AW9950"),
            #     Car("TS07HK1102"),
            #     Bike("HR03AB1234")
            # ]

            # Loop through the list to enter each vehicle automatically
            # for vehicle in vehicles:
            #     parking_lot.enterVehicle(vehicle, connection)
            #     print(f"{vehicle.get_vehicle_type()} [{vehicle.license_plate}] entered successfully.")

            parking_lot.exitVehicle(Car("UP16BL0054"), connection)

        except connection.OperationalError as e:
            print("Error: {e}")
    

if __name__ == "__main__":
    main()