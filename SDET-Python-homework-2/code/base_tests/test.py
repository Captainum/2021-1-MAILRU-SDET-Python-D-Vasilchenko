import os
import time
from contextlib import contextmanager

import allure
import pytest
from selenium.webdriver.common.by import By

from base_tests.base import BaseCase
from utils.decorators import wait

#def test_all_drivers(all_drivers):
#    time.sleep(2)

class TestLogin(BaseCase):
    def test_negative_1(self):
        pass
    def test_negative_2(self):
        pass