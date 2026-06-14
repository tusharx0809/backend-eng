package models

type VehicleEntryRequest struct {
	LicensePlate  string `json:"license_plate"`
	VehicleType   string `json:"vehicle_type"`
	Floor         int    `json:"floor"`
	ParkingNumber int    `json:"parking_number"`
}
