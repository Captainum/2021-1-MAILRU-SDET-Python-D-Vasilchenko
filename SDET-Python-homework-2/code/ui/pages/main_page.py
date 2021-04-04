import logging

from ui.pages.base_page import BasePage
from ui.locators.pages_locators import MainPageLocators

logger = logging.getLogger('test')

class MainPage(BasePage):
    url = 'https://target.my.com/'
    
    locators = MainPageLocators()

    def login(self, login=None, password=None):
        logger.info(f'Logging with login={login}, password={password}...')
        
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