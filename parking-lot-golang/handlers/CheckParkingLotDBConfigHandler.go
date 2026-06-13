package handlers

import (
	"encoding/json"
	"net/http"
	"parking-lot-golang/models"
)

func (h *ParkingHandler) ParkingLotConfigExists(
	w http.ResponseWriter,
	r *http.Request,
) {

	exists := h.Service.CreateDBStrucuture()

	if !exists {
		json.NewEncoder(w).Encode(
			models.DBStructureResponse{
				Success: true,
				Message: "Parking lot configuration exists",
			},
		)
	}
}
