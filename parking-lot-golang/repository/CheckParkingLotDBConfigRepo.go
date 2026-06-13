package repository

import (
	"context"
)

func (r *ParkingRepository) ParkingLotConfigExists() bool {
	check_parking_lot_config_query := `
		SELECT EXISTS (
			SELECT 1
			FROM pgtables
			WHERE schemaname='public'
			AND tablename = 'parking_lot_config'
		)
	`
	var exists bool

	err := r.DB.QueryRow(
		context.Background(),
		check_parking_lot_config_query,
	).Scan(&exists)

	if err != nil {
		return false
	}
	return exists

}
