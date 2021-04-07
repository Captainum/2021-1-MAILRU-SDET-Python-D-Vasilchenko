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

#def test_all_drivers(all_drivers):
#    time.sleep(2)

class TestLogin(BaseCase):
    @allure.description("""Test with wrong email form""")
    @allure.epic('Login tests')
    @allure.feature('Test with wrong email form')
    def test_negative_1(self, main_page: MainPage):
        self.logger.debug('Start test_negative_1')
        main_page.login('login', 'password')

        with allure.step('Check if notifier appeared or not'):
            try:
                main_page.find(main_page.locators.NOTIFY_LOCATOR)
                self.logger.debug('Test done successfully!')
            except TimeoutException:
                self.logger.debug('Test failed! (no notifier appeared)')
                raise

    @allure.description("""Test with wrong password""")
    @allure.epic('Login tests')
    @allure.feature('Test with wrong password')
    def test_negative_2(self, main_page: MainPage):
        self.logger.debug('Start test_negative_2')
        main_page.login('login@mail.ru', 'password')

        with allure.step('Check if current url has error_code or not'):
            try:
                assert 'error_code' in self.driver.current_url and 'error_code=0' not in self.driver.current_url
                self.logger.debug('Test done successfully!')
            except AssertionError:
                self.logger.debug('Test failed! (login and password were correct)')
                raise
            

class TestDashboard(BaseCase):
    @allure.description("""Create a new campaign, and then check if it is created or not""")
    @allure.epic('Campaign tests')
    @allure.feature('Create campaign test')
    def test_create_campaign(self, dashboard_page: DashboardPage):
        self.logger.info('Start test_create_campaign')
        campaign_page: CampaignPage = dashboard_page.go_to_create_campaign()
        campaign_name = str(time.time())
        campaign_page.create_campaign(campaign_name)

        dashboard_page.driver.get('https://target.my.com/dashboard')
        dashboard_page.is_opened()

        with allure.step('Choose active campaigns'):
            dashboard_page.click(dashboard_page.locators.SELECTMODULE_LOCATOR)
            dashboard_page.click(dashboard_page.locators.SELECT_ACTIVE_LOCATOR)

        with  allure.step('Looking for created campaign'):
            try:
                dashboard_page.find((dashboard_page.locators.CAMPAIGN_LOCATOR_TEMPLATE[0], dashboard_page.locators.CAMPAIGN_LOCATOR_TEMPLATE[1].format(campaign_name)))
                self.logger.info('Test done successfully!')
            except TimeoutException:
                self.logger.info('Test failed! (campaign was not created)')
                raise
        
    @allure.description("""Create a new segment, and then check if it is created or not""")
    @allure.epic('Segments tests')
    @allure.feature('Create segment test')
    def test_create_segment(self, dashboard_page: DashboardPage):
        self.logger.info('Start test_create_segment')
        segments_page: SegmentsPage = dashboard_page.go_to_segments_page()
        segment_name = str(time.time())
        segments_page.create_segment(segment_name)

        segments_page.is_opened()

        with allure.step('Looking for created segment'):
            try:
                segments_page.find((segments_page.locators.SEGMENT_TITLE_LOCATOR_TEMPLATE[0], segments_page.locators.SEGMENT_TITLE_LOCATOR_TEMPLATE[1].format(segment_name)))
                self.logger.info('Test done successfully!')
            except TimeoutException:
                self.logger.info('Test failed! (segment was not created)')
                raise
    
    @allure.description("""Create a new segment, then delete it and check if it is deleted or not""")
    @allure.epic('Segments tests')
    @allure.feature('Delete segment test')
    def test_delete_segment(self, dashboard_page: DashboardPage):
        self.logger.info('Start test_delete_segment')
        segments_page: SegmentsPage = dashboard_page.go_to_segments_page()
        segment_name = str(time.time())

        segments_page.create_segment(segment_name)

        segments_page.delete_segment(segment_name)

        segments_page.is_opened()

        with allure.step('Checking if segment deleted or not'):
            #Wait for page to be refreshed
            RETRY_COUNT = 10
            try:
                while(RETRY_COUNT > 0):
                    RETRY_COUNT -= 1
                    segments_page.find((segments_page.locators.SEGMENT_TITLE_LOCATOR_TEMPLATE[0], segments_page.locators.SEGMENT_TITLE_LOCATOR_TEMPLATE[1].format(segment_name)))
                    time.sleep(1)
                self.logger.info('Test failed! (segment was not deleted)')
                assert False
            except TimeoutException:
                self.logger.info('Test done successfully!')