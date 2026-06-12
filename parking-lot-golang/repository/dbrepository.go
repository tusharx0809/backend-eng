package repository

import (
	"github.com/jackc/pgx/v5/pgxpool"
)

type ParkingRepository struct {
	DB *pgxpool.Pool
}

func NewParkingRepository(
	db *pgxpool.Pool,
) *ParkingRepository {
	return &ParkingRepository{
		DB: db,
	}
}
