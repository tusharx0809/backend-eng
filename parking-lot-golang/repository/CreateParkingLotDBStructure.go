package repository

import (
	"context"
	"fmt"
	"strconv"
)

func (r *ParkingRepository) ParkingLotConfigExists() bool {
	check_parking_lot_config_query := `
		SELECT EXISTS (
			SELECT 1
			FROM pg_tables
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

func (r *ParkingRepository) ParkingLotDBStructCreate(
	numberofFloors int,
	numberofParkings int,
) (bool, error) {
	config_query := `
		CREATE TABLE IF NOT EXISTS parking_lot_config (
            id INTEGER PRIMARY KEY,
            floors INTEGER NOT NULL,
            parkings_per_floor INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT NOW()
        );
		`
	_, err := r.DB.Exec(
		context.Background(),
		config_query,
	)
	if err != nil {
		return false, err
	}

	insert_config_query :=
		`
		INSERT INTO parking_lot_config (
            id,
            floors,
            parkings_per_floor
        )
        VALUES (1, $1, $2)
        ON CONFLICT (id)
        DO UPDATE SET
         floors = EXCLUDED.floors,
        parkings_per_floor = EXCLUDED.parkings_per_floor
		`
	_, err = r.DB.Exec(
		context.Background(),
		insert_config_query,
		numberofFloors,
		numberofParkings,
	)

	if err != nil {
		return false, err
	}

	for i := 0; i < numberofFloors; i++ {
		table_name := "floor_" + strconv.Itoa(i)

		query := fmt.Sprintf(
			`			
				CREATE TABLE IF NOT EXISTS %s (
					parking_number SERIAL PRIMARY KEY,
					license_plate VARCHAR(100),
					vehicle_type VARCHAR(50),
					entry_time TIMESTAMP,
					entry_date DATE,
					is_occupied BOOL DEFAULT FALSE)			
		`, table_name,
		)

		_, err := r.DB.Exec(
			context.Background(),
			query,
		)
		if err != nil {
			return false, err
		}
	}
	return true, nil
}
