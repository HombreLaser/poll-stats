from .base_factory import BaseFactory
from src.database.models import Question
from src.database import db
from src.tests.utils.factories import FormFactory
from factory.faker import faker
import factory
import random


def create_options():
    fake = faker.Faker()
    options = []

    for i in range(5):
        options.append({
            'content': fake.sentence(nb_words=3), 'score': round(random.uniform(0, 100), ndigits=3)
        })

    return options


class QuestionFactory(BaseFactory):
    class Meta:
        sqlalchemy_session = db.session
        model = Question

    type = 'selection'
    content = factory.Faker('sentence', nb_words=3)
    options = create_options()
    score = random.uniform(0, 100)
    form = factory.SubFactory(FormFactory)