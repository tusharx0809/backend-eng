package handlers

import (
	"parking-lot-golang/services"
)

type ParkingHandler struct {
	Service *services.ParkingService
}

func NewParkingHandler(
	service *services.ParkingService,
) *ParkingHandler {
	return &ParkingHandler{
		Service: service,
	}
}
