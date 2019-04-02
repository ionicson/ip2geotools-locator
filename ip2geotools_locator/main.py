# -*- coding: utf-8 -*-
"""
Main applicaton module
======================

This module contains whole application logic

"""
import json

from ip2geotools_locator.database_connectors import (HostIpDB, IpCityDB, Ip2LocationDB, IpstackDB,
                                                     MaxMindLiteDB)
from ip2geotools_locator.database_connectors import (EurekDB, GeobytesCityDB, IpInfoDB, IpWebDB,
                                                     Ip2locationWebDB, MaxMindDB, NeustarWebDB,
                                                     SkyhookDB)
from ip2geotools_locator.calculations import Average, Clustering, Median
from ip2geotools_locator.folium_map import FoliumMap
from ip2geotools_locator.utils import LOGGER as logger, DEFAULT_SETTINGS


class Locator:
    """
    This class manages settings, Database connections and Calculations
    """
    ip_address = None
    commercial = []
    noncommercial = []

    # List of locations
    locations = {}

    def __init__(self, generate_map=True):
        """
        __init__ method which reads settings.json file.
        """
        logger.info("Reading settings.json file")

        # Should application generate Folium map file? (Default true)
        self.generate_map = generate_map

        # Read settings.json
        try:
            with open("settings.json", "r") as read_file:
                settings = json.load(read_file)
        except FileNotFoundError:
            settings = json.loads(DEFAULT_SETTINGS)
            with open("settings.json", "w") as write_file:
                json.dump(settings, write_file)

        # Parse settings file
        self.commercial = settings["commercial"]
        self.noncommercial = settings["noncommercial"]

        logger.debug("Settings parsed for commercial and noncommercial databases.")


    def get_locations(self, ip_address, databases=None):
        """
        Method which searches through selected databases for location of given IP address.
        Accepts selection of databases as list (defaultly settings are loaded from settings.json).
        Use ["commercial"], ["noncommercial"] databases or specify them ["host_ip", "ipstack", ...]
        Data are stored in "locations" list variable.
        """
        locations = {}
        self.ip_address = ip_address
        logger.info("Gathering location records for IP address %s.", ip_address)

        # Change settings according to provided database list;
        if "noncommercial" in databases:
            logger.debug("Adjusting settings for all noncommercial databases.")

            # Each noncomercial database is activated
            for database in self.noncommercial:
                self.noncommercial[database]["active"] = True
            # Each comercial database is deactivated
            for database in self.commercial:
                self.commercial[database]["active"] = False

        elif "commercial" in databases:
            logger.debug("Adjusting settings for all commercial databases.")

            # Each noncomercial database is deactivated
            for database in self.noncommercial:
                self.noncommercial[database]["active"] = False
            # Each comercial database is activated
            for database in self.commercial:
                self.commercial[database]["active"] = True

        else:
            # Configure each DB
            for i in databases:
                logger.debug("Adjusting settings for database %s.", i)
                if i in self.noncommercial:
                    self.noncommercial[i]["active"] = True
                elif i in self.commercial:
                    self.commercial[i]["active"] = True

        # Noncommercial databases
        # Json settings parsed for HostIP database
        if self.noncommercial["host_ip"]["active"]:
            logger.debug("Database HostIP is set as Active in settings. Gathering location.")
            # Create object for accessing database and store returned location
            host_ip = HostIpDB()
            locations["HostIP"] = (host_ip.get_location(ip_address))

            # Add location to the map?
            if self.noncommercial["host_ip"]["generate_marker"]:
                logger.debug("""Folium marker for HostIP database is set as Active in settings. Calling add_to_map method.""")
                host_ip.add_to_map()

        # Json settings parsed for DbIpCity database
        if self.noncommercial["ip_city"]["active"]:
            logger.debug("Database DbIpCity is set as Active in settings. Gathering location.")
            ip_city = IpCityDB()
            locations["DbIpCity"] = (ip_city.get_location(ip_address))

            if self.noncommercial["ip_city"]["generate_marker"]:
                logger.debug("""Folium marker for DbIpCity database is set Active in settings. Calling add_to_map method.""")
                ip_city.add_to_map()

        # Json settings parsed for Ip2location database
        if self.noncommercial["ip2location"]["active"]:
            logger.debug("""database Ip2location is set as Active in settings. Gathering location.""")
            ip2location = Ip2LocationDB(
                self.noncommercial["ip2location"]["db_file"])
            locations["Ip2location"] = (ip2location.get_location(ip_address))

            if self.noncommercial["ip2location"]["generate_marker"]:
                logger.debug("""Folium marker for Ip2location database is set as Active in settings. Calling add_to_map method.""")
                ip2location.add_to_map()

        # Json settings parsed for Ipstack database
        if self.noncommercial["ipstack"]["active"]:
            logger.debug("database Ipstack is set as Active in settings. Gathering location.")
            ipstack = IpstackDB(self.noncommercial["ipstack"]["api_key"])
            locations["Ipstack"] = (ipstack.get_location(ip_address))

            if self.noncommercial["ipstack"]["generate_marker"]:
                logger.debug("""Folium marker for Ipstack database is set as Active in settings. Calling add_to_map method.""")
                ipstack.add_to_map()

        # Json settings parsed for MaxMind GeoLite2City database
        if self.noncommercial["max_mind_lite"]["active"]:
            logger.debug("""database MaxMind GeoLite2City is set as Active in settings. Gathering location.""")
            max_mind_lite = MaxMindLiteDB(
                self.noncommercial["max_mind_lite"]["db_file"])
            locations["MaxMind_GeoLite2City"] = (max_mind_lite.get_location(ip_address))

            if self.noncommercial["max_mind_lite"]["generate_marker"]:
                logger.debug("""Folium marker for MaxMind GeoLite2City database is set as Active in settings. Calling add_to_map method.""")
                max_mind_lite.add_to_map()

        # Commercial Databases
        # Json settings parsed for Eurek database
        if self.commercial["eurek"]["active"]:
            logger.debug("""database Eurek is set as Active in settings. Gathering location.""")
            eurek = EurekDB()
            locations["Eurek"] = (eurek.get_location(ip_address))

            if self.commercial["eurek"]["generate_marker"]:
                logger.debug("""Folium marker for Eurek database is set as Active in settings. Calling add_to_map method.""")
                eurek.add_to_map()

        # Json settings parsed for GeobytesCityDetails database
        if self.commercial["geobytes_city"]["active"]:
            logger.debug("""database GeobytesCityDetails is set as Active in settings. Gathering location.""")
            geobytes_city = GeobytesCityDB()
            locations["GeobytesCityDetails"] = (geobytes_city.get_location(ip_address))

            if self.commercial["geobytes_city"]["generate_marker"]:
                logger.debug("""Folium marker for GeobytesCityDetails database is set as Active in settings. Calling add_to_map method.""")
                geobytes_city.add_to_map()

        # Json settings parsed for IP Info database
        if self.commercial["ip_info"]["active"]:
            logger.debug(
                "database IP Info is set as Active in settings. Gathering location.")
            ip_info = IpInfoDB(self.commercial["ip_info"]["api_key"])
            locations["IP_Info"] = (ip_info.get_location(ip_address))

            if self.commercial["ip_info"]["generate_marker"]:
                logger.debug("""Folium marker for IP Info database is set as Active in settings. Calling add_to_map method.""")
                ip_info.add_to_map()

        # Json settings parsed for DbIpWeb database
        if self.commercial["ip_web"]["active"]:
            logger.debug("database DbIpWeb is set as Active in settings. Gathering location.")
            ip_web = IpWebDB()
            locations["DbIpWeb"] = (ip_web.get_location(ip_address))

            if self.commercial["ip_web"]["generate_marker"]:
                logger.debug("""Folium marker for DbIpWeb database is set as Active in settings. Calling add_to_map method.""")
                ip_web.add_to_map()

        # Json settings parsed for DbIpWeb database
        if self.commercial["ip2location_web"]["active"]:
            logger.debug("Database IP2LocationWeb is set Active in settings. Gathering location.")
            ip2location_web = Ip2locationWebDB()
            locations["IP2Location_Web"] = (ip2location_web.get_location(ip_address))

            if self.commercial["ip2location_web"]["generate_marker"]:
                logger.debug("""Folium marker for DbIpWeb database is set as Active in settings. Calling add_to_map method.""")
                ip2location_web.add_to_map()

        # Json settings parsed for MaxMindGeoIp2City database
        if self.commercial["max_mind"]["active"]:
            logger.debug("""database MaxMindGeoIp2City is set as Active in settings. Gathering location.""")
            max_mind = MaxMindDB()
            locations["MaxMindGeoIp2City"] = (max_mind.get_location(ip_address))

            if self.commercial["max_mind"]["generate_marker"]:
                logger.debug("""Folium marker for MaxMindGeoIp2City database is set as Active in settings. Calling add_to_map method.""")
                max_mind.add_to_map()

        # Json settings parsed for NeustarWeb database
        if self.commercial["neustar_web"]["active"]:
            logger.debug("database NeustarWeb is set Active in settings. Gathering location.")
            neustar_web = NeustarWebDB()
            locations["NeustarWeb"] = (neustar_web.get_location(ip_address))

            if self.commercial["neustar_web"]["generate_marker"]:
                logger.debug("""Folium marker for NeustarWeb database is set as Active in settings. Calling add_to_map method.""")
                neustar_web.add_to_map()

        # Json settings parsed for Skyhook database
        if self.commercial["skyhook"]["active"]:
            logger.debug("database Skyhook is set as Active in settings. Gathering location.")
            skyhook = SkyhookDB()
            locations["Skyhook"] = (skyhook.get_location(ip_address))

            if self.commercial["skyhook"]["generate_marker"]:
                logger.debug("""Folium marker for Skyhook database is set as Active in settings. Calling add_to_map method.""")
                skyhook.add_to_map()

        self.locations = {key: value for key, value in locations.items() if value is not None}

    def calculate(self, average=True, clustering=False, interval=False, median=False):
        """
        Method for calculating more acurate location with statistical calculation

        There are four available methods: Average (default method), Clustering, Confidence Interval
        and Median. For multiple selected methods returns namedtuple list:
        (Location.latitude, location.longitude).
        """
        logger.debug("Method calculate has been called.")
        calculated_locations = {}
        f_map = FoliumMap()

        # No calculation if databases did not rethrieved data
        if len(self.locations) < 2:
            return None

        # Calculate average of locations (default method)
        if average:
            logger.debug(
                "Calculation of Averaged location is Active.")
            # Get location from static method
            location = Average.calculate(self.locations)
            # Add marker
            f_map.add_calculated_marker("Average", self.ip_address, location.latitude,
                                        location.longitude)
            # Append calculated location into list
            calculated_locations["Average"] = location

        # Calculate location with SciPy Clustering
        if clustering:
            logger.debug("Clustering of location is Active.")
            location = Clustering.calculate(self.locations)
            f_map.add_calculated_marker("Clustering", self.ip_address, location.latitude,
                                        location.longitude)
            calculated_locations["Clustering"] = location

        # Calculate location from 90% Confdence interval
        if interval:
            logger.debug("Calculation of Confidence Interval from location is Active.")

        # Calculate Median from given locations
        if median:
            logger.debug("Calculation of Median from locations is Active.")
            location = Median.calculate(self.locations)
            f_map.add_calculated_marker("Median", self.ip_address, location.latitude,
                                        location.longitude)
            calculated_locations["Median"] = location

        # Generate map file?
        if self.generate_map:
            logger.debug("Generating map file is set as Active")
            # Create PolyLines
            f_map.add_poly_lines(self.locations, calculated_locations)
            # Generate map file
            f_map.generate_map(location)

        # Return calculated Locations
        logger.info("Returning list of locations: %s", str(calculated_locations))
        return calculated_locations
