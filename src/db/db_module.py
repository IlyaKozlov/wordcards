import datetime
import uuid

from db.db_abc import Database


class TaskDatabase(Database):

    def __init__(self):
        super().__init__(db_name="taskdb")

    def _create_tables(self):
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
