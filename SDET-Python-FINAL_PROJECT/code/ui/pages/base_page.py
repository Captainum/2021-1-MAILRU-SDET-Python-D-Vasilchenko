
import logging
import time

import allure

from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from ui.locators.pages_locators import BasePageLocators
from utils.decorators import wait

CLICK_RETRY = 5
BASE_TIMEOUT = 5

logger = logging.getLogger('test')

class PageNotLoadedException(Exception):
    pass

class BasePage(object):
    locators = BasePageLocators()    

    def __init__(self, driver, config):
        self.driver = driver
        self.config = config

        host = config['app_host']
        port = config['app_port']
        self.url = f'http://{host}:{port}/'

        assert self.is_opened()

        logger.debug(f'{self.__class__.__name__} initialized')

    def is_opened(self, url=None):
        if (url == None):
            url = self.url
        
        logger.info(f'{self.__class__.__name__} page is opening {url}...')

        with allure.step(f'Open {url}'):
            def _check_url():
                if self.driver.current_url != url:
                    raise PageNotLoadedException(
                        f'{url} did not opened in {BASE_TIMEOUT} for {self.__class__.__name__}.\n'
                        f'Current url: {self.driver.current_url}.')
                return True
            return wait(_check_url, error=PageNotLoadedException, check=True, timeout=BASE_TIMEOUT, interval=0.1)

    @allure.step('Looking for {locator}')
    def find(self, locator, timeout=None):
        logger.debug(f'Looking for {locator} with timeout={timeout}')
        
        return self.wait(timeout).until(EC.presence_of_element_located(locator))
    
    @property
    def action_chains(self):
        return ActionChains(self.driver)

    def wait(self, timeout=None):
        if timeout is None:
            timeout = BASE_TIMEOUT
        return WebDriverWait(self.driver, timeout=timeout)

    def scroll_to(self, element):
        logger.debug(f'Scrolling')
        
        self.driver.execute_script('arguments[0].scrollIntoView(true);', element)

    @allure.step('Clicking on {locator}')
    def click(self, locator, timeout=None):
        for i in range(CLICK_RETRY):
            logger.debug(f'Clicking on {locator}. Try {i+1} of {CLICK_RETRY}...')
            
            try:
                element = self.find(locator, timeout)
                element = self.wait(timeout).until(EC.element_to_be_clickable(locator))
                element.click()
                return
            except StaleElementReferenceException:
                if i == CLICK_RETRY - 1:
                    raise