import allure
import logging

from builder.builder import Builder

from ui.pages.base_page import BasePage
from ui.pages.registration_page import RegistrationPage

from ui.locators.pages_locators import MainPageLocators

logger = logging.getLogger('test')

class MainPage(BasePage):
    locators = MainPageLocators()

    @allure.step('Checking base view of MainPage')
    def check_base_view(self, username):
        logger.info('Checking base view of MainPage')

        assert self.find(self.locators.ICON_BUG_LOCATOR)
        assert self.find(self.locators.HREF_BRAND_LOCATOR).text == 'TM version 0.1'
        assert self.find(self.locators.BUTTON_HOME_LOCATOR).text == 'HOME'
        assert self.find(self.locators.BUTTON_PYTHON_LOCATOR).text == 'Python'
        assert self.find(self.locators.BUTTON_LINUX_LOCATOR).text == 'Linux'
        assert self.find(self.locators.BUTTON_NETWORK_LOCATOR).text == 'Network'
        
        assert self.find(self.locators.TEXT_LOGGED_AS_LOCATOR).text == f'Logged as {username}'
        assert self.find(self.locators.BUTTON_LOGOUT_LOCATOR).text == 'Logout'
        
        assert self.find(self.locators.TEXT_API_LOCATOR).text == 'What is an API?'
        assert self.find(self.locators.TEXT_FUTURE_LOCATOR).text == 'Future of internet'
        assert self.find(self.locators.TEXT_SMTP_LOCATOR).text == 'Lets talk about SMTP?'
        
        assert self.find(self.locators.BUTTON_API_LOCATOR)
        assert self.find(self.locators.BUTTON_FUTURE_LOCATOR)
        assert self.find(self.locators.BUTTON_SMTP_LOCATOR)
        
        assert self.find(self.locators.TEXT_POWERED_BY_LOCATOR).text == 'powered by ТЕХНОАТОМ'
        assert self.find(self.locators.TEXT_RANDOM_PHRASE_LOCATOR).text != ''