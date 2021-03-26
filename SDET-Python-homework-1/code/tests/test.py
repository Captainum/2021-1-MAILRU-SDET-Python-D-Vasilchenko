import pytest
from tests.base import BaseCase

class Test(BaseCase):
    def test_login(self):
        self.main_page.login()
        assert "/dashboard" in self.driver.current_url

    def test_logout(self):
        self.main_page.login()
        self.dashboard_page.logout()
        assert self.driver.current_url == "https://target.my.com/"
