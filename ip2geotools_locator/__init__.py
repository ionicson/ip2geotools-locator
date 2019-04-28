# -*- coding: utf-8 -*-

"""Top-level package for ip2geotools-locator."""

import logging
import ip2geotools_locator.database_connectors
import ip2geotools_locator.calculations

from ip2geotools_locator.main import Locator

__author__ = """Oldřich Klíma"""
__email__ = 'xklima27@vutbr.cz'
__version__ = '1.6.0'
NAME = "ip2geotools-locator"

LOGGER = logging.getLogger()
LOGGER.info("###############################################")
LOGGER.info("######### Ip2Geotools-Locator v 1.6.0 #########")
LOGGER.info("###############################################")
