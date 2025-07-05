import sqlite3
import uuid
import datetime


class TaskDatabase:
    def __init__(self, db_name: str = "tasks.db"):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self._create_table()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()  # Commit any changes
        self.connection.close()    # Close the connection

    def _create_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Tasks (
                uid TEXT PRIMARY KEY,
                answer TEXT,
                timestamp DATETIME
            )
            """
        )

    def add_answer(self, answer: str):
        uid = str(uuid.uuid4())  # Generate a new UUID
        timestamp = datetime.datetime.now()  # Get the current timestamp
        self.cursor.execute(
            """
            INSERT INTO Tasks (uid, answer, timestamp)
            VALUES (?, ?, ?)
            """,
            (uid, answer, timestamp),
        )
        return uid  # Return the generated UUID

    def get_answer(self, uid):
        self.cursor.execute(
            """
            SELECT answer FROM Tasks WHERE uid = ?
            """,
            (uid,),
        )
        result = self.cursor.fetchone()
        return result[0] if result else None
