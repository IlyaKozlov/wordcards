import logging
from pathlib import Path
import sqlite3
import uuid
import time


class LLMCache:

    def __init__(self):
        self.db_filename = (
            Path(__file__).parent.parent.parent / "db" / "llm_cache.sqlite"
        )
        self.create_table()
        self.logger = logging.getLogger(__name__)

    def create_table(self):
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS cache (
                    uid TEXT PRIMARY KEY,
                    cache TEXT,
                    ts INTEGER
                )
            """
            )
            conn.commit()

    def put(self, key: uuid.UUID, value: str):
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            ts = int(time.time())
            cursor.execute(
                """
                INSERT INTO cache (uid, cache, ts) VALUES (?, ?, ?)
                ON CONFLICT(uid)
                DO UPDATE SET cache = excluded.cache, ts = excluded.ts
            """,
                (str(key), value, int(ts)),
            )
            conn.commit()

    def get(self, key: uuid.UUID) -> str:
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT cache FROM cache WHERE uid = ?",
                (str(key),),
            )
            row = cursor.fetchone()
            if row:
                ts = int(time.time())
                cursor.execute(
                    "UPDATE cache SET ts = ? WHERE uid = ?",
                    (str(key), ts),
                )
                self.logger.info(f"Found in cache {key}")
            else:
                self.logger.info(f"Not found in cache {key}")
            return row[0] if row else None

    def clear(self, max_storage_time: float):
        threshold_time = time.time() - max_storage_time
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM cache WHERE ts < ?",
                (threshold_time,),
            )
            conn.commit()
            self.logger.info("Clear old cache")
