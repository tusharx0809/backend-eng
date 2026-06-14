package services

func (s *ParkingService) EnterVehicle(licensePlate string, vehicleType string, floor int, parkingNumber int) (bool, error) {
	is_parked, err := s.Repo.EnterVehicle(licensePlate, vehicleType, floor, parkingNumber)

	if err != nil {
		return false, err
	}

	return is_parked, nil
}
