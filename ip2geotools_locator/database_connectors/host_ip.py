from collections import namedtuple

from ip2geotools.errors import LocationError, IpAddressNotFoundError, PermissionRequiredError, InvalidRequestError, InvalidResponseError, ServiceError, LimitExceededError
from ip2geotools.databases.noncommercial import HostIP

from ip2geotools_locator.folium_map import FoliumMap

Location = namedtuple('Location', 'latitude longitude')

class HostIpDB:
    m = FoliumMap()
    __db_data = None
    
    def __init__(self):
        pass        

    def get_location(self, ip):
        try:
            self.__db_data = HostIP.get(ip)
            if self.__db_data.latitude != None & self.__db_data.longitude != None:
                loc = Location(self.__db_data.latitude, self.__db_data.longitude)

            return loc
       
        except IpAddressNotFoundError as e:
            print(e)
        
        except PermissionRequiredError as e:
            print(e)

        except ServiceError as e:
            print(e)
        
        except LimitExceededError as e:
            print(e)    

        except (LocationError, InvalidRequestError, InvalidResponseError) as e:
            print(e)

        except TypeError:
            pass     
        
    def add_to_map(self):
        self.m.add_marker_noncommercial(HostIP.__name__, self.__db_data.ip_address, self.__db_data.country, self.__db_data.city, self.__db_data.latitude, self.__db_data.longitude)
