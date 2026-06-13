package models

type DBStrucutreRequest struct {
	NumberOfFloors   int `json:"number_of_floors"`
	NumberOfParkings int `json:"number_of_parkings"`
}
