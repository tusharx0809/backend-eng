package routes

import (
	"fmt"
	"net/http"
	"parking-lot-golang/handlers"
)

func RegisterRoutes(mux *http.ServeMux, handler *handlers.ParkingHandler) {
	mux.HandleFunc("/hello", helloHandler)
	mux.HandleFunc("/health", healthHandler)
}

func helloHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintln(w, "Hello from server")
}

func healthHandler(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
	fmt.Fprintln(w, "OK")
}
