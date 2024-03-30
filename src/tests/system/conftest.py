from selenium import webdriver
from src.tests.utils.factories import UserAccountFactory
import pytest
import secrets


@pytest.fixture
def user(request, db):
    user = UserAccountFactory.build()
    user.password = secrets.token_hex(8)
    user.activated = True
    if request.param:
        user.role = request.param

    db.session.add(user)
    db.session.commit()

    yield user



@pytest.fixture
def driver():
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    driver = webdriver.Firefox(options=options)

    yield driver

    driver.close()