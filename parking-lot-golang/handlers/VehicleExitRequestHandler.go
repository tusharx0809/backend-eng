package handlers

import (
	"encoding/json"
	"net/http"
	"parking-lot-golang/models"
)

func (h *ParkingHandler) ExitVehicle(
	w http.ResponseWriter,
	r *http.Request,
) {
	var req models.VehicleExitRequest
	err := json.NewDecoder(r.Body).Decode(&req)

	if err != nil {
		w.WriteHeader(http.StatusBadRequest)
		json.NewEncoder(w).Encode(
			models.VehicleExitResponse{
				Success:       false,
				Message:       err.Error(),
				LicensePlate:  "",
				Charges:       0.00,
				MinutesParked: 0.00,
			},
		)
		return
	}
	success, message, charges, minutes := h.Service.ExitVehicle(req.LicensePlate)

	if !success {
		w.WriteHeader(http.StatusInternalServerError)
		json.NewEncoder(w).Encode(
			models.VehicleExitResponse{
				Success:       success,
				Message:       message,
				LicensePlate:  req.LicensePlate,
				Charges:       0.00,
				MinutesParked: 0.00,
			},
		)
		return
	}

	w.WriteHeader(http.StatusOK)

	json.NewEncoder(w).Encode(
		models.VehicleExitResponse{
			Success:       success,
			Message:       message,
			LicensePlate:  req.LicensePlate,
			Charges:       charges,
			MinutesParked: minutes,
		},
	)
	return

}
