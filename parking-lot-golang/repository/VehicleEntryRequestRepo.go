package repository

import (
	"context"
	"errors"
	"fmt"
	"strconv"

	"github.com/jackc/pgx/v5"
)

func (r *ParkingRepository) GetTotalOccupied() (int, error) {
	var total_floors int

	get_total_floors := `SELECT floors FROM parking_lot_config`

	err := r.DB.QueryRow(
		context.Background(),
		get_total_floors,
	).Scan(&total_floors)

	if err != nil {
		return -1, err
	}

	var total_occupied int
	for floor := 0; floor < total_floors; floor++ {
		var current_floor_occupied int = 0
		table_name := "floor_" + strconv.Itoa(floor)

		query := fmt.Sprintf(
			`SELECT count(license_plate) from %s
			`, table_name,
		)

		err := r.DB.QueryRow(
			context.Background(),
			query,
		).Scan(&current_floor_occupied)

		if err != nil {
			return -1, err
		}
		total_occupied += current_floor_occupied
	}
	return total_occupied, nil
}

func (r *ParkingRepository) EnterVehicle(licensePlate string, vehicleType string, floor int, parking_number int) (bool, error) {
	table_name := "floor_" + strconv.Itoa(floor)
	var total_parkings int

	get_total_parkings_query := `SELECT floors*parkings_per_floor FROM parking_lot_config`

	err := r.DB.QueryRow(
		context.Background(),
		get_total_parkings_query,
	).Scan(&total_parkings)

	total_occupied, err := r.GetTotalOccupied()

	if total_occupied == -1 {
		return false, err
	}

	if total_parkings == total_occupied {
		return false, errors.New("Parking lot completely occupied")
	}

	var is_occupied bool
	check_query := fmt.Sprintf(
		`SELECT is_occupied FROM %s WHERE parking_number = $1`, table_name,
	)

	err = r.DB.QueryRow(
		context.Background(),
		check_query,
		parking_number,
	).Scan(&is_occupied)

	if err != nil {
		return false, err
	}

	if is_occupied {
		return false, errors.New("Parking Already occupied, please try somewhere else")
	}

	update_query := fmt.Sprintf(
		`
		UPDATE %s
		SET license_plate = $1, vehicle_type = $2, entry_time = NOW(), entry_date = CURRENT_DATE, is_occupied = $3
		WHERE parking_number = $4
	`, table_name,
	)

	tx, err := r.DB.BeginTx(context.Background(), pgx.TxOptions{})

	if err != nil {
		return false, err
	}

	defer tx.Rollback(context.Background())

	_, err = tx.Exec(context.Background(), update_query, licensePlate, vehicleType, true, parking_number)

	if err != nil {
		return false, err
	}

	if err := tx.Commit(context.Background()); err != nil {
		return false, err
	}

	return true, nil

}
