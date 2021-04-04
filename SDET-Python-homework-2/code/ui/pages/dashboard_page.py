import time
import logging

from ui.pages.base_page import BasePage
from ui.locators.pages_locators import DashboardPageLocators

from ui.pages.campaign_page import CampaignPage
from ui.pages.segments_page import SegmentsPage

logger = logging.getLogger('test')

class DashboardPage(BasePage):
    url = 'https://target.my.com/dashboard'
    locators = DashboardPageLocators()

    def go_to_create_campaign(self):
        logger.info('Go to create campaign page...')

        try:
            self.click(self.locators.CREATECAMPAIGN_HREF_LOCATOR, 3)
        except:
            self.click(self.locators.CREATECAMPAIGN_BUTTON_LOCATOR, 3)
        
        return CampaignPage(self.driver, self.config)
    
    def go_to_segments_page(self):
        logger.info('Go to segments page...')
        
        self.click(self.locators.SEGMENTS_LOCATOR)
        return SegmentsPage(self.driver, self.config)