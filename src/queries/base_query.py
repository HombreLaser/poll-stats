from src.database import db


class BaseQuery:
    def __init__(self):
        self.session = db.session