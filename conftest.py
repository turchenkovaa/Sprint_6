import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from helpers.data import Urls


@pytest.fixture
def driver():
    driver = webdriver.Firefox()
    driver.get(Urls.BASE_URL)
    yield driver
    driver.quit()



# Для корректного отображения аргументов в параметризированном тесте
def pytest_make_parametrize_id(val):
    return repr(val)