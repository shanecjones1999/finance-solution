import sqlite3


class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.initialize_database()
        return cls._instance

    def initialize_database(self):
        self.conn = sqlite3.connect('db.db')
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        # Create tables or perform other initialization tasks here

    @staticmethod
    def initialize():
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            created_at_utc TEXT NOT NULL,
            updated_at_utc TEXT NOT NULL
        )
        ''')

        conn.commit()
        conn.close()

    def terminate_connection(self):
        if not self.conn.closed:
            self.conn.close()
