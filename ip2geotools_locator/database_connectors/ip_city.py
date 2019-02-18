"""Module for connecting to DBIpCity"""
from ip2geotools.databases.noncommercial import DbIpCity
from ip2geotools.errors import (LocationError, IpAddressNotFoundError, PermissionRequiredError,
                                InvalidRequestError, InvalidResponseError, ServiceError,
                                LimitExceededError)

from ip2geotools_locator.folium_map import FoliumMap
from ip2geotools_locator.utils import Location, LOGGER as logger


class IpCityDB:
    """
    Class for handling DB connection into DbIpCity Database
    """
    # Instance of map for placing markers
    m = FoliumMap()
    __db_data = None

    def __init__(self):
        # Special config
        pass

    def get_location(self, ip_address):
        """
        Retrieves location for given IP address from DbIpCity database
        Validation and exception handling included.
        """
        try:
            # Try to get and return location
            self.__db_data = DbIpCity.get(ip_address)
            logger.info("%s: DB returned location %.3f N, %.3f E",
                        __name__, self.__db_data.latitude, self.__db_data.longitude)
            return Location(self.__db_data.latitude, self.__db_data.longitude)

        except IpAddressNotFoundError as exception:
            # Handling for IpAddressNotFoundError exception
            logger.warning("%s: Database could not find IP address. IpAddressNotFoundError: %s ",
                           __name__, str(exception))

        except PermissionRequiredError as exception:
            # Handling for PermissionRequiredError exception
            logger.critical("%s: Additional setings required for DB. PermissionRequiredError: %s ",
                            __name__, str(exception))

        except ServiceError as exception:
            # Handling for ServiceError exception
            logger.error(
                "%s: Service is unavailable. ServiceError: %s ", __name__, str(exception))

        except LimitExceededError as exception:
            # Handling for LimitExceededError exception
            logger.warning("%s: LimitExceededError: %s ",
                           __name__, str(exception))

        except (LocationError, InvalidRequestError, InvalidResponseError) as exception:
            # Handling for invalid data, request and response exception
            logger.error("%s: returned %s ", __name__,
                         str(exception.__class__))

        except TypeError as exception:
            # Handling for TypeError exception (in case of database returning None values)
            logger.warning(
                "%s: DB returned invalid values. TypeError: %s ", __name__, str(exception))

    def add_to_map(self):
        """
        Add Folium Marker to map
        Call get_location(ip) method before adding any markers to map
        """
        try:
            logger.debug("%s: Calling add_marker method for %s DB",
                         __name__, DbIpCity.__name__)
            self.m.add_marker_noncommercial(DbIpCity.__name__,
                                            self.__db_data.ip_address,
                                            self.__db_data.country,
                                            self.__db_data.city,
                                            self.__db_data.latitude,
                                            self.__db_data.longitude)
        except AttributeError as exception:
            # Handling for AttributeError exception (in case of database returning None values)
            logger.warning("%s: Cannot add empty marker %s ",
                           __name__, str(exception))
