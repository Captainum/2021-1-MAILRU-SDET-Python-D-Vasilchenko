from ui.pages.base_page import BasePage

from ui.locators.locators_android import AboutPageANDROIDLocators

class AboutPage(BasePage):
    pass


class AboutPageANDROID(AboutPage):
    locators = AboutPageANDROIDLocators()

    def check_version(self):
        assert self.config['apk_path'].strip().split('/')[-1].split('v')[-1][:-4] in self.find(self.locators.VERSION_LOCATOR).text
        assert 'Все права защищены' in self.find(self.locators.COPYRIGHT_LOCATOR).text