from selenium import webdriver
import pytest


@pytest.fixture
def driver():
    options = webdriver.FirefoxOptions()
    #options.add_argument('-headless')
    driver = webdriver.Firefox(options=options)

    yield driver

    driver.close()