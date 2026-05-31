import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

class PostgresConnection:
    def __init__(self, db_name):
        self.host = os.getenv("HOSTNAME")
        self.db_name = db_name
        self.username = os.getenv("USER")
        self.password = os.getenv("PASSWORD")
        self.port = os.getenv("PORT")
        self.connection = None

    def __enter__(self):
        try:
            connection_string = f"host={self.host} dbname={self.db_name} user={self.username} password={self.password} port={self.port}"
            self.connection = psycopg2.connect(connection_string)
            self.connection.autocommit = True
            return self.connection
        except psycopg2.OperationalError as e:
            print(f"[Connection error] Could not connect to server: {e}")
            raise
        except:
            print(f"[Interface Error] Database interface failure: {e}")
            raise

    def __exit__(self, exc_type, exc, tb):
        if self.connection:
            self.connection.close()