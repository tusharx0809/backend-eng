package repository

import (
	"context"
	"fmt"
	"strconv"
	"time"

	"github.com/jackc/pgx/v5"
)

func (r *ParkingRepository) ExitVehicle(licensplate string) (bool, string, float32, float32) {
	var total_floors int

	get_total_floors_query := `SELECT floors FROM parking_lot_config`

	err := r.DB.QueryRow(
		context.Background(),
		get_total_floors_query,
	).Scan(&total_floors)

	if err != nil {
		return false, err.Error(), 0.00, 0.00
	}

	var vehicletype string
	var entry_time time.Time
	var entry_date time.Time
	var exit_time time.Time
	var charges float32
	var minutesparked float32

	current_floor := 0

	for i := current_floor; i < total_floors; i++ {
		table_name := "floor_" + strconv.Itoa(i)

		fetch_query := fmt.Sprintf(
			`
			SELECT vehicle_type, entry_time, entry_date, NOW()::timestamp as exit_time,
            ROUND((EXTRACT(EPOCH FROM (SELECT NOW() - entry_time FROM %s WHERE license_plate = '%s')) / 60)::numeric, 2) as minutesparked from %s WHERE license_plate = '%s'		
		`, table_name, licensplate, table_name, licensplate,
		)

		err := r.DB.QueryRow(
			context.Background(),
			fetch_query,
		).Scan(&vehicletype, &entry_time, &entry_date, &exit_time, &minutesparked)

		if err != nil {
			continue
		} else {

			if vehicletype == "Car" {
				charges = minutesparked * 0.50
			} else {
				charges = minutesparked * 0.25
			}

		}

		remove_vehicle_query := fmt.Sprintf(
			`UPDATE %s
			SET license_plate=null,vehicle_type=null,entry_time=null,entry_date=null,is_occupied=False WHERE license_plate='%s'`,
			table_name, licensplate,
		)

		insert_into_history_query :=
			`INSERT INTO history(license_plate,entry_date,entry_time,exit_time,charges)
			 VALUES($1,$2,$3,$4,$5)
			`

		tx, err := r.DB.BeginTx(context.Background(), pgx.TxOptions{})

		if err != nil {
			return false, err.Error(), 0.00, 0.00
		}
		defer tx.Rollback(context.Background())

		_, err = tx.Exec(context.Background(), remove_vehicle_query)

		if err != nil {
			return false, err.Error(), 0.00, 0.00
		}

		_, err = tx.Exec(context.Background(), insert_into_history_query, licensplate, entry_date, entry_time, exit_time, charges)

		if err != nil {
			return false, err.Error(), 0.00, 0.00
		}

		if err := tx.Commit(context.Background()); err != nil {
			return false, err.Error(), 0.00, 0.00
		}
		message := "Vehicle " + licensplate + " unparked"
		return true, message, charges, minutesparked

	}

	return false, "Vehicle not found", 0.00, 0.00
}
