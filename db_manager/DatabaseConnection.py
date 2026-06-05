import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()

class PostgresConnectionPool:
    def __init__(self, db_name: str, min_size: int = 2, max_size: int = 20):
        self.host: str = os.getenv("HOSTNAME")
        self.db_name: str = db_name
        self.username: str = os.getenv("USER")
        self.password: str = os.getenv("PASSWORD")
        self.port:str = os.getenv("PORT")

        self.min_size = min_size
        self.max_size = max_size

        self.connection = None

    async def initialize_pool(self):
        try:
            self.pool = await asyncpg.create_pool(
                host=self.host,
                database=self.db_name,
                user=self.username,
                password=self.password,
                port=self.port,
                min_size=self.min_size,
                max_size=self.max_size
            )
            print(f"Database pool initialized with {self.min_size} warm connections.")
        except Exception as e:
            print(f"Pool connection error!")
            raise
    async def close_pool(self):
        if self.pool:
            await self.pool.close()

    async def __aenter__(self):
        if not self.pool:
            raise RuntimeError(f"Database pool has not been initialized. Call initialize_pool() first.")
        self._connection_context = self.pool.acquire()
        self.connection = await self._connection_context.__aenter__()
        return self.connection

    async def __aexit__(self, exc_type, exc, tb):
        if hasattr(self, '_connection_context'):
            await self._connection_context.__aexit__(exc_type, exc, tb)