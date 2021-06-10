import pytest
from _pytest.fixtures import FixtureRequest

import allure

from api.client import ApiClient
from mysql.builder import MySQLBuilder

from base_tests.base.base import BaseCase


class ApiBase(BaseCase):
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, api_client):
        self.api_client: ApiClient = api_client

    def check_db(self, user, username, password, email, access=1, active=0, start_active_time=None):
            assert user.username == username
            assert user.password == password
            assert user.email == email
            assert user.access == access
            assert user.active == active
            if start_active_time is None:
                assert user.start_active_time is None 
            else:
                assert user.start_active_time == start_active_time


class ApiBaseAuthorized(ApiBase):
    @pytest.fixture(scope='session')
    def cookies(self, config, mysql_builder):
        api_client = ApiClient(config['app_host'], config['app_port'])
        
        cookies = api_client.create_admin()
        return cookies
        
        # mysql_builder.delete_user('ADMINETOYA')

    @pytest.fixture(scope='function', autouse=True)
    def setup_authorized(self, cookies, request):
        self.api_client.admin_cookie = cookies


class TestApiAdd(ApiBaseAuthorized):

    '''
       Важно отметить, что нет какого-либо отдельного юзера-админа(или я чего-то не понял),
       поэтому перед действиями с api необходимо "вручную" зарегистрировать клиента через "/reg",
       после чего взять сессионную куку и проводить тестирование api.
       Из этой логики делаем следующее:
       1. Тестируем апи без сессионной куки(в этом случае ожидаемый код 401)
       2. Тестируем api с сессионной кукой (для этого создаем пользователя admin с паролем 1234567 и от его имени тестируем api)
    '''

        
    '''
        Тестирование добавления пользователя
    '''

    @pytest.mark.API
    @allure.epic('Test Api: /api/add_user')
    @allure.story('Add user with valid username, password and email')
    def test_add_user(self):
        '''
            Тестируем валидное добавление пользователя.
            
            Шаги:
                1. Генерируем случайного пользователя
                2. Делаем POST запрос согласно API;
                3. Проверяем статус-код ответа;
                4. Проверяем, что пользователь корректно добавлен в БД.
            
            Ожидаемый результат:
                1. Статус код == 201;
                2. Наличие данных о пользователе в БД.
        '''

        with allure.step('Generate user and add him via API'):
            username, password, email = self.builder.random_person()

            response = self.api_client.post_add_user(username=username, password=password, email=email)
        
        with allure.step('Check status code'):
            assert response.status_code ==  201

        with allure.step('Check database content'):
            db_data = self.mysql_builder.get_user_by_username(username=username)
        
            assert len(db_data) == 1
            
            user = db_data[0]

            self.check_db(user, username, password, email, access=1, active=0, start_active_time=None)

    @pytest.mark.API
    @allure.epic('Test Api: /api/add_user')
    @allure.story('Add user with existent username')
    def test_add_existent_username(self):
        '''
            Тестируем валидное добавление пользователя с уже существующим username.
            
            Шаги:
                1. Генерируем двух пользователей
                1. Добавляем первого пользователя напрямую в БД;
                1. Добавляем другого пользователя с одинаковым username с помощью API;
                2. Проверяем статус-код ответа;
                3. Проверяем, что пользователь не добавлен в БД.
            
            Ожидаемый результат:
                1. Статус код == 304;
                2. Отсутствие изменений в данных первого пользователя в БД
                2. Отсутствие данных другого пользователя в БД.
        '''

        with allure.step('Generate users and add them via MySqlBuilder and API'):
            username, password, email = self.builder.random_person()

            username_2, password_2, email_2 = self.builder.random_person()
        
            self.mysql_builder.create_user(username=username, password=password, email=email)
            
            response = self.api_client.post_add_user(username=username, password=password_2, email=email_2)
        
        with allure.step('Check status code'):        
            assert response.status_code == 304

        with allure.step('Check database content'):
            db_data = self.mysql_builder.get_user_by_username(username=username)
        
            assert len(db_data) == 1

            user = db_data[0]

            self.check_db(user, username, password, email, access=1, active=0, start_active_time=None)

            assert len(self.mysql_builder.get_user_by_password(password=password_2)) == 0
            assert len(self.mysql_builder.get_user_by_email(email=email_2)) == 0
    
    @pytest.mark.API
    @allure.epic('Test Api: /api/add_user')
    @allure.story('Add user with existent password')
    def test_add_existent_password(self):
        '''
            Тестируем добавление пользователя с паролем уже существующего пользователя.
            
            Шаги:
                1. Генерируем и добавляем пользователя напрямую в БД
                2. Генерируем и добавляем другого пользователя с таким же паролем с помощью API
                3. Проверяем статус код
                4. Проверяем, что другой пользователь добавлен в БД, а данные первого - не изменены
            
            Ожидаемый результат:
                1. Статус код == 201
                2. Наличие данных о втором пользователе в БД
        '''
        with allure.step('Generate users and add them via MySqlBuilder and API'):
            username, password, email = self.builder.random_person()

            username_2, password_2, email_2 = self.builder.random_person()
        
            self.mysql_builder.create_user(username=username, password=password, email=email)
            
            response = self.api_client.post_add_user(username=username_2, password=password, email=email_2)
                
        with allure.step('Check status code'):        
            assert response.status_code == 201
        
        with allure.step('Check database content'):
            db_data_1 = self.mysql_builder.get_user_by_username(username=username)
            db_data_2 = self.mysql_builder.get_user_by_username(username=username_2)

            assert len(db_data_1) == 1
            assert len(db_data_2) == 1

            user_1 = db_data_1[0]
            user_2 = db_data_2[0]

            self.check_db(user_1, username, password, email, access=1, active=0, start_active_time=None)
            self.check_db(user_2, password, email_2, access=1, active=0, start_active_time=None)
        
    @pytest.mark.API
    @allure.epic('Test Api: /api/add_user')
    @allure.story('Add user with existent email')
    def test_add_existent_email(self):
        '''
            Тестируем добавление пользователя с email уже существующего пользователя.
            
            Шаги:

                1. Генерируем и добавляем пользователя напрямую в БД
                2. Генерируем и добавляем другого пользователя с email первого пользователя 
                3. Проверяем статус код запроса
                4. Проверяем отсутствие данных второго пользователя в БД
            
            Ожидаемый результат:

                1. Статус код == 304
                2. Данные первого пользователя не изменены
                3. Данные второго пользователя отсутствуют в БД
        '''
        with allure.step('Generate users and add them via MySqlBuilder and API'):
            username, password, email = self.builder.random_person()

            username_2, password_2, email_2 = self.builder.random_person()
        
            self.mysql_builder.create_user(username=username, password=password, email=email)
            
            response = self.api_client.post_add_user(username=username_2, password=password_2, email=email)
        
        with allure.step('Check status code'):        
            assert response.status_code == 304

        with allure.step('Check database content'):
            db_data = self.mysql_builder.get_user_by_email(email=email)

            assert len(db_data) == 1

            user = db_data[0]

            self.check_db(user, username, password, email, access=1, active=0, start_active_time=None)

            assert len(self.mysql_builder.get_user_by_username(username=username_2)) == 0
            assert len(self.mysql_builder.get_user_by_password(password=password_2)) == 0

    @pytest.mark.API
    @allure.epic('Test Api: /api/add_user')
    @allure.story('Add user with invalid username')
    @pytest.mark.parametrize('length', range(6))
    def test_add_invalid_username(self, length):
        '''
            Тестируем добавление пользователя с невалидным username (длина < 6).
            
            Шаги:

                1. Добавляем пользователя с невалидным логином с помощью API
                2. Проверяем статус код
                3. Проверяем отсутствие данных добавленного пользователя в БД
            
            Ожидаемый результат:
                
                1. Статус код == 400
                2. Отсутствие данных пользователя в БД
        '''
        with allure.step('Generate user and add him via API'):
            username, password, email = self.builder.random_person(username_length=length)

            response = self.api_client.post_add_user(username=username, password=password, email=email)
        
        with allure.step('Check status code'):        
            assert response.status_code == 400

        with allure.step('Check database content'):
            assert len(self.mysql_builder.get_user_by_username(username=username)) == 0
            assert len(self.mysql_builder.get_user_by_password(password=password)) == 0
            assert len(self.mysql_builder.get_user_by_email(email=email)) == 0

    @pytest.mark.API
    @allure.epic('Test Api: /api/add_user')
    @allure.story('Add user with invalid email')
    def test_add_invalid_email(self):
        '''
            Тестируем добавление пользователя с невалидным email (отсутствие @_._).
            
            Шаги:

                1. Добавляем пользователя с невалидным email с помощью API
                2. Проверяем статус код
                3. Проверяем отсутствие данных добавленного пользователя в БД

            Ожидаемый результат:

                1. Статус код == 400
                2. Отсутствие данных добавленного пользователя в БД
        '''
        with allure.step('Generate user and add him via API'):
            username, password, email = self.builder.random_person(username_length=5)
            email = self.builder.random_str()

            response = self.api_client.post_add_user(username=username, password=password, email=email)
        
        with allure.step('Check status code'):
            assert response.status_code == 400
            
        with allure.step('Check database content'):
            assert len(self.mysql_builder.get_user_by_username(username=username)) == 0
            assert len(self.mysql_builder.get_user_by_password(password=password)) == 0
            assert len(self.mysql_builder.get_user_by_email(email=email)) == 0

    @pytest.mark.API
    @allure.epic('Test Api: /api/add_user')
    @allure.story('Add user without login')
    def test_add_wo_login(self):
        '''
            Тестируем добавление пользователя без логина.
            
            Шаги:

                1. Добавляем пользователя без логина с помощью API
                2. Проверяем статус код
                3. Проверяем отсутствие данных добавленного пользователя в БД

            Ожидаемый результат:

                1. Статус код == 400
                2. Отсутствие данных добавленного пользователя в БД
        '''
        with allure.step('Generate user and add him via API'):
            username, password, email = self.builder.random_person(username_length=5)
            email = self.builder.random_str()

            response = self.api_client.post_add_user(username='', password=password, email=email)
        
        with allure.step('Check status code'):
            assert response.status_code == 400
            
        with allure.step('Check database content'):
            assert len(self.mysql_builder.get_user_by_password(password=password)) == 0
            assert len(self.mysql_builder.get_user_by_email(email=email)) == 0

    @pytest.mark.API
    @allure.epic('Test Api: /api/add_user')
    @allure.story('Add user without password')
    def test_add_wo_password(self):
        '''
            Тестируем добавление пользователя без пароля.
            
            Шаги:

                1. Добавляем пользователя без пароля с помощью API
                2. Проверяем статус код
                3. Проверяем отсутствие данных добавленного пользователя в БД

            Ожидаемый результат:

                1. Статус код == 400
                2. Отсутствие данных добавленного пользователя в БД
        '''
        with allure.step('Generate user and add him via API'):
            username, password, email = self.builder.random_person(username_length=5)
            email = self.builder.random_str()

            response = self.api_client.post_add_user(username=username, password='', email=email)
        
        with allure.step('Check status code'):
            assert response.status_code == 400
            
        with allure.step('Check database content'):
            assert len(self.mysql_builder.get_user_by_username(username=username)) == 0
            assert len(self.mysql_builder.get_user_by_email(email=email)) == 0

    @pytest.mark.API
    @allure.epic('Test Api: /api/add_user')
    @allure.story('Add user without email')
    def test_add_wo_email(self):
        '''
            Тестируем добавление пользователя без email.
            
            Шаги:

                1. Добавляем пользователя без email с помощью API
                2. Проверяем статус код
                3. Проверяем отсутствие данных добавленного пользователя в БД

            Ожидаемый результат:

                1. Статус код == 400
                2. Отсутствие данных добавленного пользователя в БД
        '''
        with allure.step('Generate user and add him via API'):
            username, password, email = self.builder.random_person(username_length=5)
            email = self.builder.random_str()

            response = self.api_client.post_add_user(username=username, password=password, email='')
        
        with allure.step('Check status code'):
            assert response.status_code == 400
            
        with allure.step('Check database content'):
            assert len(self.mysql_builder.get_user_by_username(username=username)) == 0
            assert len(self.mysql_builder.get_user_by_password(password=password)) == 0


