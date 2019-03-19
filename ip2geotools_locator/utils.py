"""Things used across aplication"""
import logging
from collections import namedtuple

LOG_FORMAT = "%(asctime)s %(levelname)s - %(module)s: %(message)s"
logging.basicConfig(filename="ip2geotools_locator.log", level=logging.INFO, format=LOG_FORMAT,
                    filemode="w")

# Application logger
LOGGER = logging.getLogger()

# Location is stored as namedtuple
Location = namedtuple('Location', 'latitude longitude')

# Default application settings
DEFAULT_SETTINGS = """
{
    "noncommercial": {
        "ip_city": {
            "active": true,
            "generate_marker": true,
            "api_key": null,
            "db_file": null,
            "login": null,
            "password": null
        },
        "host_ip": {
            "active": true,
            "generate_marker": true,
            "api_key": null,
            "db_file": null,
            "login": null,
            "password": null
        },
        "ip2location": {
            "active": false,
            "generate_marker": false,
            "api_key": null,
            "db_file": "",
            "login": null,
            "password": null
        },
        "ipstack": {
            "active": false,
            "generate_marker": false,
            "api_key": "",
            "db_file": null,
            "login": null,
            "password": null
        },
        "max_mind_lite": {
            "active": false,
            "generate_marker": false,
            "api_key": null,
            "db_file": "",
            "login": null,
            "password": null
        }
    },
    "commercial": {
        "eurek": {
            "active": false,
            "generate_marker": false,
            "api_key": null,
            "db_file": null,
            "login": null,
            "password": null
        },
        "geobytes_city": {
            "active": true,
            "generate_marker": true,
            "api_key": null,
            "db_file": null,
            "login": null,
            "password": null
        },
        "ip_info": {
            "active": false,
            "generate_marker": false,
            "api_key": "",
            "db_file": null,
            "login": null,
            "password": null
        },
        "ip_web": {
            "active": true,
            "generate_marker": true,
            "api_key": null,
            "db_file": null,
            "login": null,
            "password": null
        },
        "ip2location_web": {
            "active": false,
            "generate_marker": false,
            "api_key": null,
            "db_file": null,
            "login": null,
            "password": null
        },
        "max_mind": {
            "active": true,
            "generate_marker": true,
            "api_key": null,
            "db_file": null,
            "login": null,
            "password": null
        },
        "neustar_web": {
            "active": true,
            "generate_marker": true,
            "api_key": null,
            "db_file": null,
            "login": null,
            "password": null
        },
        "skyhook": {
            "active": false,
            "generate_marker": false,
            "api_key": null,
            "db_file": null,
            "login": null,
            "password": null
        }
    }
}
"""