from src.tests.utils.factories import UserAccountFactory
from sqlalchemy.exc import IntegrityError
from . import TestModelBase
import pytest
import factory
import secrets


class TestUserAccount(TestModelBase):
    def test_user_creation(app, db):
        user = UserAccountFactory.build()
        user.password = secrets.token_hex(8)

        db.session.add(user)
        db.session.commit()

        assert user.id is not None


    def test_user_verify_password(app, db):
        user = UserAccountFactory.build()
        password = secrets.token_hex(16)
        wrong_password = secrets.token_hex(8)
        user.password = password

        db.session.add(user)
        db.session.commit()

        assert user.verify_password(password) == True
        assert user.verify_password(wrong_password) == False


    def test_invalid_user_raises_exception(app, db):
        user = UserAccountFactory(email=None, first_name=None, last_name=None)

        with pytest.raises(IntegrityError):
            db.session.add(user)
            db.session.commit()
        
        db.session.rollback()