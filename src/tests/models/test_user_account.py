from src.tests.utils.factories import UserAccountFactory
import factory
import secrets


def test_user_creation(app, db):
    user = UserAccountFactory.build()
    user.password = secrets.token_hex(8)

    db.session.add(user)
    db.session.commit()

    assert user.id is not None


def test_user_verify_password(app, db):
    user = UserAccountFactory.build()
    new_password = secrets.token_hex(16)
    wrong_password = secrets.token_hex(8)
    user.password = new_password

    db.session.add(user)
    db.session.commit()

    assert user.verify_password(new_password) == True
    assert user.verify_password(wrong_password) == False
