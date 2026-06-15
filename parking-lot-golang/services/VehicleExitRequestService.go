package services

func (s *ParkingService) ExitVehicle(licenseplate string) (bool, string, float32, float32) {
	success, message, charges, minutes := s.Repo.ExitVehicle(licenseplate)

	if !success {
		return false, message, charges, minutes
	}

	return success, message, charges, minutes
}
