import os
from typing import Optional

import psycopg2
import pandas as pd


class Db:
    def __init__(self, database_uri: Optional[str] = None):
        database_uri = os.environ.get('DATABASE_URI', database_uri)
        assert database_uri, 'DATABASE_URI environment variable not set'

        # Establishing the connection
        self._conn = psycopg2.connect(database_uri)
        self._cursor = self._conn.cursor()

    def query_something(self) -> pd.DataFrame:
        self._cursor.execute("""
            SELECT *
            FROM table_name
        """)
        return pd.DataFrame(self._cursor.fetchall(), columns=['col1', 'col2'])

