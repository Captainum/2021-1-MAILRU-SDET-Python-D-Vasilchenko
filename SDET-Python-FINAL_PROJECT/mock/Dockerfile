FROM python:3.8

ADD /requirements.txt requirements.txt
RUN pip3.8 install -r requirements.txt

ADD /code code

WORKDIR /code

EXPOSE 8083

CMD ["python", "mock.py"]