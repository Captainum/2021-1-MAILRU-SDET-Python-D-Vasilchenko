from ui.pages.base_page import BasePage
from ui.locators.pages_locators import DashboardPageLocators

class DashboardPage(BasePage):
    locators = DashboardPageLocators()

    def logout(self):
        self.click(DashboardPageLocators.RIGHTMENUBUTTON_LOCATOR)
        self.click(DashboardPageLocators.LOGOUT_LOCATOR, 15)

    def changePage(self, locator):
        self.click(locator)
