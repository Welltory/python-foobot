# -*- coding: utf-8 -*-

import datetime

import requests

__all__ = [
    'FoobotAPI',
    'FoobotDataItem',
]


class RefreshTokenError(Exception):
    pass


class FoobotDataItem(object):
    timestamp = None
    particulate_matter = None
    temp = None
    humidity = None
    co2 = None
    voc = None
    foobot_index = None

    def __init__(self, data):
        # print(data)
        self.timestamp = datetime.datetime.fromtimestamp(int(data[0]))
        self.particulate_matter = data[1]
        self.temp = data[2]
        self.humidity = data[3]
        self.co2 = data[4]
        self.voc = data[5]
        self.foobot_index = data[6]


class FoobotAPI(object):
    headers = {}

    def __init__(self,
                 api_key,
                 access_token,
                 homehost,
                 username,
                 client_key=None,
                 client_secret=None):
        self.api_key = api_key
        self.homehost = homehost
        self.username = username
        self.access_token = access_token
        self.client_key = client_key
        self.client_secret = client_secret

        self.headers['Authorization'] = 'bearer {}'.format(self.access_token)
        self.headers['X-API-KEY-TOKEN'] = self.api_key

    def _get(self, url):
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        return {}

    def _post(self, url, data):
        response = requests.post(url, data=data)
        if response.status_code == 200:
            return response.json()
        raise RefreshTokenError(response.content)

    def _url(self, url, home_host=None):
        if home_host is None:
            home_host = self.homehost
        return 'https://{}/{}'.format(home_host, url)

    @property
    def region_token(self):
        return self._get(self._url('v2/user/me/home/',
                                   home_host='api-us-east-1.foobot.io'))

    def refresh_token(self, refresh_token):
        if not self.client_key:
            raise ValueError("Client key is not valid")

        if not self.client_secret:
            raise ValueError("Client key is not valid")

        if not refresh_token:
            raise ValueError("Refresh token is not valid")

        data = {
            'client_id': self.client_key,
            'client_secret': self.client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
        }
        return self._post(self._url('oauth2/token',
                                    home_host='api-us-east-1.foobot.io'), data)

    def get_devices(self):
        return self._get(
            self._url('v2/owner/{}/device/'.format(self.username)))

    def get_data(self, start=None, end='last', average_by=3600):
        if start is None:
            start = 3600 * 24  # pragma: no cover
        data = []
        for dev in self.get_devices():
            url = 'v2/device/{}/datapoint/{}/{}/{}/'.format(
                self.homehost,
                dev['uuid'],
                start,
                end,
                average_by
            )
            item = self._get(self._url(url))
            if item:
                data.append(item)
        return data

    def get_last_day_data(self, raw=False):
        data = self.get_data(start=3600 * 24, end='last')
        if raw:
            return data
        else:
            for i in range(len(data)):
                data[i]['datapoints'] = [FoobotDataItem(d) for d in
                                         data[i]['datapoints']]
            return data