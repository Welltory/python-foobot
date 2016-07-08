Foobot API library
==================

Install
-------

.. code-block:: python

   pip install footbot

Configuration
-------------
Add FOOBOT_API_KEY to settings.py

Usage
-----

.. code-block:: python

   from foobot.foobot import FootbotAPI

   api = FootbotAPI(
       access_token=<YOUR_ACCESS_TOKEN>,
       homehost=<YOUR_HOME_HOST>,
       username=<YOUR_USER_EMAIL
   )
   devices = api.get_devices()
   data_by_devices = api.get_last_day_data()

API reference
-------------

- **get_devices()** return list of dict described devices connected to this accunt
- **get_last_day_data()** return list of data from devices
    - *raw* (Default: False) - return data as a dict or as a FoobotDataItem instance
- **get_data()** return list of data from devices
    - *start* (Default: 3600*24) - return data as a dict or as a FoobotDataItem instance
    - *end* (Default: "last") - return data as a dict or as a FoobotDataItem instance
    - *average_by* (Default: 3600) - return data as a dict or as a FoobotDataItem instance

License
-------

The MIT License (MIT)

Tests
-----

.. code-block:: python

   python setup.py test

Contributors
------------