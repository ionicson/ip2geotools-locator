# -*- coding: utf-8 -*-
from ip2geotools_locator.database_connectors import HostIpDB, IpCityDB
from ip2geotools_locator.calculations import Average
from ip2geotools_locator.folium_map import FoliumMap

"""Main module."""
class Locator:

    ip_city = True
    host_ip = True
    ip_address = None

    locations = []

    def get_locations(self, ip):
        self.ip_address = ip
        if self.host_ip:
            host_ip = HostIpDB()

            self.locations.append(host_ip.get_location(ip))
            #host_ip.add_to_map()

        if self.ip_city:
            ip_city = IpCityDB()

            self.locations.append(ip_city.get_location(ip))
            host_ip.add_to_map()

    def calculate(self):
        map = FoliumMap()
        
        location = Average.calculate(self.locations)

        map.add_calculated_marker("Average", self.ip_address, location[0], location[1])
        map.generate_map(location)

        return location