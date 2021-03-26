import pytest
from selenium import webdriver
from ui.pages.base_page import BasePage
from ui.pages.main_page import MainPage

@pytest.fixture
def base_page(driver):
    return BasePage(driver=driver)

@pytest.fixture
def main_page(driver, config):
    return MainPage(driver=driver, config=config)

@pytest.fixture(scope='function')
def driver(config):
    url = config['url']
    browser = webdriver.Chrome(executable_path='/home/captainum/python/chromedriver')
    browser.maximize_window()
    browser.get(url)
    yield browser
    browser.close()
