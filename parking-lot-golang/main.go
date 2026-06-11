package main

import (
	"fmt"
	"log"
	"os"
	"parking-lot-golang/dbmanager"

	"github.com/joho/godotenv"
)

func main() {
	err := godotenv.Load()

	if err != nil {
		log.Fatal("Error loading .env file")
		return
	}

	//fmt.Println(os.Getenv("PORT"))

	var connection_string string = "postgres://" + os.Getenv("USER") + ":" + os.Getenv("PASSWORD") + "@localhost:" + os.Getenv("PORT") + "/ParkingLot?sslmode=disable"
	//fmt.Println(connection_string)
	pool, err := dbmanager.DBmanager(connection_string)
	if err != nil {
		log.Fatal(err)
	}
	defer pool.Close()

	fmt.Println("Connection successful!")
}
