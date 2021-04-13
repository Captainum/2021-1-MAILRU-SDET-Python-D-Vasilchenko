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
        self.logger.debug('Start test_negative_1')
        main_page.login('login', 'password')

        with allure.step('Check if notifier appeared or not'):
            assert main_page.find(main_page.locators.NOTIFY_LOCATOR)

    @pytest.mark.UI
    @allure.description("""Test with wrong password""")
    @allure.epic('Login tests')
    @allure.feature('Test with wrong password')
    def test_negative_2(self, main_page: MainPage):
        self.logger.debug('Start test_negative_2')
        main_page.login('login@mail.ru', 'password')

        with allure.step('Check if current url has error_code or not'):
            assert 'error_code' in self.driver.current_url and 'error_code=0' not in self.driver.current_url


class TestDashboard(BaseCase):
    @pytest.mark.UI
    @allure.description("""Create a new campaign, and then check if it is created or not""")
    @allure.epic('Campaign tests')
    @allure.feature('Create campaign test')
    def test_create_campaign(self, dashboard_page: DashboardPage):
        self.logger.info('Start test_create_campaign')
        campaign_page: CampaignPage = dashboard_page.go_to_create_campaign()

        campaign_name = campaign_page.create_campaign()

        dashboard_page.go_to_active_campaigns()

        with allure.step('Looking for created campaign'):
            assert dashboard_page.find((dashboard_page.locators.CAMPAIGN_LOCATOR_TEMPLATE[0], dashboard_page.locators.CAMPAIGN_LOCATOR_TEMPLATE[1].format(campaign_name)))
        
    @pytest.mark.UI
    @allure.description("""Create a new segment, and then check if it is created or not""")
    @allure.epic('Segments tests')
    @allure.feature('Create segment test')
    def test_create_segment(self, dashboard_page: DashboardPage):
        self.logger.info('Start test_create_segment')
        segments_page: SegmentsPage = dashboard_page.go_to_segments_page()
        
        segment_name = segments_page.create_segment()

        segments_page.is_opened()

        with allure.step('Looking for created segment'):
            assert segments_page.find((segments_page.locators.SEGMENT_TITLE_LOCATOR_TEMPLATE[0], segments_page.locators.SEGMENT_TITLE_LOCATOR_TEMPLATE[1].format(segment_name)))
    
    @pytest.mark.UI
    @allure.description("""Create a new segment, then delete it and check if it is deleted or not""")
    @allure.epic('Segments tests')
    @allure.feature('Delete segment test')
    def test_delete_segment(self, dashboard_page: DashboardPage):
        self.logger.info('Start test_delete_segment')
        segments_page: SegmentsPage = dashboard_page.go_to_segments_page()

        segment_name = segments_page.create_segment()

        segments_page.delete_segment(segment_name)

        with allure.step('Checking if segment deleted or not'):
            segments_page.driver.refresh()
            segments_page.is_opened()
            #Eсли мы нашли удаленный сегмент, то тест провален, иначе - тест прошел.
            try:
                segments_page.find((segments_page.locators.SEGMENT_TITLE_LOCATOR_TEMPLATE[0], segments_page.locators.SEGMENT_TITLE_LOCATOR_TEMPLATE[1].format(segment_name)))
                assert False
            except TimeoutException:
                assert True
                