import logging
import allure

from ui.fixtures import get_driver

import pytest
from _pytest.fixtures import FixtureRequest

from base_tests.base.base import BaseCase

from ui.pages.base_page import BasePage
from ui.pages.authorization_page import AuthorizationPage
from ui.pages.registration_page import RegistrationPage
from ui.pages.main_page import MainPage

from api.client import MockClient

import time

logger = logging.getLogger('test')

class UIBase(BaseCase):
    '''
        Базовый класс для тестирования UI части приложения
    '''

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, request: FixtureRequest, ui_report):

        self.driver = driver   

        self.base_page: BasePage = request.getfixturevalue('base_page')
        self.authorization_page: AuthorizationPage = request.getfixturevalue('authorization_page')
        self.registration_page: RegistrationPage = request.getfixturevalue('registration_page')
        self.registration_page.url += 'reg'
        self.main_page: MainPage = request.getfixturevalue('main_page')
        self.main_page.url += 'welcome/'

        logger.debug('UIBase setup is done')


class TestUIAuthorization(UIBase):
    '''
        Тестирование формы авторизации
    '''
    @pytest.mark.UI
    @allure.epic('Test UI: Authorization page')
    @allure.story('Check base view of page')
    def test_base_view(self):
        '''
            Тестируем наличие всех элементов на странице

            Шаги:

                1. Переходим на страницу авторизации

            Ожидаемый результат:

                1. Присутствует текст 'Welcome to the TEST SERVER'
                2. Поля для логина и пароля пусты
                3. Присутствует кнопка входа
                4. Присутствует текст 'Not registered? Create an account'
                5. Присутствует кликабельный текст 'Create an account'
        '''
        self.authorization_page.check_base_view()

    @pytest.mark.UI
    @allure.epic('Test UI: Authorization page')
    @allure.story('Check login without password')
    def test_login_wo_password(self):
        '''
            Тестируем вход без указания пароля

            Шаги:

                1. Переходим на страницу авторизации
                2. Вводим только логин
                3. Нажимаем кнопку 'Login'

            Ожидаемый результат:

                1. Остаемся на странице авторизации
        '''
        username = self.builder.random_username()
        self.authorization_page.send_values(username=username)
        
        time.sleep(5)

        self.authorization_page.is_opened()

    @pytest.mark.UI
    @allure.epic('Test UI: Authorization page')
    @allure.story('Check login without login')
    def test_login_wo_login(self):
        '''
            Тестируем вход без указания логина

            Шаги:

                1. Переходим на страницу авторизации
                2. Вводим только пароль
                3. Нажимаем кнопку 'Login'

            Ожидаемый результат:

                1. Остаемся на странице авторизации
        '''
        password = self.builder.random_password()
        self.authorization_page.send_values(password=password)
        
        time.sleep(5)

        self.authorization_page.is_opened()

    @pytest.mark.UI
    @allure.epic('Test UI: Authorization page')
    @allure.story('Check login with incorrect login length={length}')
    @pytest.mark.parametrize('length', range(1, 6))
    def test_login_incorrect_username_length(self, length):
        '''
            Тестируем вход с некорректной длиной логина (< 6)

            Шаги:

                1. Переходим на страницу авторизации
                2. Вводим некорректную длину логина
                3. Вводим любой пароль
                3. Нажимаем кнопку 'Login'

            Ожидаемый результат:

                1. Появление ошибки 'Incorrect username length'
        '''
        username = self.builder.random_username(length=length)
        password = self.builder.random_password()

        self.authorization_page.send_values(username=username, password=password)

        with allure.step('Check error visibility'):
            error = self.authorization_page.find(self.authorization_page.locators.TEXT_ERROR_LOCATOR)
            time.sleep(1) # Ждем, пока появится надпись
            assert error.text == 'Incorrect username length'

    @pytest.mark.UI
    @allure.epic('Test UI: Authorization page')
    @allure.story('Check login with incorrect username and password')
    def test_login_negative(self):
        '''
            Тестируем вход с недействительными данными

            Шаги:

                1. Переходим на страницу авторизации
                2. Вводим несуществующие логин и пароль
                3. Нажимаем кнопку 'Login'

            Ожидаемый результат:

                1. Появление ошибки 'Invalid username or password'
        '''
        username, password, email = self.builder.random_person()

        self.authorization_page.send_values(username=username, password=password)
        
        with allure.step('Check error visibility'):
            error = self.authorization_page.find(self.authorization_page.locators.TEXT_ERROR_LOCATOR)
            time.sleep(1) # Ждем, пока появится надпись
            assert error.text == 'Invalid username or password'

    @pytest.mark.UI
    @allure.epic('Test UI: Authorization page')
    @allure.story('Check login with incorrect password')
    def test_login_incorrect_password(self):
        '''
            Тестируем вход с правильным логином, но неправильным паролем

            Шаги:
                
                1. Добавляем пользователя напрямую в БД
                2. Переходим на страницу авторизации
                3. Вводим существующий логин и неправильный пароль
                4. Нажимаем кнопку 'Login'

            Ожидаемый результат:

                1. Появление ошибки 'Invalid username or password'
        '''
        with allure.step('Generate user and add him to DB'):
            username, password, email = self.builder.random_person()

            self.mysql_builder.create_user(username=username, password=password, email=email)

        password_2 = self.builder.random_password()

        self.authorization_page.send_values(username=username, password=password_2)
        
        with allure.step('Check error visibility'):
            error = self.authorization_page.find(self.authorization_page.locators.TEXT_ERROR_LOCATOR)
            time.sleep(1) # Ждем, пока появится надпись
            assert error.text == 'Invalid username or password'

    @pytest.mark.UI
    @allure.epic('Test UI: Authorization page')
    @allure.story('Check login with incorrect login')
    def test_login_incorrect_login(self):
        '''
            Тестируем вход с правильным паролем, но неправильным логином

            Шаги:

                1. Добавляем пользователя напрямую в БД
                2. Переходим на страницу авторизации
                3. Вводим несуществующий логин и существующий пароль
                4. Нажимаем кнопку 'Login'

            Ожидаемый результат:

                1. Появление ошибки 'Invalid username or password'
        '''
        with allure.step('Generate user and add him to DB'):
            username, password, email = self.builder.random_person()
            self.mysql_builder.create_user(username=username, password=password, email=email)

        username_2 = self.builder.random_password()

        self.authorization_page.send_values(username=username_2, password=password)
        
        with allure.step('Check error visibility'):
            error = self.authorization_page.find(self.authorization_page.locators.TEXT_ERROR_LOCATOR)
            time.sleep(1) # Ждем, пока появится надпись
            assert error.text == 'Invalid username or password'

    @pytest.mark.UI
    @allure.epic('Test UI: Authorization page')
    @allure.story('Check login with correct username and password')
    def test_login(self):
        '''
            Тестируем вход с корректными данными

            Шаги:

                1. Добавляем пользователя напрямую в БД
                2. Переходим на страницу авторизации
                3. Вводим существующие логин и пароль
                4. Нажимаем кнопку 'Login'

            Ожидаемый результат:

                1. Переход на главную страницу
                2. Пользователь не заблокирован, активен, время входа не пустое
        '''
        with allure.step('Generate user and add him to DB'):
            username, password, email = self.builder.random_person()
            self.mysql_builder.create_user(username=username, password=password, email=email)

        self.authorization_page.send_values(username=username, password=password)
        
        with allure.step('Check that MainPage is opened'):
            assert self.authorization_page.is_opened(self.authorization_page.url + 'welcome/')

        with allure.step('Check database content'):
            user = self.mysql_builder.get_user_by_username(username)[0]
            
            assert user.access == 1
            assert user.active == 1
            assert user.start_active_time is not None

    @pytest.mark.UI
    @allure.epic('Test UI: Authorization page')
    @allure.story('Check login with correct username and password')
    def test_login_w_access_0(self):
        '''
            Тестируем вход с корректными данными заблокированного пользователя

            Шаги:

                1. Добавляем пользователя напрямую в БД, access = 0
                2. Переходим на страницу авторизации
                3. Вводим существующие логин и пароль
                4. Нажимаем кнопку 'Login'

            Ожидаемый результат:

                1. Появление ошибки 'Ваша учетная запись заблокирована'
        '''
        with allure.step('Generate user and add him to DB'):
            username, password, email = self.builder.random_person()
            self.mysql_builder.create_user(username=username, password=password, email=email, access=0)

        self.authorization_page.send_values(username=username, password=password)
        
        with allure.step('Check error visibility'):
            error = self.authorization_page.find(self.authorization_page.locators.TEXT_ERROR_LOCATOR)
            time.sleep(1) # Ждем, пока появится надпись
            assert error.text == 'Ваша учетная запись заблокирована'

    @pytest.mark.UI
    @allure.epic('Test UI: Authorization page')
    @allure.story('Check login with correct username and password')
    def test_login_w_active_1(self):
        '''
            Тестируем вход с корректными данными уже активного пользователя

            Шаги:

                1. Добавляем пользователя напрямую в БД, active = 1
                2. Переходим на страницу авторизации
                3. Вводим существующие логин и пароль
                4. Нажимаем кнопку 'Login'

            Ожидаемый результат:

                1. Переход на главную страницу
        '''
        with allure.step('Generate user and add him to DB'):
            username, password, email = self.builder.random_person()
            self.mysql_builder.create_user(username=username, password=password, email=email, active=1)

        self.authorization_page.send_values(username=username, password=password)
        
        with allure.step('Check that MainPage is opened'):
            assert self.authorization_page.is_opened(self.authorization_page.url + 'welcome/')

        with allure.step('Check database content'):
            user = self.mysql_builder.get_user_by_username(username)[0]
            
            assert user.access == 1
            assert user.active == 1
            assert user.start_active_time is not None
    
    @pytest.mark.UI
    @allure.epic('Test UI: Authorization page')
    @allure.story('Check "Create and account" reference')
    def test_go_to_create_account(self):
        '''
            Тестируем кнопку создания аккаунта

            Шаги:

                1. Переходим на страницу авторизации
                2. Нажимаем на 'Create an account'

            Ожидаемый результат:
                
                1. Переход на страницу регистрации
        '''
        self.authorization_page.go_to_create_account()
        
        assert self.authorization_page.is_opened(self.authorization_page.url + 'reg')


