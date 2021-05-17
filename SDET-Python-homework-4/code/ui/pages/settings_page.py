from ui.pages.base_page import BasePage

from ui.locators.locators_android import SettingsPageANDROIDLocators

class SettingsPage(BasePage):
    pass


class SettingsPageANDROID(SettingsPage):
    locators = SettingsPageANDROIDLocators()

    def go_to_news_source(self):
        self.swipe_to_element(self.locators.NEWS_SOURCES_LOCATOR, 5)
        self.click_for_android(self.locators.NEWS_SOURCES_LOCATOR)

    def go_to_about(self):
        self.swipe_to_element(self.locators.ABOUT_LOCATOR, 5)
        self.click_for_android(self.locators.ABOUT_LOCATOR)
        