from ui.pages.base_page import BasePage
from ui.locators.pages_locators import SegmentsPageLocators

import time

class SegmentsPage(BasePage):
    url = 'https://target.my.com/segments/segments_list'
    
    locators = SegmentsPageLocators()

    def create_segment(self, segment_name) -> str:
        '''
        Returns segment name
        '''
        try:
            self.click(self.locators.CREATESEGMENT_HREF_LOCATOR)
        except:
            self.click(self.locators.CREATESEGMENT_BUTTON_LOCATOR)

        self.click(self.locators.ADDSEGMENT_CHECKBOX_LOCATOR)
        self.click(self.locators.ADDSEGMENT_BUTTON_LOCATOR)

        segment_name_input = self.find(self.locators.SEGMENT_NAME_LOCATOR)
        segment_name_input.clear()
        segment_name_input.send_keys(segment_name)

        self.click(self.locators.CREATESEGMENT_BUTTON_LOCATOR)

        segment = self.find((self.locators.SEGMENT_TITLE_LOCATOR_TEMPLATE[0],self.locators.SEGMENT_TITLE_LOCATOR_TEMPLATE[1].format(segment_name)))

        return segment.text

    def delete_segment(self, segment_name):
        segment_id = self.find((self.locators.SEGMENT_TITLE_LOCATOR_TEMPLATE[0], self.locators.SEGMENT_TITLE_LOCATOR_TEMPLATE[1].format(segment_name))).get_attribute("href")
        segment_id = segment_id.split('/')[-1]
        
        self.click((self.locators.SEGMENT_REMOVE_LOCATOR_TEMPLATE[0], self.locators.SEGMENT_REMOVE_LOCATOR_TEMPLATE[1].format(segment_id)))
        
        self.click(self.locators.SEGMENT_REMOVEBUTTON_LOCATOR)
        