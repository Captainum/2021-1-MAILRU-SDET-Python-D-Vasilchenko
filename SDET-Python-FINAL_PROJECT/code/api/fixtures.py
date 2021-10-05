import pytest

from api.client import ApiClient, MockClient

@pytest.fixture(scope='function')
def api_client(config):
    host = config['app_host']
    port = config['app_port']

    api_client = ApiClient(host=host, port=port)

    return api_client


@pytest.fixture(scope='function')
def mock_client(config):
    host = config['vk_host']
    port = config['vk_port']

    mock_client = MockClient(host=host, port=port)

    return mock_client