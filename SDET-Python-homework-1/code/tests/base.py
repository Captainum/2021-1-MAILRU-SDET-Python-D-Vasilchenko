import pytest
from _pytest.fixtures import FixtureRequest

from ui.pages.base_page import BasePage
from ui.pages.main_page import MainPage
from ui.pages.dashboard_page import DashboardPage
from ui.pages.contacts_page import ContactsPage

class BaseCase:
    @pytest.fixture(scope='function')
    def setup_base(self, driver, request:FixtureRequest):
        self.driver = driver
        self.main_page: MainPage = request.getfixturevalue('main_page')

    @pytest.fixture(scope='function')
    def setup(self, driver_logined, request:FixtureRequest):
        self.driver = driver_logined

        self.dashboard_page: DashboardPage = request.getfixturevalue('dashboard_page')
        self.contacts_page: ContactsPage = request.getfixturevalue('contacts_page')
