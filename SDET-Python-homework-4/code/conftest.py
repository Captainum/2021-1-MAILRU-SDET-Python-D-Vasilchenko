from ui.fixtures import *

def pytest_addoption(parser):
    parser.addoption('--os', default='android')
    parser.addoption('--appium', default='http://127.0.0.1:4723/wd/hub')
    parser.addoption('--apk_path', default='stuff/Marussia_v1.39.1.apk')

@pytest.fixture(scope='session')
def config(request):
    device_os = request.config.getoption('--os')
    appium = request.config.getoption('--appium')
    apk_path = request.config.getoption('--apk_path')

    return {'appium': appium, 'device_os': device_os, 'apk_path': apk_path}

@pytest.fixture(scope='session')
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.pardir))