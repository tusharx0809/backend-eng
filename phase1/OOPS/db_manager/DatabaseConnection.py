import os
import asyncpg
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

    async def __aenter__(self):
        try:
            self.connection = await asyncpg.connect(
                host=self.host,
                database=self.db_name,
                user=self.username,
                password=self.password,
                port=self.port
            )
            return self.connection
        except Exception as e:
            print(f"[Connection error] Could not connect to server: {e}")
            raise
        except:
            print(f"[Interface Error] Database interface failure: {e}")
            raise

    async def __aexit__(self, exc_type, exc, tb):
        if self.connection:
            await self.connection.close()