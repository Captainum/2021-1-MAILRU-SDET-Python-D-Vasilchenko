import pytest
from _pytest.fixtures import FixtureRequest

from ui.pages.base_page import BasePage
from ui.pages.main_page import MainPage
from ui.pages.settings_page import SettingsPage
from ui.pages.news_sources_page import NewsSourcesPage
from ui.pages.about_page import AboutPage

class BaseCase:
    
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request: FixtureRequest):
        self.driver = driver
        self.config = config

        self.base_page: BasePage = request.getfixturevalue('base_page')
        self.main_page: MainPage = request.getfixturevalue('main_page')
        self.settings_page: SettingsPage = request.getfixturevalue('settings_page')
        self.news_sources_page: NewsSourcesPage = request.getfixturevalue('news_sources_page')
        self.about_page: AboutPage = request.getfixturevalue('about_page')
