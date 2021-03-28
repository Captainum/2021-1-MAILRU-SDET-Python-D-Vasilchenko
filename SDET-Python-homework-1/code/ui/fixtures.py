import pytest
from selenium import webdriver
from ui.pages.base_page import BasePage
from ui.pages.main_page import MainPage
from ui.pages.dashboard_page import DashboardPage
from ui.pages.contacts_page import ContactsPage

from ui.locators.pages_locators import MainPageLocators

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

@pytest.fixture
def base_page(driver):
    return BasePage(driver=driver)

@pytest.fixture
def main_page(driver, config):
    return MainPage(driver=driver, config=config)

@pytest.fixture
def dashboard_page(driver_logined):
    return DashboardPage(driver=driver_logined)

@pytest.fixture
def contacts_page(driver_logined):
    return ContactsPage(driver=driver_logined)

@pytest.fixture(scope='function')
def driver(config):
    url = config['url']
    browser = webdriver.Chrome(executable_path='/home/captainum/python/chromedriver')
    browser.maximize_window()
    browser.get(url)
    yield browser
    browser.close()

@pytest.fixture(scope='function')
def driver_logined(config):
    url = config['url']
    login = config['login']
    password = config['password']

    browser = webdriver.Chrome(executable_path='/home/captainum/python/chromedriver')
    browser.maximize_window()
    browser.get(url)

    main_page = MainPage(browser, config)
    main_page.login()

    yield browser
    browser.close()
