package routes

import (
	"net/http"
	"parking-lot-golang/handlers"
)

func RegisterRoutes(mux *http.ServeMux, handler *handlers.ParkingHandler) {
	mux.HandleFunc("POST /createdbstructure", handler.CreateDBStrucuture)
}
