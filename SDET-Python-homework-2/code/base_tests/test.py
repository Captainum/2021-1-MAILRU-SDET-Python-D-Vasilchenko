import os
import time
from contextlib import contextmanager

import allure
import pytest
from selenium.webdriver.common.by import By

from base_tests.base import BaseCase
from utils.decorators import wait

from selenium.common.exceptions import TimeoutException

from ui.pages.dashboard_page import DashboardPage
from ui.pages.campaign_page import CampaignPage
from ui.pages.segments_page import SegmentsPage

#def test_all_drivers(all_drivers):
#    time.sleep(2)

class TestLogin(BaseCase):
    @pytest.mark.skip("SKIP")
    def test_negative_1(self):
        pass
    @pytest.mark.skip("SKIP")
    def test_negative_2(self):
        pass

class TestDashboard(BaseCase):
    def test_create_campaign(self, dashboard_page: DashboardPage):
        campaign_page: CampaignPage = dashboard_page.go_to_create_campaign()
        campaign_page.create_campaign()
        campaign_name = dashboard_page.find((dashboard_page.locators.CAMPAIGN_LOCATOR_TEMPLATE[0], dashboard_page.locators.CAMPAIGN_LOCATOR_TEMPLATE[1].format("TEST CAMPAIGN")))
        assert campaign_name.text == "TEST CAMPAIGN"
    
    def test_create_segment(self, dashboard_page: DashboardPage):
        segments_page: SegmentsPage = dashboard_page.go_to_segments_page()
        segment_name = str(time.time())
        assert segments_page.create_segment(segment_name) == segment_name
    
    def test_delete_segment(self, dashboard_page: DashboardPage):
        segments_page: SegmentsPage = dashboard_page.go_to_segments_page()
        segment_name = segments_page.create_segment(str(time.time()))

        segments_page.delete_segment(segment_name)

        try:
            segments_page.find((segments_page.locators.SEGMENT_TITLE_LOCATOR_TEMPLATE[0], segments_page.locators.SEGMENT_TITLE_LOCATOR_TEMPLATE[1].format(segment_name)))
            assert False
        except TimeoutException:
            assert True
