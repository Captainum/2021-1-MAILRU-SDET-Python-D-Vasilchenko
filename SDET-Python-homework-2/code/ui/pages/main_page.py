from ui.pages.base_page import BasePage
from ui.locators.pages_locators import MainPageLocators

class MainPage(BasePage):
    url = 'https://target.my.com/'
    
    locators = MainPageLocators()

    def __init__(self, driver, config):
        super().__init__(driver, config)

    def login(self, login=None, password=None):
        if login is None:
            login = self.config['login']
        if password is None:
            password = self.config['password']
            
        login_button = self.find(MainPageLocators.LOGINBUTTON_LOCATOR)
        login_button.click()

        username_input = self.find(MainPageLocators.USERNAME_LOCATOR)
        password_input = self.find(MainPageLocators.PASSWORD_LOCATOR)

        username_input.clear()
        password_input.clear()

        username_input.send_keys(login)
        password_input.send_keys(password)

        enter_button = self.find(MainPageLocators.ENTER_LOCATOR)
        enter_button.click()