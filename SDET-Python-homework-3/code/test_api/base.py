import pytest

class ApiBase:
    authorize = True 

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, api_client, credentials, config):
        self.api_client = api_client
        self.config = config
        if self.authorize:
            self.api_client.post_login(*credentials)

    @pytest.fixture(scope='function')
    def campaign(self):
        campaign = self.api_client.post_create_campaign()
        yield campaign
        self.api_client.post_delete_campaign(campaign['id'])