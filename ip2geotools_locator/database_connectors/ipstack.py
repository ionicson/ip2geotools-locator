from collections import namedtuple

from ip2geotools.errors import LocationError, IpAddressNotFoundError, PermissionRequiredError, InvalidRequestError, InvalidResponseError, ServiceError, LimitExceededError
from ip2geotools.databases.noncommercial import ipstack

from ip2geotools_locator.folium_map import FoliumMap

Location = namedtuple('Location', 'latitude longitude')

class IpstackDB:
    m = FoliumMap()
    __db_data = None
    __api_key = None
    
    def __init__(self, api_key):
        self.__api_key = api_key        

    def get_location(self, ip):
        try:
            self.__db_data = ipstack.get(ip, self.__api_key)
            
            loc = Location(self.__db_data.latitude, self.__db_data.longitude)

            return loc
       
        except IpAddressNotFoundError as e:
            print(__name__ + ": " + str(e)) 
        
        except PermissionRequiredError as e:
            print(__name__ + ": " + str(e)) 

        except ServiceError as e:
            print(__name__ + ": " + str(e)) 
        
        except LimitExceededError as e:
            print(__name__ + ": " + str(e))     

        except (LocationError, InvalidRequestError, InvalidResponseError) as e:
            print(__name__ + ": " + str(e)) 

        except TypeError as e:
            print(__name__ + ": " + str(e))      

    def add_to_map(self):
        try:
            self.m.add_marker_noncommercial(ipstack.__name__, self.__db_data.ip_address, self.__db_data.country, self.__db_data.city, self.__db_data.latitude, self.__db_data.longitude)
        except AttributeError as e:
            print(__name__ + ": " + str(e)) 