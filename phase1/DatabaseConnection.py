import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

class PostgresConnection:
    def __init__(self):
        pass

    def connectToServer(self, connection_string):
        connection = psycopg2.connect(connection_string)
        connection.autocommit = True
        return connection
