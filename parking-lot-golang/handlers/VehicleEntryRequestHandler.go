package handlers

import (
	"encoding/json"
	"net/http"
	"parking-lot-golang/models"
	"strconv"
	"time"
)

func TimePtr(t time.Time) *time.Time {
	return &t
}

func (h *ParkingHandler) EnterVehicle(
	w http.ResponseWriter,
	r *http.Request,
) {
	var req models.VehicleEntryRequest

	err := json.NewDecoder(r.Body).Decode(&req)

	if err != nil {
		w.WriteHeader(http.StatusBadRequest)
		json.NewEncoder(w).Encode(
			models.VehiceEntryResponse{
				Success:   false,
				Message:   err.Error(),
				Timestamp: TimePtr(time.Now()),
			},
		)
		return
	}

	_, err = h.Service.EnterVehicle(req.LicensePlate, req.VehicleType, req.Floor, req.ParkingNumber)

	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		json.NewEncoder(w).Encode(
			models.VehiceEntryResponse{
				Success:   false,
				Message:   err.Error(),
				Timestamp: TimePtr(time.Now()),
			},
		)
		return
	}
	message := "Parked at floor: " + strconv.Itoa(req.Floor) + ", number: " + strconv.Itoa(req.ParkingNumber)

	w.WriteHeader(http.StatusCreated)

	json.NewEncoder(w).Encode(
		models.VehiceEntryResponse{
			Success:   true,
			Message:   message,
			Timestamp: TimePtr(time.Now()),
		},
	)

}
