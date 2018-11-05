# -*- coding: utf-8 -*-
"""
Main applicaton module
======================

This module contains whole application logic

"""
import json

from ip2geotools_locator.database_connectors import HostIpDB, IpCityDB, Ip2LocationDB, IpstackDB, MaxMindLiteDB
from ip2geotools_locator.calculations import Average, Clustering
from ip2geotools_locator.folium_map import FoliumMap

class Locator:
    """
    This class manages settings, Database connections and Calculations
    """
    
    ip_address = None
    settings = None
    locations = []

    def __init__(self, generate_map = False):
        """
        __init__ method which reads settings.json file.
        """
        #Should application generate Folium map file? (Default false)
        self.generate_map = generate_map

        #Read settings.json
        with open ("settings.json", "r") as read_file:
            self.settings = json.load(read_file)
                
    def get_locations(self, ip):
        """
        Method which searches through selected databases for location of given IP address.
        Data are stored in "locations" list variable.
        """
        self.ip_address = ip

        #Noncommercial databases
        #Json settings parsed for HostIP database
        if self.settings["noncommercial"]["host_ip"]["active"]:
            
            #Create object for accessing database and store returned location
            host_ip = HostIpDB()
            self.locations.append(host_ip.get_location(ip))
            
            #Add location to the map?
            if self.settings["noncommercial"]["host_ip"]["generate_marker"]:
                host_ip.add_to_map()

        #Json settings parsed for DbIpCity database
        if self.settings["noncommercial"]["ip_city"]["active"]:
            
            ip_city = IpCityDB()
            self.locations.append(ip_city.get_location(ip))
            
            if self.settings["noncommercial"]["ip_city"]["generate_marker"]:
                ip_city.add_to_map()

        #Json settings parsed for Ip2location database
        if self.settings["noncommercial"]["ip2location"]["active"]:
            
            ip2location = Ip2LocationDB(self.settings["noncommercial"]["ip2location"]["db_file"])
            self.locations.append(ip2location.get_location(ip))
            
            if self.settings["noncommercial"]["ip2location"]["generate_marker"]:
                ip2location.add_to_map()

        #Json settings parsed for HostIP database
        if self.settings["noncommercial"]["ipstack"]["active"]:
            
            ipstack = IpstackDB(self.settings["noncommercial"]["ipstack"]["api_key"])
            self.locations.append(ipstack.get_location(ip))
            
            if self.settings["noncommercial"]["ipstack"]["generate_marker"]:
                ipstack.add_to_map()

        #Json settings parsed for MaxMind GeoLite2City database
        if self.settings["noncommercial"]["max_mind_lite"]["active"]:
            
            max_mind_lite = MaxMindLiteDB(self.settings["noncommercial"]["max_mind_lite"]["db_file"])
            self.locations.append(max_mind_lite.get_location(ip))
            
            if self.settings["noncommercial"]["max_mind_lite"]["generate_marker"]:
                max_mind_lite.add_to_map()

    def calculate(self, average = True, clustering = False, interval = False, median = False):
        """
        Method for calculating more acurate location with statistical calculation

        There are four available methods: Average (default method), Clustering, Confidence Interval and Median)
        For multiple selected methods returns namedtuple list (Location.latitude, location.longitude).
        """
        calculated_locations = []
        map = FoliumMap()

        #Calculate average of locations (default method)
        if average:        
            location = Average.calculate(self.locations)
            map.add_calculated_marker("Average", self.ip_address, location.latitude, location.longitude)
            calculated_locations.append(location)
        
        #Calculate location with SciPy Clustering
        if clustering:
            location = Clustering.calculate(self.locations)
            map.add_calculated_marker("Clustering", self.ip_address, location.latitude, location.longitude)
            calculated_locations.append(location)
        
        #Calculate location from 90% Confdence interval
        if interval:
            pass
        
        #Calculate Median from given locations
        if median:
            pass

        #Generate map file
        if self.generate_map:
            map.generate_map(location[0])
    
        return calculated_locations