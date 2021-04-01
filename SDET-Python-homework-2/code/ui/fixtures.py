import os
import shutil

#import allure
import pytest
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from ui.pages.base_page import BasePage
from ui.pages.main_page import MainPage

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

class UnsupportedBrowserType(Exception):
    pass

@pytest.fixture
def base_page(driver):
    return BasePage(driver=driver)

@pytest.fixture
def main_page(driver, config):
    return MainPage(driver=driver, config=config)

@pytest.fixture
def dashboard_page(driver):
    return DashboardPage(driver=driver)

def get_driver(browser_name, download_dir):
    if browser_name == 'chrome':
        options = ChromeOptions()
        options.add_experimental_option("prefs", {"download.default_directory": download_dir})

        manager = ChromeDriverManager(version='latest', log_level=0)
        browser = webdriver.Chrome(executable_path=manager.install(), options=options)
    
    elif browser_name == 'firefox':
        manager = GeckoDriverManager(version='latest', log_level=0)
        browser = webdriver.Firefox(executable_path=manager.install())
    
    else:
        raise UnsupportedBrowserType(f'Unsupported browser {browser_name}')
    
    return browser

@pytest.fixture(scope='function')
def driver(config, test_dir):
    url = config['url']
    browser_name = config['browser']

    browser = get_driver(browser_name, download_dir=test_dir)

    browser.get(url)
    browser.maximize_window()
    yield browser
    browser.quit()

@pytest.fixture(scope='function', params=['chrome', 'firefox'])
def all_drivers(config, request, test_dir):
    url = config['url']

    browser = get_driver(request.param, download_dir=test_dir)

    browser.get(url)
    browser.maximize_window()
    yield browser
    browser.quit()

@pytest.fixture(scope='function', autouse=True)
def ui_report(driver, request, test_dir):
    failed_tests_count = request.session.testsfailed
    yield
    if request.session.testsfailed > failed_tests_count:
        screenshot_file = os.path.join(test_dir, 'failure.png')
        driver.get_screenshot_as_file(screenshot_file)
        #allure.attach.file(screenshot_file, 'failure.png', attachment_type=allure.attachment_type.PNG)

        browser_logfile = os.path.join(test_dir, 'browser.log')
        with open(browser_logfile, 'w') as f:
            for i in driver.get_log('browser'):
                f.write(f"{i['level']} - {i['source']}\n{i['message']}\n\n")
        
        #with open(browser_logfile, 'r') as f:
        #    allure.attach(f.read(), 'browser.log', attachment_type=allure.attachment_type.TEXT)