from src.tests.utils.factories import FormFactory
from . import TestModelBase
from sqlalchemy.exc import IntegrityError
import factory
import pytest


class TestForm(TestModelBase):
    def test_form_creation(self, app, db):
        form = FormFactory.build() 
        db.session.add(form)
        db.session.commit()

        form.id is not None

    def test_invalid_form_raises_exception(self, app, db):
        form = FormFactory.build(name=factory.Faker('paragraph', nb_sentences=64))
        # Nombre largo
        assert self.create(form) is None
        # Nombre vacío
        form.name = None
        assert self.create(form) is None