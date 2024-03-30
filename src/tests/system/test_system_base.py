from flask import session
from src.tests import TestBase



class TestSystemBase(TestBase):
    def login():
        if defined(self.user):
            session['user_id'] = self.user.id
            session['user_role'] = self.user.role