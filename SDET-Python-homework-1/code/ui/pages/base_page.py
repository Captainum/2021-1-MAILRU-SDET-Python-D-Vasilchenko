from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

class BasePage(object):
    def __init__(self, driver):
        self.driver = driver

    def find(self, locator, timeout=None):
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    def wait(self, timeout=None):
        if timeout is None:
            timeout = 5
        return WebDriverWait(self.driver, timeout=timeout)

    def click(self, locator, timeout=None):
        element = self.find(locator, timeout=timeout)
        element = self.wait(timeout).until(EC.element_to_be_clickable(locator))
        element.click()
        return
