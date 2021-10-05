import allure
import logging

from ui.pages.base_page import BasePage

from ui.locators.pages_locators import AuthorizationPageLocators

logger = logging.getLogger('test')

class AuthorizationPage(BasePage):
    locators = AuthorizationPageLocators()

    @allure.step('Checking base view of AuthorizationPage')
    def check_base_view(self):
        logger.info('Checking base view of AuthorizationPage')
        
        assert self.find(self.locators.TEXT_WELCOME_LOCATOR).text == 'Welcome to the TEST SERVER'
        assert self.find(self.locators.INPUT_USERNAME_LOCATOR).text == ''
        assert self.find(self.locators.INPUT_PASSWORD_LOCATOR).text == ''
        assert self.find(self.locators.BUTTON_LOGIN_LOCATOR)
        assert self.find(self.locators.TEXT_NOT_REGISTERED_LOCATOR).text == 'Not registered? Create an account'
        assert self.find(self.locators.HREF_CREATE_AN_ACCOUNT).text == 'Create an account'
    
    @allure.step('Go to registration page from authorization page')
    def go_to_create_account(self):
        logger.info('Go to registration page from authorization page')

        self.click(self.locators.HREF_CREATE_AN_ACCOUNT)
    
    @allure.step('Login user {username}')
    def send_values(self, username='', password=''):
        logger.info(f'Enter username={username} and password={password} at AuthorizationPage and press LOGIN')

        username_input = self.find(self.locators.INPUT_USERNAME_LOCATOR)
        password_input = self.find(self.locators.INPUT_PASSWORD_LOCATOR)

        username_input.send_keys(username)
        password_input.send_keys(password)

        self.click(self.locators.BUTTON_LOGIN_LOCATOR)