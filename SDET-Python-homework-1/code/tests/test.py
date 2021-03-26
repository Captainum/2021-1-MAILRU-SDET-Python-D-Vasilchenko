import pytest
from tests.base import BaseCase
from ui.locators.pages_locators import ContactsPageLocators
from selenium.webdriver.common.by import By

class Test(BaseCase):
    @pytest.mark.UI
    def test_login(self):
        self.main_page.login()
        assert "target.my.com/dashboard" in self.driver.current_url

    @pytest.mark.UI
    def test_logout(self):
        self.main_page.login()
        self.dashboard_page.logout()
        assert self.driver.current_url == "https://target.my.com/"

    @pytest.mark.UI
    def test_changeInfo(self):
        self.main_page.login()
        self.driver.get("https://target.my.com/profile/contacts")
        username = "TestTest"
        phonenumber = "+12345678910"
        email = "test@mail.ru"
        self.contacts_page.changeInfo(username, phonenumber, email)

        self.driver.refresh()

        assert username == self.base_page.find(ContactsPageLocators.USERNAME_LOCATOR).get_attribute("value")
        assert phonenumber == self.base_page.find(ContactsPageLocators.PHONENUMBER_LOCATOR).get_attribute("value")
        assert email == self.base_page.find(ContactsPageLocators.EMAIL_LOCATOR).get_attribute("value")

    @pytest.mark.UI
    @pytest.mark.parametrize(
        'page',
        [
            pytest.param('balance'),
            pytest.param('statistics')
        ]
    )
    def test_changePage(self, page):
        self.main_page.login()
        if page == 'balance':
            self.dashboard_page.changePage((By.XPATH, '//li[starts-with(@class, "center-module-button")]/a[contains(text(), "Баланс")]'))
            assert "target.my.com/billing" in self.driver.current_url
        elif page == 'statistics':
            self.dashboard_page.changePage((By.XPATH, '//li[starts-with(@class, "center-module-button")]/a[contains(text(), "Статистика")]'))
            assert "target.my.com/statistics" in self.driver.current_url
