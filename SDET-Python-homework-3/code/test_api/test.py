import pytest

from test_api.base import ApiBase
from api.client import ApiClient

import os

class TestApi(ApiBase):
    @pytest.mark.API
    def test_create_campaign(self, campaign):
        response = self.api_client.get_campaign(campaign['id'])
        assert response['id'] == campaign['id']

    @pytest.mark.API
    def test_create_segment(self):
        segment_id = self.api_client.post_create_segment()
        assert 'not supported' == self.api_client.get_segment_status(segment_id)

    @pytest.mark.API
    def test_delete_segment(self):
        segment_id = self.api_client.post_create_segment()
        self.api_client.post_delete_segment(segment_id)
        assert 'not found' == self.api_client.get_segment_status(segment_id)