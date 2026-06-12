package models

type VehicleEntryRequest struct {
	licensePlate  string `json:"licenseplate"`
	vehicleType   string `json:"vehicletype"`
	floor         int    `json:"floor"`
	parkingNumber int    `json:"parkingnumber"`
}
