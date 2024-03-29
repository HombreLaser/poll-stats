from src.tests.system import TestSystemBase
from flask import url_for
import pytest


@pytest.mark.usefixtures('live_server')
class TestLogin(TestSystemBase):
    def test_correct_login(app, driver, live_server):
        driver.get(f"http://localhost:8888{url_for('sessions_controller.new')}")
        assert 'Login' in driver.page_source