package server

import (
	"net/http"
	"parking-lot-golang/handlers"
)

func StartServer() *http.Server {
	mux := http.NewServeMux()

	handlers.RegisterRoutes(mux)

	server := &http.Server{
		Addr:    ":8080",
		Handler: mux,
	}

	return server
}
