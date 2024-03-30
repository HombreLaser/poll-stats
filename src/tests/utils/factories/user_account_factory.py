from .base_factory import BaseFactory
from src.database.models import UserAccount
from src.database import db
import secrets
import factory


class UserAccountFactory(BaseFactory):
    class Meta():
        sqlalchemy_session = db.session
        model = UserAccount

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('ascii_free_email')