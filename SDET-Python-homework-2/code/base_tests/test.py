import os
import time
from contextlib import contextmanager

import allure
import pytest
from selenium.webdriver.common.by import By

from base_tests.base import BaseCase
from utils.decorators import wait

from selenium.common.exceptions import TimeoutException

from ui.pages.main_page import MainPage
from ui.pages.dashboard_page import DashboardPage
from ui.pages.campaign_page import CampaignPage
from ui.pages.segments_page import SegmentsPage


class TestLogin(BaseCase):
    @pytest.mark.UI
    @allure.description("""Test with wrong email form""")
    @allure.epic('Login tests')
    @allure.feature('Test with wrong email form')
    def test_negative_1(self, main_page: MainPage):
        main_page.login('login', 'password')

        with allure.step('Check if notifier appeared or not'):
            assert main_page.find(main_page.locators.NOTIFY_LOCATOR)

    @pytest.mark.UI
    @allure.description("""Test with wrong password""")
    @allure.epic('Login tests')
    @allure.feature('Test with wrong password')
    def test_negative_2(self, main_page: MainPage):
        main_page.login('login@mail.ru', 'password')

        with allure.step('Check if current url has error_code or not'):
            assert 'error_code' in self.driver.current_url and 'error_code=0' not in self.driver.current_url


class TestDashboard(BaseCase):
    @pytest.mark.UI
    @allure.description("""Create a new campaign, and then check if it is created or not""")
    @allure.epic('Campaign tests')
    @allure.feature('Create campaign test')
    def test_create_campaign(self, dashboard_page: DashboardPage):
        campaign_page: CampaignPage = dashboard_page.go_to_create_campaign()

        campaign_name = campaign_page.create_campaign()

        dashboard_page.go_to_active_campaigns()

        assert dashboard_page.look_for_campaign(campaign_name)
        
    @pytest.mark.UI
    @allure.description("""Create a new segment, and then check if it is created or not""")
    @allure.epic('Segments tests')
    @allure.feature('Create segment test')
    def test_create_segment(self, dashboard_page: DashboardPage):
        segments_page: SegmentsPage = dashboard_page.go_to_segments_page()
        
        segment_name = segments_page.create_segment()

        segments_page.is_opened()

        assert segments_page.look_for_segment(segment_name)
    
    @pytest.mark.UI
    @allure.description("""Create a new segment, then delete it and check if it is deleted or not""")
    @allure.epic('Segments tests')
    @allure.feature('Delete segment test')
    def test_delete_segment(self, dashboard_page: DashboardPage):
        segments_page: SegmentsPage = dashboard_page.go_to_segments_page()
        segment_name = str(time.time())
        segment_name = segments_page.create_segment(segment_name)

        segments_page.delete_segment(segment_name)
                