package services

import (
	"parking-lot-golang/repository"
)

type ParkingService struct {
	Repo *repository.ParkingRepository
}

func NewParkingService(
	repo *repository.ParkingRepository,
) *ParkingService {
	return &ParkingService{
		Repo: repo,
	}
}
