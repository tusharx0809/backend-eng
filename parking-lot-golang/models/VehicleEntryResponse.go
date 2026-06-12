package models

import "time"

type VehiceEntryResponse struct {
	success   bool       `json:"success"`
	message   string     `json:"message"`
	timestamp *time.Time `json:"timestamp"`
}