class TestApiDel(ApiBaseAuthorized):
    
    '''
        Тестирование удаления пользователя
    '''
    
    @pytest.mark.API
    @allure.epic('Test API: /api/del_user/<username>')
    @allure.story('Delete existent user')
    def test_delete_existent_user(self):
        '''
            Тестируем удаление существующего пользователя.
            
            Шаги:

                1. Добавляем пользователя напрямую в БД
                2. Удаляем его с помощью API
                2. Проверяем статус код
                3. Проверяем отсутствие данных добавленного пользователя в БД

            Ожидаемый результат:

                1. Статус код == 204
                2. Отсутствие данных добавленного пользователя в БД
        '''
        with allure.step('Generate user and add him to DB, then delete him via API'):
            username, password, email = self.builder.random_person()
            
            self.mysql_builder.create_user(username=username, password=password, email=email)

            response = self.api_client.get_del_user(username=username)
        
        with allure.step('Check status code'):
            assert response.status_code == 204
        
        with allure.step('Check database content'):
            assert len(self.mysql_builder.get_user_by_username(username=username)) == 0
            assert len(self.mysql_builder.get_user_by_password(password=password)) == 0
            assert len(self.mysql_builder.get_user_by_email(email=email)) == 0

    @pytest.mark.API
    @allure.epic('Test API: /api/del_user/<username>')
    @allure.story('Delete non existent user')
    def test_delete_non_existent_user(self):
        '''
            Тестируем удаление несуществующего пользователя.
            
            Шаги:

                1. Удаляем несуществуюшего пользователя его с помощью API
                2. Проверяем статус код
                3. Проверяем отсутствие данных удаляемого пользователя в БД

            Ожидаемый результат:

                1. Статус код == 404
                2. Отсутствие данных добавленного пользователя в БД
        '''
        with allure.step('Generate user and try delete him via API'):
            username = self.builder.random_username()

            response = self.api_client.get_del_user(username=username)

        with allure.step('Check status code'):
            assert response.status_code == 404

        with allure.step('Check database content'):
            assert len(self.mysql_builder.get_user_by_username(username=username)) == 0

    @pytest.mark.API
    @allure.epic('Test API: /api/del_user/<username>')
    @allure.story('Delete existent user by email')
    def test_delete_by_email(self):
        '''
            Тестируем удаление существующего пользователя через его email.
            
            Шаги:

                1. Удаляем существуюшего пользователя его с помощью API используя его email
                2. Проверяем статус код
                3. Проверяем присутствие данных удаляемого пользователя в БД

            Ожидаемый результат:

                1. Статус код == 404
                2. Присутствие данных добавленного пользователя в БД
        '''
        with allure.step('Generate user and try delete him via API by his email'):
            username, password, email = self.builder.random_person()
            
            self.mysql_builder.create_user(username=username, password=password, email=email)

            response = self.api_client.get_del_user(username=email)

        with allure.step('Check status code'):
            assert response.status_code == 404

        with allure.step('Check database content'):
            db_data = self.mysql_builder.get_user_by_username(username=username)
        
            assert len(db_data) == 1
            
            user = db_data[0]

            self.check_db(user, username, password, email, access=1, active=0, start_active_time=None)

    @pytest.mark.API
    @allure.epic('Test API: /api/del_user/<username>')
    @allure.story('Delete existent user by password')
    def test_delete_by_password(self):
        '''
            Тестируем удаление существующего пользователя через его пароль.
            
            Шаги:

                1. Удаляем существуюшего пользователя его с помощью API используя его пароль
                2. Проверяем статус код
                3. Проверяем присутствие данных удаляемого пользователя в БД

            Ожидаемый результат:

                1. Статус код == 404
                2. Присутствие данных добавленного пользователя в БД
        '''
        with allure.step('Generate user and try delete him via API by his password'):
            username, password, email = self.builder.random_person()
            
            self.mysql_builder.create_user(username=username, password=password, email=email)

            response = self.api_client.get_del_user(username=password)

        with allure.step('Check status code'):
            assert response.status_code == 404

        with allure.step('Check database content'):
            db_data = self.mysql_builder.get_user_by_username(username=username)
        
            assert len(db_data) == 1
            
            user = db_data[0]

            self.check_db(user, username, password, email, access=1, active=0, start_active_time=None)


