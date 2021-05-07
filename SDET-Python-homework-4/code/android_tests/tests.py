import pytest

from android_tests.base import BaseCase

class TestMarussiaAndroid(BaseCase):
    @pytest.mark.AndroidUI
    def test_command_window(self):
        self.main_page.search('Russia')
        fact_card = self.main_page.find_fact_card()
        assert 'Росси́я, другое официальное название - Росси́йская Федера́ция, - государство в Восточной Европе и Северной Азии.' in fact_card.text

        fact_card = self.main_page.find_population_command()
        assert fact_card.text == '146 млн.'
    
    @pytest.mark.AndroidUI
    def test_calculator(self):
        expected_answer = '122'
        self.main_page.search('(2+(5*4*18)/3)')
        assert expected_answer == self.main_page.find(self.main_page.locators.ANSWER_LOCATOR).text
    
    @pytest.mark.AndroidUI
    def test_news(self):
        source = 'Вести FM'
        self.main_page.change_news_source(source) # Настраиваем источник
        self.main_page.search('News') # Выполняем поиск
        self.main_page.check_news_source(source) # Проверяем источник

    @pytest.mark.AndroidUI
    def test_settings(self):
        self.main_page.check_version()