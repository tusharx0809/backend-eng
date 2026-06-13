package handlers

import (
	"encoding/json"
	"net/http"
	"parking-lot-golang/models"
)

func (h *ParkingHandler) CreateDBStrucuture(
	w http.ResponseWriter,
	r *http.Request,
) {
	var req models.DBStrucutreRequest

	err := json.NewDecoder(r.Body).Decode(&req)

	if err != nil {
		w.WriteHeader(http.StatusBadRequest)

		json.NewEncoder(w).Encode(
			models.DBStructureResponse{
				Success: false,
				Message: err.Error(),
			},
		)
		return
	}

	_, err = h.Service.CreateDBStrucuture(req.NumberOfFloors, req.NumberOfParkings)

	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		json.NewEncoder(w).Encode(
			models.DBStructureResponse{
				Success: false,
				Message: err.Error(),
			},
		)
		return
	}
	w.WriteHeader(http.StatusCreated)

	json.NewEncoder(w).Encode(
		models.DBStructureResponse{
			Success: true,
			Message: "Parking Lot Created Successfully",
		},
	)
}
