import pytest
import requests
from urllib.parse import urljoin

import time
import json
import os

class ResponseStatusCodeException(Exception):
    pass


class ApiClient:
    def __init__(self, config):
        self.base_url = config['url']
        self.session = requests.Session()
        self.config = config

    def _request(self, method, location, headers=None, data=None, expected_status=200, jsonify=True, allow_redirects=True, cookies=None, files=None):
        url = urljoin(self.base_url, location)

        if cookies == None:
            cookies = self.session.cookies
        response = self.session.request(method, url, headers=headers, data=data, allow_redirects=allow_redirects,files=files, cookies=cookies)

        if response.status_code != expected_status:
            raise ResponseStatusCodeException(f'Got {response.status_code} {response.reason} for URL "{url}"!\n'
                                              f'Expected status_code: {expected_status}.')

        if jsonify:
            json_response = response.json()
            return json_response
        return response

    def get_csrftoken(self):
        location = '/csrf/'

        headers = {}

        headers['Referer'] = 'https://target.my.com/dashboard'
        
        self._request('GET', location=location, headers=headers, jsonify=False)

        for name, value in self.session.cookies.items():
            if name == 'csrftoken':
                self.csrf_token = value
                break

    def post_login(self, user, password):
        self.base_url = 'https://auth-ac.my.com/'

        location = '/auth?lang=ru&nosavelogin=0'
        
        headers = {}

        headers['Origin'] = 'https://target.my.com'
        headers['Referer'] = 'https://target.my.com/'

        data = json.load(open(os.path.join(self.config['requests_data_root'], 'post_login.json'), 'rb'))
        data['email'] = user
        data['password'] = password
        self._request('POST', location=location, headers=headers, data=data, jsonify=False)
        
        self.base_url = 'https://target.my.com/'
        
        self.get_csrftoken()

    def post_create_campaign(self, campaign_name):

        pic1_id = self.post_picture('pic1.jpeg')
        pic2_id = self.post_picture('pic2.png')

        location = '/api/v2/campaigns.json'

        headers = {}

        headers['Origin'] = 'https://target.my.com'
        headers['Referer'] = 'https://target.my.com/campaign/new'

        headers['X-CSRFToken'] = self.csrf_token
        
        headers['X-Campaign-Create-Action'] = 'new'

        data = json.load(open(os.path.join(self.config['requests_data_root'], 'post_create_campaign.json'), 'rb'))
        data['banners'][0]['content']['icon_256x256']['id'] = pic2_id
        data['banners'][0]['content']['image_600x600_slide_1']['id'] = pic1_id
        data['banners'][0]['content']['image_600x600_slide_2']['id'] = pic1_id
        data['banners'][0]['content']['image_600x600_slide_3']['id'] = pic1_id
        data['name'] = campaign_name

        response = self._request('POST', location=location, headers=headers, data=json.dumps(data), jsonify=True)

        return response

    def get_campaign(self, campaign_id):
        location = f'/api/v2/campaigns/{campaign_id}.json'

        headers = {}

        headers['Referer'] = f'https://target.my.com/campaign/{campaign_id}'

        headers['X-CSRFToken'] = self.csrf_token

        response = self._request('GET', location=location, headers=headers, jsonify=True)

        return response

    def post_delete_campaign(self, campaign_id):
        location = '/api/v2/campaigns/mass_action.json'
        headers = {}

        headers['Origin'] = 'https://target.my.com'
        headers['Referer'] = 'https://target.my.com/dashboard'
        
        headers['X-CSRFToken'] = self.csrf_token
        
        data = json.load(open(os.path.join(self.config['requests_data_root'], 'post_delete_campaign.json'), 'rb'))
        data[0]['id'] = campaign_id

        self._request('POST', location=location, headers=headers, data=json.dumps(data), jsonify=False, expected_status=204)
 
    def post_picture(self, picture_name):
        location = '/api/v2/content/static.json'

        headers = {}

        headers['Origin'] = 'https://target.my.com'
        headers['Referer'] = 'https://target.my.com/campaign/new'
        
        headers['X-CSRFToken'] = self.csrf_token

        files = {'file': open(os.path.join(self.config['pictures_root'], picture_name), 'rb')}

        response = self._request('POST', location=location, headers=headers, files=files)
        return response['id']

    def post_create_segment(self, segment_name):
        location = '/api/v2/remarketing/segments.json?fields=id,name'

        headers = {}
        
        headers['Origin'] = 'https://target.my.com'
        headers['Referer'] = 'https://target.my.com/segments/segments_list/new'
        
        headers['X-CSRFToken'] = self.csrf_token

        data = json.load(open(os.path.join(self.config['requests_data_root'], 'post_create_segment.json'), 'rb'))
        data['name'] = segment_name

        response = self._request('POST', location=location, headers=headers, data=json.dumps(data), jsonify=True)
        time.sleep(1)
        return response['id']

    def get_segment_status(self, segment_id):
        location = f'/api/v2/coverage/segment.json?id={segment_id}'
        
        headers = {}

        headers['Referer'] = 'https://target.my.com/segments/segments_list'

        response = self._request('GET', location=location, headers=headers, jsonify=True)
        return response['items'][0]['status']

    def post_delete_segment(self, segment_id):
        location = f'/api/v2/remarketing/segments/{segment_id}.json'

        headers = {}

        headers['Origin'] = 'https://target.my.com'
        headers['Referer'] = 'https://target.my.com/segments/segments_list'

        headers['X-CSRFToken'] = self.csrf_token

        self._request('DELETE', location=location, headers=headers, expected_status=204, jsonify=False)
        time.sleep(1)