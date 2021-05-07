import os
import shutil

import pytest
from appium import webdriver

from ui.capability import capability_select

from ui.pages.base_page import BasePage
from ui import pages


class UnsupportedBrowserType(Exception):
    pass


@pytest.fixture
def base_page(driver, config):
    return BasePage(driver=driver, config=config)


@pytest.fixture
def main_page(driver, config):
    page = get_page(config['device_os'], 'MainPage')
    return page(driver=driver, config=config)


@pytest.fixture
def settings_page(driver, config):
    page = get_page(config['device_os'], 'SettingsPage')
    return page(driver=driver, config=config)


@pytest.fixture
def news_sources_page(driver, config):
    page = get_page(config['device_os'], 'NewsSourcesPage')
    return page(driver=driver, config=config)


@pytest.fixture
def about_page(driver, config):
    page = get_page(config['device_os'], 'AboutPage')
    return page(driver=driver, config=config)


def get_page(device, page_class):
    if device == 'android':
        page_class += 'ANDROID'
    page = getattr(pages, page_class, None)
    if page is None:
        raise Exception(f'No such page {page_class}')
    return page


def get_driver(device_os, appium_url=None, apk_path=None):
    if device_os == 'android':
        desired_caps = capability_select(device_os, apk_path)
        driver = webdriver.Remote(appium_url, desired_capabilities=desired_caps)
        return driver
    else:
        raise UnsupportedBrowserType(f'Unsupported device_os type {device_os}')


@pytest.fixture(scope='function')
def driver(config, repo_root):
    device_os = config['device_os']
    appium_url = config['appium']
    apk_path = os.path.join(repo_root, config['apk_path'])
    driver = get_driver(device_os, appium_url, apk_path)
    yield driver
    driver.quit()