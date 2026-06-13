package services

import "errors"

func (s *ParkingService) CreateDBStrucuture(numberofFloors int, numberofParkings int) (bool, error) {
	if s.Repo.ParkingLotConfigExists() {
		return false, errors.New(
			"parking lot configuration already exists",
		)
	}

	_, err := s.Repo.ParkingLotDBStructCreate(
		numberofFloors,
		numberofParkings,
	)

	if err != nil {
		return false, err
	}

	return true, nil
}
