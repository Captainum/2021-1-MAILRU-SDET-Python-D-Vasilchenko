from ui.pages.base_page import BasePage
from ui.locators.pages_locators import CampaignPageLocators

import time
import os
import pytest

class CampaignPage(BasePage):
    url = 'https://target.my.com/campaign/new'
    locators = CampaignPageLocators

    def create_campaign(self, campaign_name):
        self.click((self.locators.GOAL_LOCATOR_TEMPLATE[0], self.locators.GOAL_LOCATOR_TEMPLATE[1].format('traffic')), 10)

        url_input = self.find(self.locators.URL_LOCATOR)
        url_input.send_keys('ya.ru')
        self.click((self.locators.BANNERFORMAT_LOCATOR_TEMPLATE[0], self.locators.BANNERFORMAT_LOCATOR_TEMPLATE[1].format("Карусель")))

        campaign_name_input = self.find(self.locators.CAMPAIGN_NAME_LOCATOR)
        campaign_name_input.clear()
        campaign_name_input.send_keys(campaign_name)

        for number in range(1, 4):
            self.click((self.locators.SLIDENUMBER_LOCATOR_TEMPLATE[0], self.locators.SLIDENUMBER_LOCATOR_TEMPLATE[1].format(str(number))))
            self.scroll_to(self.find(self.locators.SLIDEPICTURE_LOCATOR))
            self.upload_picture(self.locators.SLIDEPICTURE_LOCATOR, 'pic1.jpeg')

            slide_url_input = self.find(self.locators.SLIDEURL_LOCATOR)
            slide_url_input.send_keys('ya.ru')

            slide_title_input = self.find(self.locators.SLIDETITLE_LOCATOR)
            slide_title_input.send_keys('TEST')
        self.upload_picture(self.locators.ADVPICTURE_LOCATOR, 'pic2.png')

        adv_title_input = self.find(self.locators.ADVTITLE_LOCATOR)
        adv_title_input.send_keys('TEST')

        adv_text_textarea = self.find(self.locators.ADVTEXT_LOCATOR)
        adv_text_textarea.send_keys('TEST')
        time.sleep(5)

        self.click(self.locators.CREATEBUTTON_LOCATOR)

    def upload_picture(self, locator, picture_name):
        input_field = self.find(locator)
        input_field.send_keys(os.path.join(self.config['pictures_root'], picture_name))