class TestUIRegistration(UIBase):
    '''
        Тестирование формы регистрации
    '''

    @pytest.fixture(scope='function', autouse=True)
    def setup_page(self):
        self.registration_page.driver.get(self.registration_page.url)

    @pytest.mark.UI
    @allure.epic('Test UI: Registration page')
    @allure.story('Check base view of page')
    def test_base_view(self):
        '''
            Тестируем наличие всех элементов на странице

            Шаги:

                1. Переходим на страницу регистрации

            Ожидаемый результат:

                1. Присутствует текст 'Registration'
                2. Поля username, email, password, repeat password пусты
                3. Присутствует чекбокс
                4. Присутствует текст 'I accept that I want to be a SDET'
                5. Присутствует кнопка 'Register'
                6. Присутсвтует текст 'Already have an account? Log in'
                5. Присутствует кликабельный текст 'Log in'
        '''
        self.registration_page.check_base_view()

    @pytest.mark.UI
    @allure.epic('Test UI: Registration page')
    @allure.story('Check "Log in" reference')
    def test_go_to_log_in(self):
        '''
            Тестируем кнопку перехода на страницу авторизации

            Шаги:

                1. Переходим на страницу регистрации
                2. Нажимаем на 'Log in'

            Ожидаемый результат:
                
                1. Переход на страницу авторизации
        '''
        self.registration_page.go_to_log_in()
        assert self.base_page.is_opened(self.base_page.url + 'login')

    @pytest.mark.UI
    @allure.epic('Test UI: Registration page')
    @allure.story('Check registratuion without username')
    def test_registration_wo_username(self):
        '''
            Тестируем регистрацию без указания логина

            Шаги:

                1. Переходим на страницу регистрации
                2. Вводим email, password и repeat password (корректные), проставляем чекбокс
                3. Нажимаем на 'Register'

            Ожидаемый результат:
                
                1. Остаемся на странице регистрации
        '''
        username, password, email = self.builder.random_person()

        self.registration_page.send_values(email=email, password=password, repeat_password=password, checkbox=True)
        time.sleep(5)
        self.registration_page.is_opened()

    @pytest.mark.UI
    @allure.epic('Test UI: Registration page')
    @allure.story('Check registratuion without email')
    def test_registration_wo_email(self):
        '''
            Тестируем регистрацию без указания email

            Шаги:

                1. Переходим на страницу регистрации
                2. Вводим username, password и repeat password (корректные), проставляем чекбокс
                3. Нажимаем на 'Register'

            Ожидаемый результат:
                
                1. Остаемся на странице регистрации
        '''
        username, password, email = self.builder.random_person()

        self.registration_page.send_values(username=username, password=password, repeat_password=password, checkbox=True)
        time.sleep(5)
        self.registration_page.is_opened()

    @pytest.mark.UI
    @allure.epic('Test UI: Registration page')
    @allure.story('Check registratuion without password')
    def test_registration_wo_password(self):
        '''
            Тестируем регистрацию без указания password

            Шаги:

                1. Переходим на страницу регистрации
                2. Вводим username, email и repeat password (корректные), проставляем чекбокс
                3. Нажимаем на 'Register'

            Ожидаемый результат:
                
                1. Остаемся на странице регистрации
        '''
        username, password, email = self.builder.random_person()

        self.registration_page.send_values(username=username, email=email, password='', repeat_password=password, checkbox=True)

        time.sleep(5)
        assert self.registration_page.is_opened()

    @pytest.mark.UI
    @allure.epic('Test UI: Registration page')
    @allure.story('Check registratuion without repeat password')
    def test_registration_wo_repeat_password(self):
        '''
            Тестируем регистрацию без указания repeat password

            Шаги:

                1. Переходим на страницу регистрации
                2. Вводим username, password и repeat password (корректные), проставляем чекбокс
                3. Нажимаем на 'Register'

            Ожидаемый результат:
                
                1. Появление ошибки 'Passwords must match'
        '''
        username, password, email = self.builder.random_person()

        self.registration_page.send_values(username=username, email=email, password=password, repeat_password='', checkbox=True)

        time.sleep(1) # Ждем появления ошибки
        assert self.registration_page.find(self.registration_page.locators.TEXT_ERROR_LOCATOR).text == 'Passwords must match'

    @pytest.mark.UI
    @allure.epic('Test UI: Registration page')
    @allure.story('Check registratuion without choosing checkbox')
    def test_registration_wo_checkbox(self):
        '''
            Тестируем регистрацию без проставления чекбокса

            Шаги:

                1. Переходим на страницу регистрации
                2. Вводим username, email, password и repeat password (корректные)
                3. Нажимаем на 'Register'

            Ожидаемый результат:
                
                1. Остаемся на странице регистрации
        '''
        username, password, email = self.builder.random_person()

        self.registration_page.send_values(username=username, email=email, password=password, repeat_password=password, checkbox=False)

        time.sleep(5)
        assert self.registration_page.is_opened()

    @pytest.mark.UI
    @allure.epic('Test UI: Registration page')
    @allure.story('Check registratuion with existent data')
    def test_registration_existent_user(self):
        '''
            Тестируем регистрацию уже существующего пользователя

            Шаги:

                1. Создаем пользователя напрямую в БД
                2. Переходим на страницу регистрации
                3. Вводим username, email, password и repeat password (добавленного пользователя), проставляем чекбокс
                3. Нажимаем на 'Register'

            Ожидаемый результат:
                
                1. Появление ошибки 'User already exist'
        '''
        with allure.step('Generate user and add him to DB'):
            username, password, email = self.builder.random_person()

            self.mysql_builder.create_user(username=username, password=password, email=email)

        self.registration_page.send_values(username=username, email=email, password=password, repeat_password=password, checkbox=True)

        with allure.step('Check error visibility'):
            time.sleep(1) # Ждем появления ошибки
            assert self.registration_page.find(self.registration_page.locators.TEXT_ERROR_LOCATOR).text == 'User already exist'

    @pytest.mark.UI
    @allure.epic('Test UI: Registration page')
    @allure.story('Check registratuion with existent username')
    def test_registration_existent_username(self):
        '''
            Тестируем регистрацию пользователя с уже существующим username

            Шаги:

                1. Создаем пользователя напрямую в БД
                2. Создаем другие email и password
                2. Переходим на страницу регистрации
                3. Вводим username добавленного пользователя
                4. Вводим сгенерированные email, password и repeat password, проставляем чекбокс
                3. Нажимаем на 'Register'

            Ожидаемый результат:
                
                1. Появление ошибки 'User already exist'
        '''
        with allure.step('Generate user and add him to DB'):
            username, password, email = self.builder.random_person()
            self.mysql_builder.create_user(username=username, password=password, email=email, access=1, active=0)

        username_2, password_2, email_2 = self.builder.random_person()

        self.registration_page.send_values(username=username, email=email_2, password=password_2, repeat_password=password_2, checkbox=True)

        with allure.step('Check error visibility'):
            time.sleep(1) # Ждем появления ошибки
            assert self.registration_page.find(self.registration_page.locators.TEXT_ERROR_LOCATOR).text == 'User already exist'

    @pytest.mark.UI
    @allure.epic('Test UI: Registration page')
    @allure.story('Check registratuion with existent email')
    def test_registration_existent_email(self):
        '''
            Тестируем регистрацию пользователя с уже существующим email

            Шаги:

                1. Создаем пользователя напрямую в БД
                2. Создаем другие username и password
                2. Переходим на страницу регистрации
                3. Вводим email добавленного пользователя
                4. Вводим сгенерированные username, password и repeat password, проставляем чекбокс
                3. Нажимаем на 'Register'

            Ожидаемый результат:
                
                1. Какая-либо ошибка, указывающая на невалидный email
        '''
        with allure.step('Generate user and add him to DB'):
            username, password, email = self.builder.random_person()
            self.mysql_builder.create_user(username=username, password=password, email=email, access=1, active=0)

        username_2, password_2, email_2 = self.builder.random_person()

        self.registration_page.send_values(username=username_2, email=email, password=password_2, repeat_password=password_2, checkbox=True)

        with allure.step('Check error visibility'):
            time.sleep(1) # Ждем появления ошибки
            assert self.registration_page.find(self.registration_page.locators.TEXT_ERROR_LOCATOR).text != 'Internal Server Error'

    @pytest.mark.UI
    @allure.epic('Test UI: Registration page')
    @allure.story('Check registratuion with existent password')
    def test_registration_existent_password(self):
        '''
            Тестируем регистрацию пользователя с уже существующим password

            Шаги:

                1. Создаем пользователя напрямую в БД
                2. Создаем другие username и email
                2. Переходим на страницу регистрации
                3. Вводим password и repeat password добавленного пользователя
                4. Вводим сгенерированные username и email, проставляем чекбокс
                3. Нажимаем на 'Register'

            Ожидаемый результат:
                
                1. Переход на главную страницу
        '''
        with allure.step('Generate user and add him to DB'):
            username, password, email = self.builder.random_person()
            self.mysql_builder.create_user(username=username, password=password, email=email)

        username_2, password_2, email_2 = self.builder.random_person()

        self.registration_page.send_values(username=username_2, email=email_2, password=password, repeat_password=password, checkbox=True)

        with allure.step('Check error visibility'):
            assert self.base_page.is_opened(self.base_page.url + 'welcome/')

    @pytest.mark.UI
    @allure.epic('Test UI: Registration page')
    @allure.story('Check registratuion with incorrect username length={length}')
    @pytest.mark.parametrize('length', [1, 2, 3, 4, 5])
    def test_registration_incorrect_username_length(self, length):
        '''
            Тестируем регистрацию пользователя с некорректной длиной логина (<6)

            Шаги:

                1. Переходим на страницу регистрации
                2. Вводим username, email, password и repeat password, проставляем чекбокс
                3. Нажимаем на 'Register'

            Ожидаемый результат:
                
                1. Появление ошибки 'Incorrect username length'
        '''
        username, password, email = self.builder.random_person(username_length=length)

        self.registration_page.send_values(username=username, email=email, password=password, repeat_password=password, checkbox=True)

        with allure.step('Check error visibility'):
            time.sleep(1) # Ждем появления ошибки
            assert self.registration_page.find(self.registration_page.locators.TEXT_ERROR_LOCATOR).text == 'Incorrect username length'

    @pytest.mark.UI
    @allure.epic('Test UI: Registration page')
    @allure.story('Check registratuion with incorrect email length={length}')
    def test_registration_incorrect_email_length(self):
        '''
            Тестируем регистрацию пользователя с некорректной длиной email

            Шаги:

                1. Переходим на страницу регистрации
                2. Вводим username, email, password и repeat password, проставляем чекбокс
                3. Нажимаем на 'Register'

            Ожидаемый результат:
                
                1. Остаемся на странице регистрации
        '''
        pass

    @pytest.mark.UI
    @allure.epic('Test UI: Registration page')
    @allure.story('Check registratuion with incorrect repeat password')
    def test_registration_incorrect_repeat_password(self):
        '''
            Тестируем регистрацию пользователя с некорректным repeat password

            Шаги:

                1. Переходим на страницу регистрации
                2. Генерируем еще один password
                3. Вводим username, email, password и repeat password (сгенерированный во второй раз), проставляем чекбокс
                4. Нажимаем на 'Register'

            Ожидаемый результат:
                
                1. Появление ошибки ''
        '''
        username, password, email = self.builder.random_person()
        password_2 = self.builder.random_password()

        self.registration_page.send_values(username=username, email=email, password=password, repeat_password=password_2, checkbox=True)

        with allure.step('Check error visibility'):
            time.sleep(1) # Ждем появления ошибки
            assert self.registration_page.find(self.registration_page.locators.TEXT_ERROR_LOCATOR).text == 'Passwords must match'

    @pytest.mark.UI
    @allure.epic('Test UI: Registration page')
    @allure.story('Check registratuion with correct data')
    def test_registration(self):
        '''
            Тестируем регистрацию пользователя с корректными данными

            Шаги:

                1. Переходим на страницу регистрации
                2. Вводим username, email, password и repeat password, проставляем чекбокс
                3. Нажимаем на 'Register'

            Ожидаемый результат:
                
                1. Переход на главную страницу
                2. Наличие данных о пользователе в БД
        '''
        username, password, email = self.builder.random_person()

        self.registration_page.send_values(username=username, email=email, password=password, repeat_password=password, checkbox=True)

        self.base_page.is_opened(self.base_page.url + 'welcome/')

        user = self.mysql_builder.get_user_by_username(username=username)[0]

        assert user.username == username
        assert user.password == password
        assert user.email == email
        assert user.access == 1
        assert user.active == 1
        assert user.start_active_time is not None


