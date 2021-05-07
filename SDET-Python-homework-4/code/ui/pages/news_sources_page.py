from ui.pages.base_page import BasePage

from ui.locators.locators_android import NewsSourcesPageANDROIDLocators

class NewsSourcesPage(BasePage):
    pass


class NewsSourcesPageANDROID(NewsSourcesPage):
    locators = NewsSourcesPageANDROIDLocators()

    def select_source(self, source):
        self.click_for_android((self.locators.ITEM_SELECTED_LOCATOR[0], self.locators.NEWS_SOURCE_LOCATOR[1].format(source)))
        assert self.find((self.locators.ITEM_SELECTED_LOCATOR[0], self.locators.ITEM_SELECTED_LOCATOR[1].format(source)))

    def go_to_settings(self):
        self.click_for_android(self.locators.BACK_BUTTON_LOCATOR)
        