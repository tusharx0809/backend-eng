import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

class PostgresConnection:
    def __init__(self, db_name: str):
        self.host: str = os.getenv("HOSTNAME")
        self.db_name: str = db_name
        self.username: str = os.getenv("USER")
        self.password: str = os.getenv("PASSWORD")
        self.port:str = os.getenv("PORT")
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