class TestUIMainPage(UIBase):
    '''
        Тестирование главной страницы
        (тесты используют куки, первоначальная страница - главная)
    '''
    @pytest.fixture(scope='session')
    def cookies(self, config, mysql_builder, builder):
        driver = get_driver(config)
        driver.get(config['url'])
        
        authorization_page = AuthorizationPage(driver, config)

        username, password, email = builder.random_person()
        mysql_builder.create_user(username=username, password=password, email=email, access=1, active=0)
        authorization_page.send_values(username=username, password=password)

        cookies = driver.get_cookies()
        driver.quit()
        return cookies

    @pytest.fixture(scope='function', autouse=True)
    def setup_authorized(self, cookies, request):
        if 'noautofixt' in request.keywords:
            return
        for cookie in cookies:
            if cookie.get('domain') is not None:
                cookie.pop('domain')
            self.driver.add_cookie(cookie)
        self.driver.refresh()
        # time.sleep(0.1)

    @pytest.fixture(scope='session')
    def cookies_w_username(self, config, mysql_builder, builder):
        driver = get_driver(config)
        driver.get(config['url'])
        
        authorization_page = AuthorizationPage(driver, config)

        username, password, email = builder.random_person()
        mysql_builder.create_user(username=username, password=password, email=email, access=1, active=0)
        authorization_page.send_values(username=username, password=password)

        cookies = driver.get_cookies()
        driver.quit()

        return (cookies, username)

    @pytest.fixture(scope='function', autouse=False)
    def setup_authorized_w_username(self, cookies_w_username):
        cookies = cookies_w_username[0]
        username = cookies_w_username[1]

        for cookie in cookies:
            if cookie.get('domain') is not None:
                cookie.pop('domain')
            self.driver.add_cookie(cookie)
        self.driver.refresh()
        # time.sleep(0.1)
        
        return username
    
    @pytest.mark.UI
    @allure.epic('Test UI: Main page')
    @allure.story('Check base view of page')
    @pytest.mark.noautofixt
    def test_base_view(self, setup_authorized_w_username):
        '''
            Тестируем наличие всех элементов на странице

            Шаги:

                0. Переходим на главную страницу

            Ожидаемый результат:

                1. Присутствует картинка 'Bug'
                2. Присутствует кнопка с надписью 'TM version 0.1'
                3. Присутствует кнопка с надписью 'HOME'
                4. Присутствует кнопка с надписью 'Python'
                5. Присутствует кнопка с надписью 'Linux'
                6. Присутствует кнопка с надписью 'Network'
                7. Присутствует надпись 'Logged as <username>'
                8. Присутствует кнопка с надписью 'Logout'
                9. Присутствует надпись 'What is an API?'
                10. Присутствует надпись 'Future of internet'
                11. Присутствует надпись 'Lets talk about SMTP?'
                12. Присутствует кнопка 'What is an API?'
                13. Присутствует кнопка 'Future of internet'
                14. Присутствует кнопка 'Lets talk about SMTP?'
                15. Присутствует надпись 'powered by ТЕХНОАТОМ'
                16. Присутствует не пустая надпись с цитатой
        '''
        self.main_page.check_base_view(setup_authorized_w_username)

    @pytest.mark.UI
    @allure.epic('Test UI: Main page')
    @allure.story('Check "Brand" button')
    def test_go_to_brand(self):
        '''
            Тестируем кнопку 'TM version 0.1'

            Шаги:

                0. Переходим на главную страницу
                1. Нажимаем на 'TM version 0.1'

            Ожидаемый результат:
                
                1. Переход на главную страницу
        '''
        self.main_page.click(self.main_page.locators.HREF_BRAND_LOCATOR)
        self.base_page.is_opened(url=self.base_page.url + 'welcome/')

    @pytest.mark.UI
    @allure.epic('Test UI: Main page')
    @allure.story('Check "HOME" button')
    def test_go_to_home(self):
        '''
            Тестируем кнопку 'HOME'

            Шаги:

                0. Переходим на главную страницу
                1. Нажимаем на 'HOME'

            Ожидаемый результат:
                
                1. Переход на главную страницу
        '''
        self.main_page.click(self.main_page.locators.BUTTON_HOME_LOCATOR)
        self.base_page.is_opened(url=self.base_page.url + 'welcome/')

    @pytest.mark.UI
    @allure.epic('Test UI: Main page')
    @allure.story('Check "Python" button')
    def test_go_to_python(self):
        '''
            Тестируем кнопку 'Python'

            Шаги:

                0. Переходим на главную страницу
                1. Нажимаем на 'Python'

            Ожидаемый результат:
                
                1. Переход на python.org
        '''
        self.main_page.click(self.main_page.locators.BUTTON_PYTHON_LOCATOR)
        self.base_page.is_opened(url='https://www.python.org/')
    
    @pytest.mark.UI
    @allure.epic('Test UI: Main page')
    @allure.story('Check "Python: Python history" button')
    def test_go_to_python_history(self):
        '''
            Тестируем кнопку 'Python: Python history'

            Шаги:

                0. Переходим на главную страницу
                1. Наводим указатель на 'Python'
                2. Наводим указатель на Python history и нажимаем на эту кнопку

            Ожидаемый результат:
                
                1. Переход на https://en.wikipedia.org/wiki/History_of_Python
        '''
        python_button = self.main_page.find(self.main_page.locators.BUTTON_PYTHON_LOCATOR)
        history = self.main_page.find(self.main_page.locators.BUTTON_PYTHON_HISTORY_LOCATOR)
        self.main_page.action_chains.move_to_element(python_button).move_to_element(history).click().perform()
        
        self.main_page.is_opened(url='https://en.wikipedia.org/wiki/History_of_Python')

    @pytest.mark.UI
    @allure.epic('Test UI: Main page')
    @allure.story('Check "Python: About Flask" button')
    def test_go_to_python_about_flask(self):
        '''
            Тестируем кнопку 'Python: About Flask'

            Шаги:

                0. Переходим на главную страницу
                1. Наводим указатель на 'Python'
                2. Наводим указатель на About Flask и нажимаем на эту кнопку

            Ожидаемый результат:
                
                1. Переход на https://flask.palletsprojects.com/en/1.1.x/#
        '''
        python_button = self.main_page.find(self.main_page.locators.BUTTON_PYTHON_LOCATOR)
        about_flask = self.main_page.find(self.main_page.locators.BUTTON_PYTHON_ABOUT_FLASK_LOCATOR)
        self.main_page.action_chains.move_to_element(python_button).move_to_element(about_flask).click().perform()
        
        new_tab = self.driver.window_handles[1]
        
        self.driver.switch_to.window(new_tab)
        
        self.main_page.is_opened(url='https://flask.palletsprojects.com/en/1.1.x/#')
    
    @pytest.mark.UI
    @allure.epic('Test UI: Main page')
    @allure.story('Check "Download Centos7" button')
    def test_go_to_linux_download_centos(self):
        '''
            Тестируем кнопку 'Download Centos7'

            Шаги:

                0. Переходим на главную страницу
                1. Нажимаем на кнопку 'Linux'
                2. Нажимаем на кнопку 'Download Centos7'

            Ожидаемый результат:
                
                1. Переход на https://getfedora.org/ru/workstation/download/ в новой вкладке
        '''
        self.main_page.click(self.main_page.locators.BUTTON_LINUX_LOCATOR)
        self.main_page.click(self.main_page.locators.BUTTON_LINUX_DOWNLOAD_CENTOS_LOCATOR)

        new_tab = self.driver.window_handles[1]
        
        self.driver.switch_to.window(new_tab)
        
        assert self.base_page.is_opened(url='https://getfedora.org/ru/workstation/download/')
    
    @pytest.mark.UI
    @allure.epic('Test UI: Main page')
    @allure.story('Check "Network: NEWS" button')
    def test_go_to_network_news(self):
        '''
            Тестируем кнопку 'Network: NEWS'

            Шаги:

                0. Переходим на главную страницу
                1. Нажимаем на кнопку 'Network'
                2. Нажимаем на кнопку 'NEWS'

            Ожидаемый результат:
                
                1. Переход на https://www.wireshark.org/news/ в новой вкладке
        '''
        self.main_page.click(self.main_page.locators.BUTTON_NETWORK_LOCATOR)
        self.main_page.click(self.main_page.locators.BUTTON_NETWORK_NEWS_LOCATOR)

        new_tab = self.driver.window_handles[1]
        self.driver.switch_to.window(new_tab)
        
        assert self.base_page.is_opened(url='https://www.wireshark.org/news/')

    @pytest.mark.UI
    @allure.epic('Test UI: Main page')
    @allure.story('Check "Network: DOWNLOAD" button')
    def test_go_to_network_download(self):
        '''
            Тестируем кнопку 'Network: DOWNLOAD'

            Шаги:

                0. Переходим на главную страницу
                1. Нажимаем на кнопку 'Network'
                2. Нажимаем на кнопку 'DOWNLOAD'

            Ожидаемый результат:
                
                1. Переход на https://www.wireshark.org/#download в новой вкладке
        '''
        self.main_page.click(self.main_page.locators.BUTTON_NETWORK_LOCATOR)
        self.main_page.click(self.main_page.locators.BUTTON_NETWORK_DOWNLOAD_LOCATOR)

        new_tab = self.driver.window_handles[1]
        self.driver.switch_to.window(new_tab)
        
        assert self.base_page.is_opened(url='https://www.wireshark.org/#download')

    @pytest.mark.UI
    @allure.epic('Test UI: Main page')
    @allure.story('Check "Network: EXAMPLES" button')
    def test_go_to_network_examples(self):
        '''
            Тестируем кнопку 'Network: EXAMPLES'

            Шаги:

                0. Переходим на главную страницу
                1. Нажимаем на кнопку 'Network'
                2. Нажимаем на кнопку 'EXAMPLES'

            Ожидаемый результат:
                
                1. Переход на https://hackertarget.com/tcpdump-examples/ в новой вкладке
        '''
        self.main_page.click(self.main_page.locators.BUTTON_NETWORK_LOCATOR)
        self.main_page.click(self.main_page.locators.BUTTON_NETWORK_EXAMPLES_LOCATOR)

        new_tab = self.driver.window_handles[1]
        self.driver.switch_to.window(new_tab)
        
        assert self.base_page.is_opened(url='https://hackertarget.com/tcpdump-examples/')
        
    @pytest.mark.UI
    @allure.epic('Test UI: Main page')
    @allure.story('Check "What is an API?" button')
    def test_go_to_API(self):
        '''
            Тестируем кнопку 'What is an API?'

            Шаги:

                0. Переходим на главную страницу
                1. Нажимаем на кнопку 'What is an API?'

            Ожидаемый результат:
                
                1. Переход на https://en.wikipedia.org/wiki/API в новой вкладке
        '''
        self.main_page.click(self.main_page.locators.BUTTON_API_LOCATOR)

        new_tab = self.driver.window_handles[1]
        self.driver.switch_to.window(new_tab)
        
        assert self.base_page.is_opened(url='https://en.wikipedia.org/wiki/API')

    @pytest.mark.UI
    @allure.epic('Test UI: Main page')
    @allure.story('Check "Future of internet" button')
    def test_go_to_future_of_internet(self):
        '''
            Тестируем кнопку 'Future of internet'

            Шаги:

                0. Переходим на главную страницу
                1. Нажимаем на кнопку 'Future of internet'

            Ожидаемый результат:
                
                1. Переход на https://www.popularmechanics.com/technology/infrastructure/a29666802/future-of-the-internet/ в новой вкладке
        '''
        self.main_page.click(self.main_page.locators.BUTTON_FUTURE_LOCATOR)

        new_tab = self.driver.window_handles[1]
        
        self.driver.switch_to.window(new_tab)
        
        assert self.base_page.is_opened(url='https://www.popularmechanics.com/technology/infrastructure/a29666802/future-of-the-internet/')

    @pytest.mark.UI
    @allure.epic('Test UI: Main page')
    @allure.story('Check "Lets talk about SMTP?" button')
    def test_go_to_SMTP(self):
        '''
            Тестируем кнопку 'Lets talk about SMTP?'

            Шаги:

                0. Переходим на главную страницу
                1. Нажимаем на кнопку 'Lets talk about SMTP?'

            Ожидаемый результат:
                
                1. Переход на https://ru.wikipedia.org/wiki/SMTP в новой вкладке
        '''
        self.main_page.click(self.main_page.locators.BUTTON_SMTP_LOCATOR)

        new_tab = self.driver.window_handles[1]
        
        self.driver.switch_to.window(new_tab)
        
        assert self.base_page.is_opened(url='https://ru.wikipedia.org/wiki/SMTP')

    @pytest.mark.UI
    @allure.epic('Test UI: Main page')
    @allure.story('Check "Logout" button')
    @pytest.mark.noautofixt
    def test_logout(self):
        '''
            Тестируем кнопку 'Logout'

            Шаги:

                0. Переходим на главную страницу
                1. Нажимаем на кнопку 'Logout'

            Ожидаемый результат:
                
                1. Переход на /login
                2. У пользователя в БД active = 0
        '''
        username, password, email = self.builder.random_person()

        with allure.step('Registrate new user'):
            self.registration_page.driver.get(self.registration_page.url)
            self.registration_page.send_values(username=username, email=email, password=password, repeat_password=password, checkbox=True)

        self.main_page.click(self.main_page.locators.BUTTON_LOGOUT_LOCATOR)

        self.base_page.is_opened(url=self.base_page.url + 'login')
        with allure.step('Check database content:'):
            user = self.mysql_builder.get_user_by_username(username=username)[0]
            assert user.access == 1
            assert user.active == 0

    @pytest.mark.UI
    @allure.epic('Test UI: Main page')
    @allure.story('Test block user while he is active')
    @pytest.mark.noautofixt
    def test_block_user(self):
        '''
            Тестируем кнопку блокировку пользователя, когда он на странице

            Шаги:

                0. Переходим на главную страницу
                1. Блокируем пользователя
                2. Проверяем, что пользователя разлогинило и полявилась ошибка

            Ожидаемый результат:
                
                1. Переход на /login?next=/welcome/
                2. Появление ошибки 'This page is available only to authorized users'
                3. У пользователя в БД active = 0, access = 0
        '''
        username, password, email = self.builder.random_person()

        with allure.step('Registrate new user'):
            self.registration_page.driver.get(self.registration_page.url)
            self.registration_page.send_values(username=username, email=email, password=password, repeat_password=password, checkbox=True)

        with allure.step('Make user access = 0'):
            self.mysql_builder.update_user(username=username, data_to_update={'access': 0})

        with allure.step('Check error'):
            self.driver.refresh()
            
            assert self.main_page.is_opened(self.config['url'] + '/login?next=/welcome/')
            error = self.authorization_page.find(self.authorization_page.locators.TEXT_ERROR_LOCATOR)
            assert error.text == 'This page is available only to authorized users'

        with allure.step('Check database content'):
            user = self.mysql_builder.get_user_by_username(username=username)[0]

            assert user.access == 0
            assert user.active == 0

    @pytest.mark.UI
    @allure.epic('Test UI: Main page')
    @allure.story('Test deactivate user while he is active')
    @pytest.mark.noautofixt
    def test_deactivate_user(self):
        '''
            Тестируем кнопку деактивацию пользователя, когда он на странице

            Шаги:

                0. Переходим на главную страницу
                1. Блокируем пользователя
                2. Проверяем, что пользователя разлогинило и полявилась ошибка

            Ожидаемый результат:
                
                1. Переход на /login?next=/welcome/
                2. Появление ошибки 'This page is available only to authorized users'
                3. У пользователя в БД active = 0, access = 0
        '''
        username, password, email = self.builder.random_person()

        with allure.step('Registrate new user'):
            self.registration_page.driver.get(self.registration_page.url)
            self.registration_page.send_values(username=username, email=email, password=password, repeat_password=password, checkbox=True)

        with allure.step('Make user active = 0'):
            self.mysql_builder.update_user(username=username, data_to_update={'active': 0})

        with allure.step('Check error'):
            self.driver.refresh()
            
            assert self.main_page.is_opened(self.config['url'] + '/login?next=/welcome/')
            error = self.authorization_page.find(self.authorization_page.locators.TEXT_ERROR_LOCATOR)
            assert error.text == 'This page is available only to authorized users'

        with allure.step('Check database content'):
            user = self.mysql_builder.get_user_by_username(username=username)[0]
            assert user.access == 1
            assert user.active == 0


