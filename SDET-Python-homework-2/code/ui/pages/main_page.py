import logging
import allure

from ui.pages.base_page import BasePage
from ui.locators.pages_locators import MainPageLocators

logger = logging.getLogger('test')

class MainPage(BasePage):
    url = 'https://target.my.com/'
    
    locators = MainPageLocators()

    @allure.step("Logining")
    def login(self, login=None, password=None):
        logger.info(f'Logining with login={login}, password={password}...')
        
        if login is None:
            login = self.config['login']
        if password is None:
            password = self.config['password']
            
        self.click(self.locators.LOGINBUTTON_LOCATOR)

        username_input = self.find(MainPageLocators.USERNAME_LOCATOR)
        password_input = self.find(MainPageLocators.PASSWORD_LOCATOR)

        username_input.clear()
        password_input.clear()

        username_input.send_keys(login)
        password_input.send_keys(password)

        self.click(self.locators.ENTER_LOCATOR)