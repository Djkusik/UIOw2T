import sqlite3


class Database:
    def __init__(self, db_name: str) -> None:
        self.conn = sqlite3.connect(db_name)

    def get_conn(self):
        return self.conn
