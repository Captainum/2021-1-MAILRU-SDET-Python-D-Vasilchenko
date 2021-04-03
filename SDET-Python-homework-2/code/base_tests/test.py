import os
import time
from contextlib import contextmanager

import allure
import pytest
from selenium.webdriver.common.by import By

from base_tests.base import BaseCase
from utils.decorators import wait

from ui.pages.dashboard_page import DashboardPage
from ui.pages.campaign_page import CampaignPage

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
    @pytest.mark.skip("SKIP")
    def test_create_segment(self, dashboard_page):
        pass