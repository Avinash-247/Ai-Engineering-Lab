
import sqlite3


class SessionStorage:
    def __init__(self, db_path="database.db"):
        self.db_path = db_path
        self.create_table()

    def create_table(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS user_sessions (
                    user_id TEXT PRIMARY KEY,
                    session_id TEXT
                )
            """)

    def get_session(self, user_id):
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT session_id FROM user_sessions WHERE user_id = ?",
                (user_id,)
            ).fetchone()

        return row[0] if row else None

    def create_user(self, user_id):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR IGNORE INTO user_sessions (user_id, session_id) VALUES (?, NULL)",
                (user_id,)
            )

    def save_session(self, user_id, session_id):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                UPDATE user_sessions
                SET session_id = ?
                WHERE user_id = ?
            """, (session_id, user_id))
