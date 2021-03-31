from ui.pages.base_page import BasePage
from ui.locators.pages_locators import MainPageLocators

class MainPage(BasePage):
    locators = MainPageLocators()

    def __init__(self, driver, config):
        super().__init__(driver)
        self.config = config

    def login(self):
        login_button = self.find(MainPageLocators.LOGINBUTTON_LOCATOR)
        login_button.click()

        username_input = self.find(MainPageLocators.USERNAME_LOCATOR)
        password_input = self.find(MainPageLocators.PASSWORD_LOCATOR)

        username_input.clear()
        password_input.clear()

        username_input.send_keys(self.config['login'])
        password_input.send_keys(self.config['password'])

        enter_button = self.find(MainPageLocators.ENTER_LOCATOR)
        enter_button.click()
