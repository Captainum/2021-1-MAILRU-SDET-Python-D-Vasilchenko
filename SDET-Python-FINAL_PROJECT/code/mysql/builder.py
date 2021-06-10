from mysql.models import *

import allure
import logging

logger = logging.getLogger('test')

class MySQLBuilder:

    def __init__(self, client):
        self.client = client

        logger.debug('MySQLBuilder initialized')

    @allure.step('Database: add user with username={username}')
    def create_user(self, password, email, id=None, username=None, access=1, active=0, start_active_time=None):
        user = TestUsers(
            id = id,
            username = username,
            password = password,
            email = email,
            access = access,
            active = active,
            start_active_time = start_active_time
        )
        logger.info(f'Database: add user with username={username},'\
                    f'password={password}, email={email}, access={access}, active={active}, start_active_time={start_active_time}'
                   )
        self.client.session.add(user)
        self.client.session.commit()

        return user

    @allure.step('Database: delete user with username={username}')
    def delete_user(self, username):
        logger.info(f'Database: delete user with username={username}')
        
        self.client.session.query(TestUsers).filter(TestUsers.username==username).delete()
        self.client.session.commit()

    @allure.step('Database: update user with username={username}')
    def update_user(self, username, data_to_update: dict):
        logger.info(f'Database: update user with username={username}, data={data_to_update}')

        self.client.session.query(TestUsers).filter(TestUsers.username==username).update(data_to_update)
        self.client.session.commit()        

    @allure.step('Database: get user with username={username}')
    def get_user_by_username(self, username):
        logger.info(f'Database: get user with username={username}')

        response = self.client.session.query(TestUsers).filter(TestUsers.username==username).all()
        return response

    @allure.step('Database: get user with password={password}')
    def get_user_by_password(self, password):
        logger.info(f'Database: get user with password={password}')

        response = self.client.session.query(TestUsers).filter(TestUsers.password==password).all()
        return response
    
    @allure.step('Database: get user with email={email}')
    def get_user_by_email(self, email):
        logger.info(f'Database: get user with email={email}')

        response = self.client.session.query(TestUsers).filter(TestUsers.email==email).all()
        return response