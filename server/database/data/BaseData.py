from database.Database import Database


class BaseData:
    def __init__(self):
        db = Database()
        self.cursor = db.cursor
        self.conn = db.conn
