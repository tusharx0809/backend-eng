package models

import "time"

type VehiceEntryResponse struct {
	Success   bool       `json:"success"`
	Message   string     `json:"message"`
	Timestamp *time.Time `json:"timestamp"`
}
