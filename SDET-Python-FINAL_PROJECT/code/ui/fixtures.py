import os
import shutil

import pytest
import allure

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver import FirefoxOptions

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from ui.pages.base_page import BasePage
from ui.pages.authorization_page import AuthorizationPage
from ui.pages.registration_page import RegistrationPage
from ui.pages.main_page import MainPage


class UnsupportedBrowserType(Exception):
    pass


@pytest.fixture
def base_page(driver, config):
    return BasePage(driver=driver, config=config)


@pytest.fixture
def authorization_page(driver, config):
    return AuthorizationPage(driver=driver, config=config)


@pytest.fixture
def registration_page(driver, config):
    return RegistrationPage(driver=driver, config=config)


@pytest.fixture
def main_page(driver, config):
    return MainPage(driver=driver, config=config)


def get_driver(config):
    browser_name = config['browser']
    selenoid = config['selenoid']
    vnc = config['vnc']

    if browser_name == 'chrome':
        options = ChromeOptions()

        if selenoid is not None:
            caps = {'browserName': browser_name,
                    'version': '90.0',
                    'sessionTimeout': '2m',
                    'additionalNetworks': ['myapp-net'],
                    }

            if vnc:
                caps['version'] += '_vnc'
                caps['enableVNC'] = True

            browser = webdriver.Remote(selenoid + '/wd/hub', options=options, desired_capabilities=caps)

        else:
            manager = ChromeDriverManager(version='latest')
            browser = webdriver.Chrome(executable_path=manager.install(), options=options)

    elif browser_name == 'firefox':
        options = FirefoxOptions()

        if selenoid is not None:
            caps = {'browserName': browser_name,
                    'version': '88.0',
                    'sessionTimeout': '2m',
                    'additionalNetworks': ['myapp-net']
                    }

            if vnc:
                caps['version'] += '_vnc'
                caps['enableVNC'] = True

            browser = webdriver.Remote(selenoid + '/wd/hub', options=options, desired_capabilities=caps)

        else:
            manager = GeckoDriverManager(version='latest', log_level=0)
            browser = webdriver.Firefox(executable_path=manager.install(), options=options)
    
    else:
        raise UnsupportedBrowserType(f'Unsupported browser {browser_name}')
    
    return browser


@pytest.fixture(scope='function')
def driver(config):
    host = config['app_host']
    port = config['app_port']

    url = f'http://{host}:{port}'

    browser = get_driver(config)

    browser.get(url)
    browser.maximize_window()
    yield browser
    browser.quit()


@pytest.fixture(scope='function', autouse=False)
def ui_report(driver, request, test_dir):
    failed_tests_count = request.session.testsfailed
    yield
    if request.session.testsfailed > failed_tests_count:
        screenshot_file = os.path.join(test_dir, 'failure.png')
        driver.get_screenshot_as_file(screenshot_file)
        allure.attach.file(screenshot_file, 'failure.png', attachment_type=allure.attachment_type.PNG)

        browser_logfile = os.path.join(test_dir, 'browser.log')
        with open(browser_logfile, 'w') as f:
            for i in driver.get_log('browser'):
                f.write(f"{i['level']} - {i['source']}\n{i['message']}\n\n")
        
        with open(browser_logfile, 'r') as f:
           allure.attach(f.read(), 'browser.log', attachment_type=allure.attachment_type.TEXT)