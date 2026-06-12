package handlers

import (
	"parking-lot-golang/repository"
)

type ParkingHandler struct {
	Repo *repository.ParkingRepository
}

func NewParkingHandler(
	repo *repository.ParkingRepository,
) *ParkingHandler {
	return &ParkingHandler{
		Repo: repo,
	}
}
