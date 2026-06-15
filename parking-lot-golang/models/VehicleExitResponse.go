package models

type VehicleExitResponse struct {
	Success       bool    `json:"success"`
	Message       string  `json:"message"`
	LicensePlate  string  `json:"licenseplate"`
	Charges       float32 `json:"charges"`
	MinutesParked float32 `json:"minutesparked"`
}
