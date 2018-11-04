# -*- coding: utf-8 -*-
import json

from ip2geotools_locator.database_connectors import HostIpDB, IpCityDB
from ip2geotools_locator.calculations import Average
from ip2geotools_locator.folium_map import FoliumMap

"""Main module."""
class Locator:
    
    ip_address = None
    settings = None
    locations = []

    def __init__(self):
        with open ("ip2geotools_locator/settings.json", "r") as read_file:
            self.settings = json.load(read_file)
        
    def get_locations(self, ip):
        self.ip_address = ip
        
        if self.settings["noncommercial"]["host_ip"]["active"]:
            
            host_ip = HostIpDB()
            self.locations.append(host_ip.get_location(ip))
            
            if self.settings["noncommercial"]["host_ip"]["generate_marker"]:
                host_ip.add_to_map()

        if self.settings["noncommercial"]["ip_city"]["active"]:
            
            ip_city = IpCityDB()
            self.locations.append(ip_city.get_location(ip))
            
            if self.settings["noncommercial"]["ip_city"]["generate_marker"]:
                ip_city.add_to_map()

    def calculate(self):
                
        location = Average.calculate(self.locations)

        map = FoliumMap()
        map.add_calculated_marker("Average", self.ip_address, location[0], location[1])
        map.generate_map(location)

        if location[0] == None or location[1] == None:
            return ("Location for IP address %s could not be calculated!" % self.ip_address)
        else:
            return location