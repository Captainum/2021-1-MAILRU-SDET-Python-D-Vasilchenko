import allure
import logging

from ui.pages.base_page import BasePage
from ui.locators.pages_locators import RegistrationPageLocators

logger = logging.getLogger('test')

class RegistrationPage(BasePage):
    locators = RegistrationPageLocators()
    
    @allure.step('Checking base view of RegistrationPage')
    def check_base_view(self):
        logger.info('Checking base view of RegistrationPage')

        assert self.find(self.locators.TEXT_REGISTRATION_LOCATOR).text == 'Registration'
        assert self.find(self.locators.INPUT_USERNAME_LOCATOR). text == ''
        assert self.find(self.locators.INPUT_EMAIL_LOCATOR).text == ''
        assert self.find(self.locators.INPUT_PASSWORD_LOCATOR).text == ''
        assert self.find(self.locators.INPUT_PASSWORD_LOCATOR).text == ''
        assert self.find(self.locators.INPUT_REPEAT_PASSWORD_LOCATOR).text == ''
        self.find(self.locators.INPUT_CHECKBOX_LOCATOR)
        assert self.find(self.locators.TEXT_ACCEPT_LOCATOR).text == 'I accept that I want to be a SDET'
        self.find(self.locators.BUTTON_REGISTER_LOCATOR)
        assert self.find(self.locators.TEXT_HAVE_AN_ACCOUNT).text == 'Already have an account? Log in'
        assert self.find(self.locators.HREF_LOG_IN_LOCATOR).text == 'Log in'
    
    @allure.step('Go to login page from registration page')
    def go_to_log_in(self):
        logger.info('Go to login page from registration page')

        self.click(self.locators.HREF_LOG_IN_LOCATOR)
    
    @allure.step('Registrate new user')
    def send_values(self, username='', email='', password='', repeat_password='', checkbox=False):
        logger.info(f'Enter username={username}, email={email}, password={password}, repeat_password={repeat_password}, checkbox={checkbox} at RegistrationPage and press REGISTER')
        
        username_input = self.find(self.locators.INPUT_USERNAME_LOCATOR)
        email_input = self.find(self.locators.INPUT_EMAIL_LOCATOR)
        password_input = self.find(self.locators.INPUT_PASSWORD_LOCATOR)
        repeat_password_input = self.find(self.locators.INPUT_REPEAT_PASSWORD_LOCATOR)

        username_input.send_keys(username)
        email_input.send_keys(email)
        password_input.send_keys(password)
        repeat_password_input.send_keys(repeat_password)
        
        if checkbox:
            self.click(self.locators.INPUT_CHECKBOX_LOCATOR)
        
        self.click(self.locators.BUTTON_REGISTER_LOCATOR)