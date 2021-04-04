import time
import logging

from ui.pages.base_page import BasePage
from ui.locators.pages_locators import SegmentsPageLocators

from selenium.common.exceptions import TimeoutException

logger = logging.getLogger('test')

class SegmentsPage(BasePage):
    url = 'https://target.my.com/segments/segments_list'
    
    locators = SegmentsPageLocators()

    def create_segment(self, segment_name):
        logger.info(f'Creating a segment with name={segment_name}...')
        
        try:
            self.click(self.locators.CREATESEGMENT_HREF_LOCATOR, 2)
        except:
            self.click(self.locators.CREATESEGMENT_BUTTON_LOCATOR, 2)

        self.click(self.locators.ADDSEGMENT_ITEM_LOCATOR)
        self.click(self.locators.ADDSEGMENT_CHECKBOX_LOCATOR)
        self.click(self.locators.ADDSEGMENT_BUTTON_LOCATOR)

        segment_name_input = self.find(self.locators.SEGMENT_NAME_LOCATOR)
        segment_name_input.clear()
        segment_name_input.send_keys(segment_name)

        self.click(self.locators.CREATESEGMENT_BUTTON_LOCATOR)

    def delete_segment(self, segment_name):
        logger.info(f'Deleting a segment with name={segment_name}...')
        
        segment_title = self.find((self.locators.SEGMENT_TITLE_LOCATOR_TEMPLATE[0], self.locators.SEGMENT_TITLE_LOCATOR_TEMPLATE[1].format(segment_name))).get_attribute('href')
        segment_id = segment_title.split('/')[-1]

        self.click((self.locators.SEGMENT_REVERTBUTTON_LOCATOR_TEMPLATE[0], self.locators.SEGMENT_REVERTBUTTON_LOCATOR_TEMPLATE[1].format(segment_id)))
        self.click(self.locators.SEGMENT_CONFIRMBUTTON_LOCATOR)