class TestApiBlock(ApiBaseAuthorized):
    
    '''
        Тестирование блокировки пользователя
    '''
    
    @pytest.mark.API
    @allure.epic('Test API: /api/block_user/<username>')
    @allure.story('Block existent user with access = 0')
    def test_block_existent_user_w_access_0(self):
        '''
            Тестируем блокирование существующего пользователя через его username, когда его access = 0.
            
            Шаги:
                1. Создаем напрямую в БД пользователя с access = 0
                2. Блокируем его с помощью API
                2. Проверяем статус код
                3. Проверяем значение access у данного пользователяче 

            Ожидаемый результат:

                1. Статус код == 304
                2. Присутствие данных добавленного пользователя в БД
                3. У данного пользователя access == 0
        '''
        with allure.step('Generate user with access = 0 and block him via API'):
            username, password, email = self.builder.random_person()

            self.mysql_builder.create_user(username=username, password=password, email=email, access=0)
            
            response = self.api_client.get_block_user(username=username)
        
        with allure.step('Check status code'):
            assert response.status_code == 304

        with allure.step('Check database content'):
            db_data = self.mysql_builder.get_user_by_username(username=username)
        
            assert len(db_data) == 1
            
            user = db_data[0]

            self.check_db(user, username, password, email, access=0, active=0, start_active_time=None)

    @pytest.mark.API
    @allure.epic('Test API: /api/block_user/<username>')
    @allure.story('Block existent user with access = 1')
    def test_block_existent_user_w_access_1(self):
        '''
            Тестируем блокирование существующего пользователя через его username, когда его access = 1.
            
            Шаги:
                1. Создаем напрямую в БД пользователя с access = 1
                2. Блокируем его с помощью API
                2. Проверяем статус код
                3. Проверяем значение access у данного пользователя

            Ожидаемый результат:

                1. Статус код == 200
                2. Присутствие данных добавленного пользователя в БД
                3. У данного пользователя access == 0
        '''
        with allure.step('Generate user with access = 1 and block him via API'):
            username, password, email = self.builder.random_person()

            self.mysql_builder.create_user(username=username, password=password, email=email, access=1)
            
            response = self.api_client.get_block_user(username=username)
        
        with allure.step('Check status code'):
            assert response.status_code == 200

        with allure.step('Check database content'):
            db_data = self.mysql_builder.get_user_by_username(username=username)
        
            assert len(db_data) == 1
            
            user = db_data[0]

            self.check_db(user, username, password, email, access=0, active=0, start_active_time=None)

    @pytest.mark.API
    @allure.epic('Test API: /api/block_user/<username>')
    @allure.story('Block non existent user')
    def test_block_non_existent_user(self):
        '''
            Тестируем блокирование несуществующего пользователя.
            
            Шаги:
                1. Блокируем несушествующего пользователя с помощью API
                2. Проверяем статус код
                3. Проверяем отсутствие данных пользователя в БД

            Ожидаемый результат:

                1. Статус код == 404
                2. Отсутствие данных пользователя в БД
        '''
        with allure.step('Generate user, do not add him to DB and try blocking him via API'):
            username = self.builder.random_username()

            response = self.api_client.get_block_user(username=username)

        with allure.step('Check status code'):
            assert response.status_code == 404
        
        with allure.step('Check database content'):
            assert len(self.mysql_builder.get_user_by_username(username=username)) == 0
    
    @pytest.mark.API
    @allure.epic('Test API: /api/block_user/<username>')
    @allure.story('Block existent user by email')
    def test_block_by_email(self):
        '''
            Тестируем блокирование существующего пользователя через его email.
            
            Шаги:
                1. Блокируем сушествующего пользователя (c access = 1) с помощью API через его email
                2. Проверяем статус код
                3. Проверяем значение access у данного пользователя

            Ожидаемый результат:

                1. Статус код == 404
                2. Присутствие данных добавленного пользователя в БД
                3. У данного пользователя access == 1
        '''
        with allure.step('Generate user (access = 1), add him to DB and try blocking him via API by his email'):
            username, password, email = self.builder.random_person()

            self.mysql_builder.create_user(username=username, password=password, email=email, access=1)
        
            response = self.api_client.get_block_user(username=email)
        
        with allure.step('Check status code'):
            assert response.status_code == 404

        with allure.step('Check database content'):
            db_data = self.mysql_builder.get_user_by_username(username=username)
        
            assert len(db_data) == 1
            
            user = db_data[0]

            self.check_db(user, username, password, email, access=1, active=0, start_active_time=None)

    @pytest.mark.API
    @allure.epic('Test API: /api/block_user/<username>')
    @allure.story('Block existent user by password')
    def test_block_by_password(self):
        '''
            Тестируем блокирование существующего пользователя через его пароль.
            
            Шаги:
                1. Блокируем сушествующего пользователя с помощью API через его пароль
                2. Проверяем статус код
                3. Проверяем значение access у данного пользователя

            Ожидаемый результат:

                1. Статус код == 404
                2. Присутствие данных добавленного пользователя в БД
                3. У данного пользователя access == 1
        '''
        with allure.step('Generate user, add him to DB and try blocking him via API by his email'):
            username, password, email = self.builder.random_person()

            self.mysql_builder.create_user(username=username, password=password, email=email, access=1)
            
            response = self.api_client.get_block_user(username=password)
        
        with allure.step('Check status code'):
            assert response.status_code == 404

        with allure.step('Check database content'):
            db_data = self.mysql_builder.get_user_by_username(username=username)
        
            assert len(db_data) == 1
            
            user = db_data[0]

            self.check_db(user, username, password, email, access=1, active=0, start_active_time=None)


