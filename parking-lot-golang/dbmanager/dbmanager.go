package dbmanager

import (
	"context"
	"fmt"
	"os"
	"time"

	"github.com/jackc/pgx/v5/pgxpool"
)

func DBmanager(connection_string string) (*pgxpool.Pool, error) {

	pool, err := pgxpool.New(context.Background(), connection_string)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Unable to create connection pool: %v\n", err)
		return nil, err
	}
	pintCtx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	if err := pool.Ping(pintCtx); err != nil {
		pool.Close()
		return nil, err
	}

	return pool, nil
}
