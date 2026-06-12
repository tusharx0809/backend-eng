package main

import (
	"fmt"
	"log"
	"os"
	"parking-lot-golang/dbmanager"
	"parking-lot-golang/handlers"
	"parking-lot-golang/repository"
	"parking-lot-golang/server"

	"github.com/joho/godotenv"
)

func main() {
	err := godotenv.Load()

	if err != nil {
		log.Fatal("Error loading .env file")
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

	repo := repository.NewParkingRepository(pool)

	handler := handlers.NewParkingHandler(repo)

	server := server.StartServer(handler)
	fmt.Println("Server running on :8080")
	server_error := server.ListenAndServe()

	if server_error != nil {
		log.Fatal(server_error)
	}

}
