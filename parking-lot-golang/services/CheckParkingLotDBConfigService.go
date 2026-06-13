package services

func (s *ParkingService) CreateDBStrucuture() bool {
	exists := s.Repo.ParkingLotConfigExists()
	return exists
}
