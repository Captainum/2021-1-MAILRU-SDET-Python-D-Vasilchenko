import pytest

from utils.builder import Builder

class ApiBase:
    authorize = True 

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, api_client, credentials, config, builder):
        self.api_client = api_client
        self.config = config
        self.builder = builder
        if self.authorize:
            self.api_client.post_login(*credentials)

    @pytest.fixture(scope='function')
    def campaign(self):
        campaign_name = self.builder.random_title()
        campaign = self.api_client.post_create_campaign(campaign_name)
        yield campaign
        self.api_client.post_delete_campaign(campaign['id'])