import pytest
from tests.base import BaseCase

class Test(BaseCase):
    def test_login(self):
        self.main_page.login()
        assert "/dashboard" in self.driver.current_url