class TestApiAccept(ApiBaseAuthorized):
    
    '''
        Тестирование разблокировки пользователя
    '''

    @pytest.mark.API
    @allure.epic('Test API: /api/accept_user/<username>')
    @allure.story('Accept existent user with access = 0')
    def test_accept_existent_user_w_access_0(self):
        '''
            Тестируем разблокирование существующего пользователя через его username, когда его access = 0.
            
            Шаги:
                1. Создаем напрямую в БД пользователя с access = 0
                2. Разблокируем его с помощью API
                2. Проверяем статус код
                3. Проверяем значение access у данного пользователя

            Ожидаемый результат:

                1. Статус код == 200
                2. Присутствие данных добавленного пользователя в БД
                3. У данного пользователя access == 1
        '''
        with allure.step('Generate user and add him to DB, make accept request'):
            username, password, email = self.builder.random_person()

            self.mysql_builder.create_user(username=username, password=password, email=email, access=0)
        
        response = self.api_client.get_accept_user(username=username)
        
        with allure.step('Check status code'):
            assert response.status_code == 200
        
        with allure.step('Check database content'):
            db_data = self.mysql_builder.get_user_by_username(username=username)

            assert len(db_data) == 1

            user = db_data[0]

            self.check_db(user, username, password, email, access=1, active=0, start_active_time=None)

    @pytest.mark.API
    @allure.epic('Test API: /api/accept_user/<username>')
    @allure.story('Accept existent user with access = 1')
    def test_accept_existent_user_w_access_1(self):
        '''
            Тестируем разблокирование существующего пользователя через его username, когда его access = 1.
            
            Шаги:
                1. Создаем напрямую в БД пользователя с access = 1
                2. Разблокируем его с помощью API
                2. Проверяем статус код
                3. Проверяем значение access у данного пользователя

            Ожидаемый результат:

                1. Статус код == 304
                2. Присутствие данных добавленного пользователя в БД
                3. У данного пользователя access == 1
        '''
        with allure.step('Generate user and add him to DB, make accept request'):
            username, password, email = self.builder.random_person()

            self.mysql_builder.create_user(username=username, password=password, email=email, access=1)
            
            response = self.api_client.get_accept_user(username=username)
        
        with allure.step('Check status code'):
            assert response.status_code == 304

        with allure.step('Check database content'):
            db_data = self.mysql_builder.get_user_by_username(username=username)

            assert len(db_data) == 1

            user = db_data[0]

            self.check_db(user, username, password, email, access=1, active=0, start_active_time=None)

    @pytest.mark.API
    @allure.epic('Test API: /api/accept_user/<username>')
    @allure.story('Accept non existent user')
    def test_accept_non_existent_user(self):
        '''
            Тестируем разблокирование несуществующего пользователя.
            
            Шаги:
                1. Разблокируем несушествующего пользователя с помощью API
                2. Проверяем статус код
                3. Отсутствие данных пользовател в БД

            Ожидаемый результат:

                1. Статус код == 404
                2. Отсутствие данных пользователя в БД
        '''
        with allure.step('Generate user and make accept request'):
            username = self.builder.random_username()

            response = self.api_client.get_accept_user(username=username)
        
        with allure.step('Check status code'):
            assert response.status_code == 404

        with allure.step('Check database content'):
            assert len(self.mysql_builder.get_user_by_username(username=username)) == 0
    
    @pytest.mark.API
    @allure.epic('Test API: /api/accept_user/<username>')
    @allure.story('Accept existent user via email')
    def test_accept_by_email(self):
        '''
            Тестируем разблокирование существующего пользователя через его email.
            
            Шаги:
                1. Разблокируем сушествующего пользователя с помощью API через его email
                2. Проверяем статус код

            Ожидаемый результат:

                1. Статус код == 404
        '''
        with allure.step('Generate user and add him to DB (with access = 0), make accept request via email'):
            username, password, email = self.builder.random_person()

            self.mysql_builder.create_user(username=username, password=password, email=email, access=0)
            
            response = self.api_client.get_accept_user(username=email)
        
        with allure.step('Check status code'):
            assert response.status_code == 404

        with allure.step('Check database content'):
            db_data = self.mysql_builder.get_user_by_username(username=username)

            assert len(db_data) == 1

            user = db_data[0]

            self.check_db(user, username, password, email, access=0, active=0, start_active_time=None)

    @pytest.mark.API
    @allure.epic('Test API: /api/accept_user/<username>')
    @allure.story('Accept existent user via password')
    def test_accept_by_password(self):
        '''
            Тестируем разблокирование существующего пользователя через его пароль.
            
            Шаги:
                1. Разблокируем сушествующего пользователя с помощью API через его пароль
                2. Проверяем статус код

            Ожидаемый результат:

                1. Статус код == 404
        '''

        with allure.step('Generate user and add him to DB (with access = 0), make accept request via password'):
            username, password, email = self.builder.random_person()

            self.mysql_builder.create_user(username=username, password=password, email=email, access=0)
        
            response = self.api_client.get_accept_user(username=password)
        
        with allure.step('Check status code'):
            assert response.status_code == 404

        with allure.step('Check database content'):
            db_data = self.mysql_builder.get_user_by_username(username=username)

            assert len(db_data) == 1

            user = db_data[0]

            self.check_db(user, username, password, email, access=0, active=0, start_active_time=None)