class TestUIVkIdentifier(UIBase):
    '''
        Тестирование появления значка привязанности к VK
    '''
    @pytest.fixture(scope='function', autouse=True)
    def setup_vk_client(self, mock_client):
        self.mock_client: MockClient = mock_client

    @pytest.mark.UI
    @allure.epic('Test UI: Main page: VK Identifier')
    @allure.story('Test user without VK')
    def test_wo_vk(self):
        '''
            Тестируем вход без привязки к VK

        Шаги:

            0. Переходим на главную страницу
            1. Проверяем отсутствие значка

        Ожидаемый результат:
                
            1. Отсутствие идентификатора
        '''
        with allure.step('Add new user in DB and login'):
            username, password, email = self.builder.random_person()
            self.mysql_builder.create_user(username=username, password=password, email=email)

            self.authorization_page.send_values(username=username, password=password)

        with allure.step('Check Identifier'):
            if self.main_page.find(self.main_page.locators.VK_ID_LOCATOR).text != '':
                assert False

    @pytest.mark.UI
    @allure.epic('Test UI: Main page: VK Identifier')
    @allure.story('Test user with VK')
    def test_w_vk(self):
        '''
            Тестируем вход с привязкой к VK

        Шаги:

            0. Переходим на главную страницу
            1. Проверяем наличие значка

        Ожидаемый результат:
                
            1. Наличие идентификатора
        '''
        username, password, email = self.builder.random_person()
        
        with allure.step('Add new user in VK mock'):
            vk_id = self.builder.random_str(length=5)
            self.mock_client.add_user(username=username, vk_id=vk_id)

        
        with allure.step('Add new user in DB and login'):
            self.mysql_builder.create_user(username=username, password=password, email=email)
            self.authorization_page.send_values(username=username, password=password)

        with allure.step('Check Identifier'):
            assert self.main_page.find(self.main_page.locators.VK_ID_LOCATOR).text == f'VK ID: {vk_id}'