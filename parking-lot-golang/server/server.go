package server

import (
	"net/http"
	"parking-lot-golang/handlers"
	"parking-lot-golang/routes"
)

func StartServer(handler *handlers.ParkingHandler) *http.Server {
	mux := http.NewServeMux()

	routes.RegisterRoutes(mux, handler)

	return &http.Server{
		Addr:    ":8080",
		Handler: mux,
	}
}
