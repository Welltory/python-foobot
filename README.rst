Foobot API library
==================

Install
-------

.. code-block:: bash

   $ pip install foobot

Usage
-----

.. code-block:: python

   from foobot.api import FoobotAPI

   api = FoobotAPI(
       api_key=<YOUR_API_KEY>,
       access_token=<YOUR_ACCESS_TOKEN>,
       homehost=<YOUR_HOME_HOST>,
       username=<YOUR_USER_EMAIL
   )
   devices = api.get_devices()
   data_by_devices = api.get_last_day_data()

API reference
-------------

FoobotAPI
^^^^^^^^^

- **get_devices()** return list of dict described devices connected to this accunt
- **get_last_day_data()** return list of data from devices
    - *raw* (Default: False) - return data as a dict or as a FoobotDataItem instance
- **get_data()** return list of data from devices
    - *start* (Default: 3600*24) - return data as a dict or as a FoobotDataItem instance
    - *end* (Default: "last") - return data as a dict or as a FoobotDataItem instance
    - *average_by* (Default: 3600) - return data as a dict or as a FoobotDataItem instance

FoobotDataItem
^^^^^^^^^^^^^^

- **timstamp** - timestamp for measure
- **particulate_matter (ppm)** - particulate matter
- **temp (C)** - temperature
- **humidity (pc)** - humidity
- **co2 (ppm)** - CO2
- **voc (ppb)** - volatile organic compounds 
- **foobot_index** - Internal index for Foobot


License
-------

The MIT License (MIT)

Tests
-----

.. code-block:: bash

   $ python setup.py test

Contributors
------------
