from faker import Faker

import allure
import logging

fake = Faker()

logger = logging.getLogger('test')

class Builder:
    
    @staticmethod
    @allure.step('Generate random username with length={length}')
    def random_username(length=8):
        logger.info(f'Generate random username with length={length}')

        username = fake.lexify(text='?'*length)
        return username

    @staticmethod
    @allure.step('Generate random password with length={length}')
    def random_password(length=8):
        logger.info(f'Generate random password with length={length}')

        password = fake.lexify(text='?'*length)
        return password
    
    @staticmethod
    @allure.step('Generate random email with length={length}')
    def random_email(length=8):
        logger.info(f'Generate random email with length={length}')

        email = fake.lexify(text='?'*length + '@mail.ru')
        return email
    
    @staticmethod
    @allure.step('Generate random person')
    def random_person(username_length=8, email_length=8, password_length=8):
        username = Builder.random_username(username_length)
        password = Builder.random_password(password_length)
        email = Builder.random_email(email_length)

        logger.info(f'Generate random person: username={username}, password={password}, email={email}')

        return (username, password, email)
    
    @staticmethod
    @allure.step('Generate random string with length={length}')
    def random_str(length=20):
        logger.info(f'Generate random string with length={length}')
        return fake.pystr(max_chars=length)