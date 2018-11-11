# -*- coding: utf-8 -*-
"""
Main applicaton module
======================

This module contains whole application logic

"""
import json

from ip2geotools_locator.database_connectors import HostIpDB, IpCityDB, Ip2LocationDB, IpstackDB, MaxMindLiteDB
from ip2geotools_locator.database_connectors import GeobytesCityDB, IpInfoDB, MaxMindDB
from ip2geotools_locator.calculations import Average, Clustering, Median
from ip2geotools_locator.folium_map import FoliumMap

class Locator:
    """
    This class manages settings, Database connections and Calculations
    """
    ip_address = None
    commercial = []
    noncommercial = []

    # List of locations
    locations = []

    def __init__(self, generate_map = True):
        """
        __init__ method which reads settings.json file.
        """
        # Should application generate Folium map file? (Default false)
        self.generate_map = generate_map

        # Read settings.json
        with open ("settings.json", "r") as read_file:
            settings = json.load(read_file)

        # Parse settings file
        self.commercial = settings["commercial"]
        self.noncommercial = settings["noncommercial"]
                
    def get_locations(self, ip, databases = []):
        """
        Method which searches through selected databases for location of given IP address.
        Accepts selection of databases as list (defaultly settings are loaded from settings.json).
        Sellect ["commercial"] or ["noncommercial"] databases or specify them ["host_ip", "ipstack", ...]
        Data are stored in "locations" list variable.
        """
        self.ip_address = ip

        # Change settings according to provided db list;
        if "noncommercial" in databases:
            for db in self.noncommercial:
                self.noncommercial[db]["active"] = True
            for db in self.commercial:
                self.commercial[db]["active"] = False
        
        elif "commercial" in databases:
            for db in self.noncommercial:
                self.noncommercial[db]["active"] = False
            for db in self.commercial:
                self.commercial[db]["active"] = True

        else:
            for i in databases:
                if i in self.noncommercial:
                    self.noncommercial[i]["active"] = True
                elif i in self.commercial:
                    self.commercial[i]["active"] = True

        # Noncommercial databases
        # Json settings parsed for HostIP database
        if self.noncommercial["host_ip"]["active"]:
            
            # Create object for accessing database and store returned location
            host_ip = HostIpDB()
            self.locations.append(host_ip.get_location(ip))
            
            # Add location to the map?
            if self.noncommercial["host_ip"]["generate_marker"]:
                host_ip.add_to_map()

        # Json settings parsed for DbIpCity database
        if self.noncommercial["ip_city"]["active"]:
            
            ip_city = IpCityDB()
            self.locations.append(ip_city.get_location(ip))
            
            if self.noncommercial["ip_city"]["generate_marker"]:
                ip_city.add_to_map()

        # Json settings parsed for Ip2location database
        if self.noncommercial["ip2location"]["active"]:
            
            ip2location = Ip2LocationDB(self.noncommercial["ip2location"]["db_file"])
            self.locations.append(ip2location.get_location(ip))
            
            if self.noncommercial["ip2location"]["generate_marker"]:
                ip2location.add_to_map()

        # Json settings parsed for Ipstack database
        if self.noncommercial["ipstack"]["active"]:
            
            ipstack = IpstackDB(self.noncommercial["ipstack"]["api_key"])
            self.locations.append(ipstack.get_location(ip))
            
            if self.noncommercial["ipstack"]["generate_marker"]:
                ipstack.add_to_map()

        # Json settings parsed for MaxMind GeoLite2City database
        if self.noncommercial["max_mind_lite"]["active"]:
            
            max_mind_lite = MaxMindLiteDB(self.noncommercial["max_mind_lite"]["db_file"])
            self.locations.append(max_mind_lite.get_location(ip))
            
            if self.noncommercial["max_mind_lite"]["generate_marker"]:
                max_mind_lite.add_to_map()

        # Commercial Databases
        # Json settings parsed for IP Info database
        if self.commercial["ip_info"]["active"]:
            
            ip_info = IpInfoDB(self.commercial["ip_info"]["api_key"])
            self.locations.append(ip_info.get_location(ip))
            
            if self.commercial["ip_info"]["generate_marker"]:
                ip_info.add_to_map()
        
        # Json settings parsed for GeobytesCityDetails database
        if self.commercial["geobytes_city"]["active"]:
            
            geobytes_city = GeobytesCityDB()
            self.locations.append(geobytes_city.get_location(ip))
            
            if self.commercial["geobytes_city"]["generate_marker"]:
                geobytes_city.add_to_map()
        
        # Json settings parsed for MaxMindGeoIp2City database
        if self.commercial["max_mind"]["active"]:
            
            max_mind = MaxMindDB()
            self.locations.append(max_mind.get_location(ip))
            
            if self.commercial["max_mind"]["generate_marker"]:
                max_mind.add_to_map()

    def calculate(self, average = True, clustering = False, interval = False, median = False):
        """
        Method for calculating more acurate location with statistical calculation

        There are four available methods: Average (default method), Clustering, Confidence Interval and Median)
        For multiple selected methods returns namedtuple list (Location.latitude, location.longitude).
        """
        calculated_locations = []
        map = FoliumMap()

        # Calculate average of locations (default method)
        if average:        
            location = Average.calculate(self.locations)
            map.add_calculated_marker("Average", self.ip_address, location.latitude, location.longitude)
            calculated_locations.append(location)
        
        # Calculate location with SciPy Clustering
        if clustering:
            location = Clustering.calculate(self.locations)
            map.add_calculated_marker("Clustering", self.ip_address, location.latitude, location.longitude)
            calculated_locations.append(location)
        
        # Calculate location from 90% Confdence interval
        if interval:
            pass
        
        # Calculate Median from given locations
        if median:
            location = Median.calculate(self.locations)
            map.add_calculated_marker("Median", self.ip_address, location.latitude, location.longitude)
            calculated_locations.append(location)

        # Generate map file
        if self.generate_map:
            map.generate_map(location)
    
        return calculated_locations