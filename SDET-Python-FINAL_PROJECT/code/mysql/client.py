import sqlalchemy
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker

import allure
import logging

logger = logging.getLogger('test')

class MySqlClient:

    def __init__(self, user, password, db_name, host='mysql', port=3306):
        self.user = user
        self.password = password
        self.db_name = db_name

        self.host = host #ИЗМЕНИТЬ, КОГДА БУДУ ДЕЛАТЬ ДОКЕР (на имя контейнера) 
        self.port = port

        self.engine = None
        self.connection = None
        self.session = None

        logger.debug('MySqlClient initialized')

    @allure.step('Connect MySqlClient to Database')
    def connect(self, db_created=True):
        db = self.db_name if db_created else ''

        self.engine = sqlalchemy.create_engine(
            f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{db}',
            encoding='utf8'
        )
        self.connection = self.engine.connect()
        self.session = sessionmaker(bind=self.connection.engine,
                                    autocommit=False,
                                    expire_on_commit=True
                                    )()
        logger.debug('Database connected')

    @allure.step('MySqlClient: execute {query}')
    def execute_query(self, query, fetch=True):
        logger.debug(f'MySqlClient: execute {query}')
        
        res = self.connection.execute(query)
        if fetch:
            return res.fetchall()
    
    @allure.step('MySqlClient: recreate database')
    def recreate_db(self):
        self.connect(db_created=False)
        self.execute_query(f'DROP database if exists {self.db_name}', fetch=False)
        self.execute_query(f'CREATE database {self.db_name}', fetch=False)
        self.connection.close()

        logger.debug('Database recreated')