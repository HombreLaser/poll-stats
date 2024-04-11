from .base_factory import BaseFactory
from src.database.models import Form
from src.database import db
from src.tests.utils.factories import UserAccountFactory
import factory
import secrets
import random


class FormFactory(BaseFactory):
    class Meta:
        sqlalchemy_session = db.session
        model = Form

    name = factory.Faker('sentence', nb_words=5)
    status = random.choice(['review', 'open', 'closed'])
    public_key = secrets.token_hex(12)
    author = factory.SubFactory(UserAccountFactory)