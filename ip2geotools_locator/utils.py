import logging
from collections import namedtuple

LOG_FORMAT = "%(asctime)s %(levelname)s - %(message)s"
logging.basicConfig(filename = "ip2geotools_locator.log", level = logging.DEBUG, format = LOG_FORMAT, filemode= "w")

# Application logger
logger = logging.getLogger()

# Location is stored as namedtuple
Location = namedtuple('Location', 'latitude longitude')