class TestApiStatus(ApiBase):
    '''
        Тестирование статуса приложения
    '''
    @pytest.mark.API
    @allure.epic('Test API: /status')
    @allure.story('Get application status')
    def test_status(self):
        '''
            Тестируем ответ на запрос /status.
            
            Шаги:
                1. Запрашиваем статус приложения
                2. Проверяем статус код
                3. Проверяем содержимое json

            Ожидаемый результат:

                1. Статус код == 200
                2. status == ok
        '''
        with allure.step('Get status via API'):
            response = self.api_client.get_status()

        with allure.step('Check status code and "status"'):
            assert response.status_code == 200
            assert len(response.json()) == 1
            assert response.json()['status'] == 'ok'


class TestApiUnauthorized(ApiBase):
    '''
        Тестирование API со стороны неавторизированного пользователя
        (все запросы корректны)
    '''
    @pytest.mark.API
    @allure.epic('Test API: unauthorized requests')
    @allure.story('GET /api/add_user')
    def test_add(self):
        '''
            Тестируем валидное добавление пользователя.
            
            Шаги:
                1. Генерируем случайного пользователя
                2. Делаем POST запрос согласно API;
                3. Проверяем статус-код ответа;
                4. Проверяем, что пользователь не добавлен в БД.
            
            Ожидаемый результат:
                1. Статус код == 401;
                2. Отсутствие данных о пользователе в БД.
        '''
        with allure.step('Generate user and add him via API'):
            username, password, email = self.builder.random_person()

            response = self.api_client.post_add_user(username=username, password=password, email=email)
        
        with allure.step('Check status code'):
            assert response.status_code ==  401

        with allure.step('Check database content'):
            assert len(self.mysql_builder.get_user_by_username(username=username)) == 0
            assert len(self.mysql_builder.get_user_by_password(password=password)) == 0
            assert len(self.mysql_builder.get_user_by_email(email=email)) == 0
        
    @pytest.mark.API
    @allure.epic('Test API: unauthorized requests')
    @allure.story('GET /api/del_user/<username>')
    def test_delete(self):
        '''
            Тестируем удаление существующего пользователя.
            
            Шаги:

                1. Добавляем пользователя напрямую в БД
                2. Удаляем его с помощью API
                2. Проверяем статус код
                3. Проверяем наличие данных добавленного пользователя в БД

            Ожидаемый результат:

                1. Статус код == 401
                2. Наличие данных добавленного пользователя в БД
        '''
        with allure.step('Generate user and add him to DB, then delete him via API'):
            username, password, email = self.builder.random_person()
            
            self.mysql_builder.create_user(username=username, password=password, email=email)

            response = self.api_client.get_del_user(username=username)
        
        with allure.step('Check status code'):
            assert response.status_code == 401
        
        with allure.step('Check database content'):
            db_data = self.mysql_builder.get_user_by_username(username=username)
        
            assert len(db_data) == 1
            
            user = db_data[0]

            self.check_db(user, username, password, email, access=1, active=0, start_active_time=None)

    @pytest.mark.API
    @allure.epic('Test API: unauthorized requests')
    @allure.story('GET /api/block_user/<username>')
    def test_block(self):
        '''
            Тестируем блокирование существующего пользователя через его username, когда его access = 1.
            
            Шаги:
                1. Создаем напрямую в БД пользователя с access = 1
                2. Блокируем его с помощью API
                2. Проверяем статус код
                3. Проверяем значение access у данного пользователя

            Ожидаемый результат:

                1. Статус код == 401
                2. Присутствие данных добавленного пользователя в БД
                3. У данного пользователя access == 1
        '''
        with allure.step('Generate user with access = 1 and block him via API'):
            username, password, email = self.builder.random_person()

            self.mysql_builder.create_user(username=username, password=password, email=email, access=1)
            
            response = self.api_client.get_block_user(username=username)
        
        with allure.step('Check status code'):
            assert response.status_code == 401

        with allure.step('Check database content'):
            db_data = self.mysql_builder.get_user_by_username(username=username)
        
            assert len(db_data) == 1
            
            user = db_data[0]
            
            self.check_db(user, username, password, email, access=1, active=0, start_active_time=None)

    @pytest.mark.API
    @allure.epic('Test API: unauthorized requests')
    @allure.story('GET /api/accept_user/<username>')
    def test_accept(self):
        '''
            Тестируем разблокирование существующего пользователя через его username, когда его access = 0.
            
            Шаги:
                1. Создаем напрямую в БД пользователя с access = 0
                2. Разблокируем его с помощью API
                2. Проверяем статус код
                3. Проверяем значение access у данного пользователя

            Ожидаемый результат:

                1. Статус код == 401
                2. Присутствие данных добавленного пользователя в БД
                3. У данного пользователя access == 0
        '''
        with allure.step('Generate user and add him to DB, make accept request'):
            username, password, email = self.builder.random_person()

            self.mysql_builder.create_user(username=username, password=password, email=email, access=0)
        
        response = self.api_client.get_accept_user(username=username)
        
        with allure.step('Check status code'):
            assert response.status_code == 401
        
        with allure.step('Check database content'):
            db_data = self.mysql_builder.get_user_by_username(username=username)

            assert len(db_data) == 1

            user = db_data[0]

            self.check_db(user, username, password, email, access=0, active=0, start_active_time=None)