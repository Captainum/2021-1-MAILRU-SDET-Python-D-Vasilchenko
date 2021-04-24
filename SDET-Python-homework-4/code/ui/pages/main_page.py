from ui.pages.base_page import BasePage

from ui.locators.locators_android import MainPageANDROIDLocators

from ui.pages.settings_page import SettingsPageANDROID
from ui.pages.news_sources_page import NewsSourcesPageANDROID
from ui.pages.about_page import AboutPageANDROID

class MainPage(BasePage):
    pass


class MainPageANDROID(MainPage):
    locators = MainPageANDROIDLocators()

    def search(self, request):
        self.click_for_android(self.locators.KEYBOARD_BUTTON_LOCATOR)
        self.find(self.locators.INPUT_LOCATOR).send_keys(request)
        self.click_for_android(self.locators.SEARCH_BUTTON_LOCATOR)
        
    def find_fact_card(self):
        return self.find(self.locators.FACT_CARD_CONTENT_LOCATOR)
    
    def find_population_command(self):
        for i in range(1000):
            element = self.find(self.locators.COMMANDS_LOCATOR)
            if element.text == 'численность населения россии':
                self.click_for_android(self.locators.COMMANDS_LOCATOR)
                return self.find(self.locators.FACT_CARD_TITLE_LOCATOR)
            self.swipe_element_lo_left(self.locators.COMMANDS_LOCATOR, 110)
        assert False
    
    def change_news_source(self, source):
        self.click_for_android(self.locators.SETTINGS_LOCATOR)

        settings_page: SettingsPageANDROID = SettingsPageANDROID(self.driver, self.config)
        settings_page.go_to_news_source()
        
        news_sources_page: NewsSourcesPageANDROID = NewsSourcesPageANDROID(self.driver, self.config)
        news_sources_page.select_source(source)
        news_sources_page.go_to_settings()

        settings_page.click_for_android(settings_page.locators.CLOSE_SETTINGS_LOCATOR)
    
    def check_version(self):
        self.click_for_android(self.locators.SETTINGS_LOCATOR)

        settings_page = SettingsPageANDROID(self.driver, self.config)
        settings_page.go_to_about()

        about_page: AboutPageANDROID = AboutPageANDROID(self.driver, self.config)
        about_page.check_version()