from collections import namedtuple

from ip2geotools.databases.noncommercial import DbIpCity
from ip2geotools.errors import LocationError, IpAddressNotFoundError, PermissionRequiredError, InvalidRequestError, InvalidResponseError, ServiceError, LimitExceededError

from ip2geotools_locator.folium_map import FoliumMap

# Namedtuple for storing location info
Location = namedtuple('Location', 'latitude longitude')

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

    def get_location(self, ip):
        """
        Rethrieves location for given IP address from DbIpCity database
        Validation and exception handling included.
        """
        try:
            # Try to get and return location
            self.__db_data = DbIpCity.get(ip)
            return Location(self.__db_data.latitude, self.__db_data.longitude)
       
        except IpAddressNotFoundError as e:
            # Handling for IpAddressNotFoundError exception
            print("Module %s returned %s " % (__name__, str(e.with_traceback))) 
        
        except PermissionRequiredError as e:
            # Handling for PermissionRequiredError exception
            print("Module %s returned %s " % (__name__, str(e.with_traceback)))

        except ServiceError as e:
            # Handling for ServiceError exception
            print("Module %s returned %s " % (__name__, str(e.with_traceback))) 
        
        except LimitExceededError as e:
            # Handling for LimitExceededError exception
            print("Module %s returned %s " % (__name__, str(e.with_traceback)))     

        except (LocationError, InvalidRequestError, InvalidResponseError) as e:
            # Handling for invalid data, request and response exception
            print("Module %s returned %s " % (__name__, str(e.with_traceback))) 

        except TypeError as e:
            # Handling for TypeError exception (in case of database returning None values)
            print("Module %s returned %s " % (__name__, str(e.with_traceback)))     
        
    def add_to_map(self):
        """
        Add Folium Marker to map
        Call get_location(ip) method before adding any markers to map
        """
        self.m.add_marker_noncommercial(DbIpCity.__name__, 
            self.__db_data.ip_address, 
            self.__db_data.country, 
            self.__db_data.city, 
            self.__db_data.latitude, 
            self.__db_data.longitude)
