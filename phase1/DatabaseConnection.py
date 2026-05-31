import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

class PostgresConnection:
    def __init__(self):
        pass

    def connectToServer(self, connection_string):
        connection = None
        try:
            connection = psycopg2.connect(connection_string)
            connection.autocommit = True
            return connection
        except psycopg2.OperationalError as e:
            print(f"[Connection Error] Could not connect to server: {e}")
            return connection
        except psycopg2.InterfaceError as e:
            print(f"[Interface Error] Database interface failure: {e}")
            return connection