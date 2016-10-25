# -*- coding: utf-8 -*-

import datetime

import requests

from foobot.error import *

__all__ = [
    'FoobotAPI',
    'FoobotDataItem',
]


def check_execption(func):
    def _check(*arg, **kws):
        resp = func(*arg, **kws)
        if resp.status_code >= 400:
            if resp.status_code == 403:
                raise FoobotOAuthError(401, 'UNAUTHORIZED')
            else:
                raise FoobotAPIError(resp)
        body = resp.content
        if body:
            return resp.json()
        return body

    return _check


class APIBase(object):
    @property
    def headers(self):
        return {
            'Authorization': 'bearer {}'.format(
                self.credentials['access_token']),
            'X-API-KEY-TOKEN': self.credentials['api_key']
        }

    @check_execption
    def _get(self, url, base_url=None, **opts):
        if 'headers' not in opts:
            opts['headers'] = self.headers
        return requests.get(self._url(url, base_url=base_url), **opts)

    @check_execption
    def _post(self, url, **opts):
        return requests.post(self._url(url), **opts)

    def _url(self, url, base_url=None):
        return "https://{}/{}".format(
            self.credentials['base_url'] if base_url is None else base_url,
            url
        )


class FoobotDataItem(object):
    timestamp = None
    particulate_matter = None
    temp = None
    humidity = None
    co2 = None
    voc = None
    foobot_index = None

    def __init__(self, data):
        self.timestamp = datetime.datetime.fromtimestamp(int(data[0]))
        self.particulate_matter = data[1]
        self.temp = data[2]
        self.humidity = data[3]
        self.co2 = data[4]
        self.voc = data[5]
        self.foobot_index = data[6]


class FoobotAPI(APIBase):
    def __init__(self,
                 api_key,
                 homehost,
                 username,
                 access_token,
                 client_key,
                 client_secret):
        self.base_url = 'api-us-east-1.foobot.io'
        self.home_host = homehost
        self.username = username

        self.api_key = api_key
        self.access_token = access_token
        self.client_key = client_key
        self.client_secret = client_secret

    @property
    def credentials(self):
        return {
            'client_key': self.client_key,
            'client_secret': self.client_secret,
            'access_token': self.access_token,
            'api_key': self.api_key,
            'home_host': self.home_host,
            'base_url': self.base_url,
            'username': self.username,
        }

    @property
    def device(self):
        return self._get(
            'v2/owner/{}/device/'.format(self.credentials['username']),
            base_url=self.credentials['home_host'],
        )

    def get_devices(self):
        return self.device

    @property
    def region_token(self):
        return self._get('v2/user/me/home/',
                         base_url=self.credentials['home_host'])

    def refresh_token(self, refresh_token):
        data = {
            'client_id': self.credentials['client_key'],
            'client_secret': self.credentials['client_secret'],
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
        }
        return self._post('oauth2/token', data=data)

    def get_data(self, start=None, end='last', average_by=3600):
        if start is None:
            start = 3600 * 24  # pragma: no cover
        data = []
        for dev in self.get_devices():
            url = 'v2/device/{}/datapoint/{}/{}/{}/'.format(
                dev['uuid'],
                start,
                end,
                average_by
            )
            item = self._get(url, base_url=self.credentials['home_host'])
            if item:
                data.append(item)
        return data

    def get_last_day_data(self, raw=False):
        data = self.get_data(start=3600 * 24, end='last')

        if raw:
            return data

        for i in range(len(data)):
            data[i]['datapoints'] = [FoobotDataItem(d) for d in
                                     data[i]['datapoints']]
        return data