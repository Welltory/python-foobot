# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest
import datetime

from foobot.api import (FoobotAPI, FoobotDataItem)
from unittest.mock import patch


class FoobotDataItemTestCase(unittest.TestCase):
    def test_create_data_item(self):
        now = datetime.datetime.now()
        data = [now.strftime("%s"), '1', '2', '3', '4', '5', '6']
        data_item = FoobotDataItem(data)
        self.assertTrue(data_item.timestamp.year == now.year)
        self.assertTrue(data_item.timestamp.month == now.month)
        self.assertTrue(data_item.timestamp.day == now.day)
        self.assertTrue(data_item.timestamp.hour == now.hour)
        self.assertTrue(data_item.timestamp.minute == now.minute)
        self.assertTrue(data_item.timestamp.second == now.second)
        self.assertTrue(data_item.particulate_matter == data[1])
        self.assertTrue(data_item.temp == data[2])
        self.assertTrue(data_item.humidity == data[3])
        self.assertTrue(data_item.co2 == data[4])
        self.assertTrue(data_item.voc == data[5])
        self.assertTrue(data_item.foobot_index == data[6])


class FoobotTestCase(unittest.TestCase):
    def create_test_api(self):
        return FoobotAPI(
            api_key='TEST_API_KEY',
            access_token='TEST_API_TOKEN',
            username='TEST_USERNAME',
            homehost='api-eu-west-1.foobot.io',
            client_key='',
            client_secret='',
        )

    def test_create_api(self):
        api = self.create_test_api()
        self.assertTrue(api.access_token == 'TEST_API_TOKEN')
        self.assertTrue(api.username == 'TEST_USERNAME')
        self.assertTrue(api.home_host == 'http://api.foobot.io/')

    def test_get_devices(self):
        api = self.create_test_api()
        with patch('foobot.api.requests.get') as mock_devices:
            mock_devices.return_value.ok = True
            mock_devices.return_value.status_code = 200
            mock_devices.return_value.json.return_value = [{
                'mac': '123',
                'userId': 0,
                'name': 'MyFoobot',
                'uuid': '123'
            }]
            data = api.get_devices()
            self.assertTrue(data is not None)
            self.assertTrue(data != {})
            self.assertTrue(data[0]['userId'] == 0)
            self.assertTrue(data[0]['uuid'] == '123')
            self.assertTrue(data[0]['name'] == 'MyFoobot')
            self.assertTrue(data[0]['mac'] == '123')

    def test_bad_get_devices(self):
        api = self.create_test_api()
        with patch('foobot.api.requests.get') as mock_devices:
            mock_devices.return_value.ok = True
            mock_devices.return_value.status_code = 404
            mock_devices.return_value.json.return_value = [{
                'mac': '123',
                'userId': 0,
                'name': 'MyFoobot',
                'uuid': '123'
            }]
            data = api.get_devices()
            self.assertTrue(data == {})

    def test_get_last_day_data_raw(self):
        api = self.create_test_api()
        with patch('foobot.api.requests.get') as mock_get, \
            patch.object(FoobotAPI, 'get_devices') as mock_get_devices:
            mocked_json = {
                'datapoints': [
                    ['28372837', '1', '2', '3', '4', '5', '6'],
                    ['28372838', '11', '12', '13', '14', '15', '16'],
                    ['28372838', '21', '22', '23', '24', '25', '26'],
                ]
            }
            mock_get_devices.return_value = [{
                'mac': '123',
                'userId': 0,
                'name': 'MyFoobot',
                'uuid': '123'
            }]

            mock_get.return_value.ok = True
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = mocked_json

            data = api.get_last_day_data(raw=True)
            self.assertTrue(data is not None)
            self.assertTrue(data != {})
            self.assertTrue('datapoints' in data[0])
            for i, d in enumerate(data[0]['datapoints']):
                self.assertTrue(mocked_json['datapoints'][i] == d)

    def test_get_last_day_data_items(self):
        api = self.create_test_api()
        with patch('foobot.api.requests.get') as mock_get, \
            patch.object(FoobotAPI, 'get_devices') as mock_get_devices:
            mocked_json = {
                'datapoints': [
                    ['28372837', '1', '2', '3', '4', '5', '6'],
                    ['28372838', '11', '12', '13', '14', '15', '16'],
                    ['28372838', '21', '22', '23', '24', '25', '26'],
                ]
            }
            mock_get_devices.return_value = [{
                'mac': '123',
                'userId': 0,
                'name': 'MyFoobot',
                'uuid': '123'
            }]

            rt_json = mocked_json.copy()

            mock_get.return_value.ok = True
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = mocked_json

            data = api.get_last_day_data(raw=False)
            self.assertTrue(data is not None)
            self.assertTrue(data != {})
            self.assertTrue('datapoints' in data[0])
            for i, d in enumerate(rt_json['datapoints']):
                self.assertTrue(FoobotDataItem(d).particulate_matter == data[0]['datapoints'][i].particulate_matter)
                self.assertTrue(FoobotDataItem(d).temp == data[0]['datapoints'][i].temp)
                self.assertTrue(FoobotDataItem(d).humidity == data[0]['datapoints'][i].humidity)
                self.assertTrue(FoobotDataItem(d).co2 == data[0]['datapoints'][i].co2)
                self.assertTrue(FoobotDataItem(d).voc == data[0]['datapoints'][i].voc)
                self.assertTrue(FoobotDataItem(d).foobot_index == data[0]['datapoints'][i].foobot_index)


if __name__ == '__main__':
    unittest.main()
