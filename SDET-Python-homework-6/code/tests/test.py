import pytest

from mysql.builder import MySQLBuilder
from mysql.models import Total, TotalType, TopURL, TopSizeCli, TopServ

from scripts.scripts import *

class MySQLBase:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_client, config):
        self.mysql = mysql_client
        self.mysql_builder = MySQLBuilder(mysql_client)
        self.config = config


class TestMySQL(MySQLBase):

    def test_script_1(self):
        data = total_requests(self.config['log_root'])
        self.mysql_builder.create_total('TOTAL COUNT', data['TOTAL COUNT'])

        res = self.mysql.session.query(Total).all()

        assert len(data) == len(res)
    
    def test_script_2(self):
        data = total_requests_type(self.config['log_root'])
        for d in data:
            self.mysql_builder.create_total_type(d['METHOD'], d['COUNT'])
        
        res = self.mysql.session.query(TotalType).all()

        assert len(data) == len(res) 

    def test_script_3(self):
        data = top_requests_url(self.config['log_root'])
        for d in data:
            self.mysql_builder.create_top_url(d['URL'], d['COUNT'])
    
        res = self.mysql.session.query(TopURL).all()

        assert len(data) == len(res) 

    def test_script_4(self):
        data = top_requests_size_cli(self.config['log_root'])
        for d in data:
            self.mysql_builder.create_top_size_cli(d['URL'], d['STATUS'], d['SIZE'], d['IP'])

        res = self.mysql.session.query(TopSizeCli).all()

        assert len(data) == len(res) 
    
    def test_script_5(self):
        data = top_requests_serv(self.config['log_root'])
        for d in data:
            self.mysql_builder.create_top_serv(d['IP'], d['COUNT'])
        
        res = self.mysql.session.query(TopServ).all()

        assert len(data) == len(res) 