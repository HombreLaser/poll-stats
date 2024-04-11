from builtins import Exception
from src.tests import TestBase
from src.database import db


class TestModelBase(TestBase):
    def create(self, record):
        try:
            db.session.add(record)
            db.commit()

            return record
        except Exception as error:
            db.session.rollback()
            return None