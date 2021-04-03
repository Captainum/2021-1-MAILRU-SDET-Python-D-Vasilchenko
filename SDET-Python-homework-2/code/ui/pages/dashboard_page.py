from ui.pages.base_page import BasePage
from ui.locators.pages_locators import DashboardPageLocators

from ui.pages.campaign_page import CampaignPage
from ui.pages.segments_page import SegmentsPage

import time

class DashboardPage(BasePage):
    url = 'https://target.my.com/dashboard'
    locators = DashboardPageLocators()

    def logout(self):
        self.click(self.locators.RIGHTMENUBUTTON_LOCATOR)
        time.sleep(2.5)
        self.click(self.locators.LOGOUT_LOCATOR)

    def go_to_create_campaign(self):
        try:
            self.click(self.locators.CREATECAMPAIGN_HREF_LOCATOR)
        except:
            self.click(self.locators.CREATECAMPAIGN_BUTTON_LOCATOR)
        
        return CampaignPage(self.driver, self.config)
    
    def go_to_create_segment(self):
        self.click(self.locators.SEGMENTS_LOCATOR)
        return SegmentsPage(self.driver, self.config)