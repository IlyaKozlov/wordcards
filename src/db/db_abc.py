import abc
import os
import sqlite3
from pathlib import Path


class Database(abc.ABC):

    def __init__(self, db_name: str):
        self.path = Path(os.getenv("HOME")) / ".wordcards" / "db.sqlite"
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def __enter__(self):
        os.makedirs(self.path.parent, exist_ok=True)
        self.connection = sqlite3.connect(self.path)
        self.cursor = self.connection.cursor()
        self._create_tables()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()  # Commit any changes
        self.connection.close()    # Close the connection

    @abc.abstractmethod
    def _create_tables(self):
        raise NotImplementedError()
