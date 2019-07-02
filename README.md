
# Cisco Prime API Module
This module provides a Python object-oriented "wrapper" for the [Cisco Prime Infrastructure API](https://solutionpartner.cisco.com/media/prime-infrastructure/api-reference/szier-m8-106.cisco.com/webacs/api/v1/index.html). Using the Python [requests module](https://2.python-requests.org/en/master/), it provides a more convenient interface for accomplishing some repeatable tasks.

The current version of this module provides a few basic functions, including setting the high availability settings for Unified Wireless access points that match certain criteria.

Parameters are read from a JSON file, consistent with formatting established in the [Cisco Prime Infrastructure API documentation](https://solutionpartner.cisco.com/media/prime-infrastructure/api-reference/szier-m8-106.cisco.com/webacs/api/v1/index0404.html?id=filtering-doc). The access points that match the criteria are then set with the controllers that are also defined in the JSON file.

#### Before
![Before image](https://github.com/pablopenton/CiscoPrimeAPI/blob/master/static/before.png?raw=true)

#### After
![After image](https://github.com/pablopenton/CiscoPrimeAPI/blob/master/static/after.png?raw=true)

The module also provides a method for obtaining some basic information about access points, like their hostnames, IP addresses, model name, and the IP, hostname, and port of their CDP neighbor.