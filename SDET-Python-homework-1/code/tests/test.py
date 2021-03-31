import pytest
from tests.base import BaseCase
from ui.locators.pages_locators import ContactsPageLocators
from ui.locators.pages_locators import DashboardPageLocators
from selenium.webdriver.common.by import By

class Test(BaseCase):
    @pytest.mark.UI
    def test_login(self, setup_base):
        self.main_page.login()
        assert "target.my.com/dashboard" in self.driver.current_url

    @pytest.mark.UI
    def test_logout(self, setup):
        self.dashboard_page.logout()
        assert self.driver.current_url == "https://target.my.com/"

    @pytest.mark.UI
    def test_changeInfo(self, setup):
        self.dashboard_page.changePage(DashboardPageLocators.PROFILE_LOCATOR)
        username = "TestTest"
        phonenumber = "+12345678910"
        email = "test@mail.ru"
        self.contacts_page.changeInfo(username, phonenumber, email)

        self.driver.refresh()

        assert username == self.contacts_page.find(ContactsPageLocators.USERNAME_LOCATOR).get_attribute("value")
        assert phonenumber == self.contacts_page.find(ContactsPageLocators.PHONENUMBER_LOCATOR).get_attribute("value")
        assert email == self.contacts_page.find(ContactsPageLocators.EMAIL_LOCATOR).get_attribute("value")

    @pytest.mark.UI
    @pytest.mark.parametrize(
        'page',
        [
            'balance',
            'statistics'
        ]
    )
    def test_changePage(self, page, setup):
        if page == 'balance':
            self.dashboard_page.changePage(DashboardPageLocators.BALANCE_LOCATOR)
            assert "target.my.com/billing" in self.driver.current_url
        elif page == 'statistics':
            self.dashboard_page.changePage(DashboardPageLocators.STATISTICS_LOCATOR)
            assert "target.my.com/statistics" in self.driver.current_url
