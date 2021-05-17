from faker import Faker

from mysql.models import *


class MySQLBuilder:

    def __init__(self, client):
        self.client = client

    def create_total(self, value, count):
        total = Total(
            value=value,
            count=count
        )
        
        self.client.session.add(total)
        self.client.session.commit()
        
        return total
    
    def create_total_type(self, method, count):
        total_type = TotalType(
            method=method,
            count=count
        )

        self.client.session.add(total_type)
        self.client.session.commit()

        return total_type

    def create_top_url(self, url, count):
        top_url = TopURL(
            url=url,
            count=count
        )

        self.client.session.add(top_url)
        self.client.session.commit()

        return top_url
    
    def create_top_size_cli(self, url, status, size, ip):
        top_size_cli = TopSizeCli(
            url=url,
            status=status,
            size=size,
            ip=ip
        )        
        
        self.client.session.add(top_size_cli)
        self.client.session.commit()

        return top_size_cli
    
    def create_top_serv(self, ip, count):
        top_serv = TopServ(
            ip=ip,
            count=count
        )

        self.client.session.add(top_serv)
        self.client.session.commit()

        return top_serv