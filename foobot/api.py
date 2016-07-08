# -*- coding: utf-8 -*-

import requests
import datetime


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

    def __init__(self, api_key, access_token, homehost, username):
        self.FOOBOT_API_KEY = api_key
        self.homehost = homehost
        self.username = username
        self.access_token = access_token
        self.headers['Authorization'] = 'bearer {}'.format(self.access_token)
        self.headers['X-API-KEY-TOKEN'] = self.FOOBOT_API_KEY

    def get_devices(self):
        url = 'https://{}/v2/owner/{}/device/'.format(
            self.homehost,
            self.username
        )
        r = requests.get(url, headers=self.headers)
        if r.status_code == 200:
            return r.json()
        return {}

    def get_data(self, start=None, end='last', average_by=3600):
        if start is None:
            start = 3600 * 24  # pragma: no cover
        data = []
        for dev in self.get_devices():
            url = 'https://{}/v2/device/{}/datapoint/{}/{}/{}/'.format(
                self.homehost,
                dev['uuid'],
                start,
                end,
                average_by
            )
            r = requests.get(url, headers=self.headers)
            if r.status_code == 200:
                data.append(r.json())
        return data

    def get_last_day_data(self, raw=False):
        data = self.get_data(start=3600 * 24, end='last')
        if raw:
            return data
        else:
            for i in range(len(data)):
                data[i]['datapoints'] = [FoobotDataItem(d) for d in data[i]['datapoints']]
            return data
