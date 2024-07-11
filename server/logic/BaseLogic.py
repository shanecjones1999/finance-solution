from database.Connection import Session


class BaseLogic:
    def __init__(self):
        self.session = Session()
