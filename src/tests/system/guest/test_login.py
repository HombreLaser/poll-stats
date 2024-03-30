from src.tests.system import TestSystemBase
from selenium.webdriver.common.by import By
from flask import url_for
from src.tests.utils.factories import UserAccountFactory
import pytest


class TestLogin(TestSystemBase):
    def test_correct_login(self, server, db, driver):
        user = UserAccountFactory()
        user.password = 'safe_password'
        user.activated = True
        db.session.add(user)
        db.session.commit()
        driver.get(f"http://localhost:8888{url_for('sessions_controller.new')}")
        email_field = driver.find_element(By.ID, 'email')
        password_field = driver.find_element(By.ID, 'password')
        email_field.send_keys(user.email)
        password_field.send_keys('safe_password')
        driver.find_element(By.ID, 'login_button').click()
        assert 'Dashboard' in driver.page_source