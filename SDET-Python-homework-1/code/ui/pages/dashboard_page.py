from ui.pages.base_page import BasePage
from ui.locators.pages_locators import DashboardPageLocators
from selenium.webdriver.support.wait import WebDriverWait

import time

class DashboardPage(BasePage):
    locators = DashboardPageLocators()

    def logout(self):
        self.click(DashboardPageLocators.RIGHTMENUBUTTON_LOCATOR)
        time.sleep(2.5)
        self.click(DashboardPageLocators.LOGOUT_LOCATOR)

    def changePage(self, locator):
        self.click(locator)
