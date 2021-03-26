from ui.fixtures import *

def pytest_addoption(parser):
    parser.addoption('--url', default='https://target.my.com')
    parser.addoption('--login', default='dimon201188@gmail.com')
    parser.addoption('--password', default='12345t')

@pytest.fixture(scope='session')
def config(request):
    url = request.config.getoption('--url')
    login = request.config.getoption('--login')
    password = request.config.getoption('--password')
    return {'url': url, 'login': login, 'password': password}
