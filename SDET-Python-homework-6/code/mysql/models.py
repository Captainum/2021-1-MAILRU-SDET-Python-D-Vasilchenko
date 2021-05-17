from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Total(Base):
    __tablename__ = 'total_requests'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<TotalRequests(" \
               f"id='{self.id}', " \
               f"value='{self.value}', " \
               f"count='{self.count}'" \
               f")>"


    value = Column(String(30), primary_key=True)
    count = Column(Integer, nullable=False)


class TotalType(Base):
    __tablename__ = 'total_requests_type'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<TotalRequestsType(" \
               f"method='{self.method}', " \
               f"count='{self.count}'" \
               f")>"

    method = Column(String(300), primary_key=True)
    count = Column(Integer, nullable=False)


class TopURL(Base):
    __tablename__ = 'top_requests_url'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<TopURL(" \
               f"url='{self.url}', " \
               f"count='{self.count}'" \
               f")>"

    url = Column(String(300), primary_key=True)
    count = Column(Integer, nullable=False)


class TopSizeCli(Base):
    __tablename__ = 'top_requests_size_cli'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<TopSizeCli(" \
               f"url='{self.url}', " \
               f"status='{self.status}', " \
               f"size='{self.size}', " \
               f"ip='{self.ip}'" \
               f")>"

    url = Column(String(300), primary_key=True)
    status = Column(Integer, nullable=False)
    size = Column(Integer, nullable=False)
    ip = Column(String(15), nullable=False)


class TopServ(Base):
    __tablename__ = 'top_requests_serv'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<TopServ(" \
               f"ip='{self.ip}'," \
               f"count='{self.count}'" \
               f")>"
    ip = Column(String(30), primary_key=True)
    count = Column(Integer, nullable=False)