# -*- coding: utf-8 -*-
"""
Main applicaton module
======================

This module contains whole application logic

"""
import json

from ip2geotools_locator.calculations import Average, Clustering, Median
from ip2geotools_locator.database_connectors import (EurekDB, GeobytesCityDB,
                                                     HostIpDB, Ip2LocationDB,
                                                     Ip2locationWebDB,
                                                     IpCityDB, IpInfoDB,
                                                     IpstackDB, IpWebDB,
                                                     MaxMindDB, MaxMindLiteDB,
                                                     NeustarWebDB, SkyhookDB)
from ip2geotools_locator.folium_map import FoliumMap
from ip2geotools_locator.utils import DEFAULT_SETTINGS
from ip2geotools_locator.utils import LOGGER as logger
from ip2geotools_locator.utils import Location


class Locator:
    """
    This class manages settings, Database connections and Calculations
    """
    ip_address = None

    # List of locations
    locations = {}

    def __init__(self, generate_map=True, map_file_name="locations"):
        """
        __init__ method which reads settings.json file.
        """
        # Should application generate Folium map file map_file_name.html?
        self.generate_map = generate_map
        self.map_file_name = map_file_name

        # Read settings.json
        try:
            with open("settings.json", "r") as read_file:
                self.settings = json.load(read_file)
                logger.info("Reading settings.json file.")
        except FileNotFoundError:
            self.settings = json.loads(DEFAULT_SETTINGS)
            logger.info("Loading default settings.")
            with open("settings.json", "w") as write_file:
                json.dump(self.settings, write_file, indent=4, sort_keys=True)
                logger.info("Settings are saved into settings.json file.")

        logger.debug("Settings parsed for commercial and noncommercial databases.")


    def fetch_locations(self, ip_address):
        """
        Method which searches through selected databases for location of given IP address.
        Accepts selection of databases as list (defaultly settings are loaded from settings.json).
        Use ["commercial"], ["noncommercial"] databases or specify them ["host_ip", "ipstack", ...]
        Data are stored in "locations" list variable.
        """
        locations = {}
        self.ip_address = ip_address
        commercial_db_settings = self.settings["commercial"]
        noncommercial_db_settings = self.settings["noncommercial"]

        logger.info("Gathering location records for IP address %s.", ip_address)

        # Noncommercial databases
        # Json settings parsed for HostIP database
        if noncommercial_db_settings["host_ip"]["active"]:
            logger.debug("Database HostIP is set as Active in settings. Gathering location.")
            # Create object for accessing database and store returned location
            host_ip = HostIpDB()
            locations["HostIP"] = (host_ip.get_location(ip_address))

            # Add location to the map?
            if noncommercial_db_settings["host_ip"]["generate_marker"] is True and self.generate_map is True:
                logger.debug("""Folium marker for HostIP database is set as Active in settings. Calling add_to_map method.""")
                host_ip.add_to_map()

        # Json settings parsed for DbIpCity database
        if noncommercial_db_settings["ip_city"]["active"]:
            logger.debug("Database DbIpCity is set as Active in settings. Gathering location.")
            ip_city = IpCityDB()
            locations["DbIpCity"] = (ip_city.get_location(ip_address))

            if noncommercial_db_settings["ip_city"]["generate_marker"] is True and self.generate_map is True:
                logger.debug("""Folium marker for DbIpCity database is set Active in settings. Calling add_to_map method.""")
                ip_city.add_to_map()

        # Json settings parsed for Ip2location database
        if noncommercial_db_settings["ip2location"]["active"]:
            logger.debug("""database Ip2location is set as Active in settings. Gathering location.""")
            ip2location = Ip2LocationDB(
                noncommercial_db_settings["ip2location"]["db_file"])
            locations["Ip2location"] = (ip2location.get_location(ip_address))

            if noncommercial_db_settings["ip2location"]["generate_marker"] is True and self.generate_map is True:
                logger.debug("""Folium marker for Ip2location database is set as Active in settings. Calling add_to_map method.""")
                ip2location.add_to_map()

        # Json settings parsed for Ipstack database
        if noncommercial_db_settings["ipstack"]["active"]:
            logger.debug("database Ipstack is set as Active in settings. Gathering location.")
            ipstack = IpstackDB(noncommercial_db_settings["ipstack"]["api_key"])
            locations["Ipstack"] = (ipstack.get_location(ip_address))

            if noncommercial_db_settings["ipstack"]["generate_marker"] is True and self.generate_map is True:
                logger.debug("""Folium marker for Ipstack database is set as Active in settings. Calling add_to_map method.""")
                ipstack.add_to_map()

        # Json settings parsed for MaxMind GeoLite2City database
        if noncommercial_db_settings["max_mind_lite"]["active"]:
            logger.debug("""database MaxMind GeoLite2City is set as Active in settings. Gathering location.""")
            max_mind_lite = MaxMindLiteDB(
                noncommercial_db_settings["max_mind_lite"]["db_file"])
            locations["MaxMind_GeoLite2City"] = (max_mind_lite.get_location(ip_address))

            if noncommercial_db_settings["max_mind_lite"]["generate_marker"] is True and self.generate_map is True:
                logger.debug("""Folium marker for MaxMind GeoLite2City database is set as Active in settings. Calling add_to_map method.""")
                max_mind_lite.add_to_map()

        # Commercial Databases
        # Json settings parsed for Eurek database
        if commercial_db_settings["eurek"]["active"]:
            logger.debug("""database Eurek is set as Active in settings. Gathering location.""")
            eurek = EurekDB()
            locations["Eurek"] = (eurek.get_location(ip_address))

            if commercial_db_settings["eurek"]["generate_marker"] is True and self.generate_map is True:
                logger.debug("""Folium marker for Eurek database is set as Active in settings. Calling add_to_map method.""")
                eurek.add_to_map()

        # Json settings parsed for GeobytesCityDetails database
        if commercial_db_settings["geobytes_city"]["active"]:
            logger.debug("""database GeobytesCityDetails is set as Active in settings. Gathering location.""")
            geobytes_city = GeobytesCityDB()
            locations["GeobytesCityDetails"] = (geobytes_city.get_location(ip_address))

            if commercial_db_settings["geobytes_city"]["generate_marker"] is True and self.generate_map is True:
                logger.debug("""Folium marker for GeobytesCityDetails database is set as Active in settings. Calling add_to_map method.""")
                geobytes_city.add_to_map()

        # Json settings parsed for IP Info database
        if commercial_db_settings["ip_info"]["active"]:
            logger.debug(
                "database IP Info is set as Active in settings. Gathering location.")
            ip_info = IpInfoDB(commercial_db_settings["ip_info"]["api_key"])
            locations["IP_Info"] = (ip_info.get_location(ip_address))

            if commercial_db_settings["ip_info"]["generate_marker"] is True and self.generate_map is True:
                logger.debug("""Folium marker for IP Info database is set as Active in settings. Calling add_to_map method.""")
                ip_info.add_to_map()

        # Json settings parsed for DbIpWeb database
        if commercial_db_settings["ip_web"]["active"]:
            logger.debug("database DbIpWeb is set as Active in settings. Gathering location.")
            ip_web = IpWebDB()
            locations["DbIpWeb"] = (ip_web.get_location(ip_address))

            if commercial_db_settings["ip_web"]["generate_marker"] is True and self.generate_map is True:
                logger.debug("""Folium marker for DbIpWeb database is set as Active in settings. Calling add_to_map method.""")
                ip_web.add_to_map()

        # Json settings parsed for DbIpWeb database
        if commercial_db_settings["ip2location_web"]["active"]:
            logger.debug("Database IP2LocationWeb is set Active in settings. Gathering location.")
            ip2location_web = Ip2locationWebDB()
            locations["IP2Location_Web"] = (ip2location_web.get_location(ip_address))

            if commercial_db_settings["ip2location_web"]["generate_marker"] is True and self.generate_map is True:
                logger.debug("""Folium marker for DbIpWeb database is set as Active in settings. Calling add_to_map method.""")
                ip2location_web.add_to_map()

        # Json settings parsed for MaxMindGeoIp2City database
        if commercial_db_settings["max_mind"]["active"]:
            logger.debug("""database MaxMindGeoIp2City is set as Active in settings. Gathering location.""")
            max_mind = MaxMindDB()
            locations["MaxMindGeoIp2City"] = (max_mind.get_location(ip_address))

            if commercial_db_settings["max_mind"]["generate_marker"] is True and self.generate_map is True:
                logger.debug("""Folium marker for MaxMindGeoIp2City database is set as Active in settings. Calling add_to_map method.""")
                max_mind.add_to_map()

        # Json settings parsed for NeustarWeb database
        if commercial_db_settings["neustar_web"]["active"]:
            logger.debug("database NeustarWeb is set Active in settings. Gathering location.")
            neustar_web = NeustarWebDB()
            locations["NeustarWeb"] = (neustar_web.get_location(ip_address))

            if commercial_db_settings["neustar_web"]["generate_marker"] is True and self.generate_map is True:
                logger.debug("""Folium marker for NeustarWeb database is set as Active in settings. Calling add_to_map method.""")
                neustar_web.add_to_map()

        # Json settings parsed for Skyhook database
        if commercial_db_settings["skyhook"]["active"]:
            logger.debug("database Skyhook is set as Active in settings. Gathering location.")
            skyhook = SkyhookDB()
            locations["Skyhook"] = (skyhook.get_location(ip_address))

            if commercial_db_settings["skyhook"]["generate_marker"] is True and self.generate_map is True:
                logger.debug("""Folium marker for Skyhook database is set as Active in settings. Calling add_to_map method.""")
                skyhook.add_to_map()

        # Clean all tangling None values
        self.locations = {key: value for key, value in locations.items() if value is not None}

    def calculate(self, average=True, clustering=False, median=False):
        """
        Method for calculating more acurate location with statistical calculation

        There are four available methods: Average (default method), Clustering, Confidence Interval
        and Median. For multiple selected methods returns namedtuple list:
        (Location.latitude, location.longitude).
        """
        logger.debug("Calculation started for %i DB entries.", len(self.locations))
        calculated_locations = {}
        f_map = FoliumMap()

        # No calculation if databases did not rethrieved data
        if len(self.locations) < 2:
            logger.error("Not enough locations to start calculation!")
            return None

        # Calculate average of locations (default method)
        if average:
            logger.debug("Calculation of Averaged location is Active.")
            # Get location from static method
            location = Average.calculate(self.locations)
            # Add marker
            f_map.add_calculated_marker("Average", self.ip_address, location.latitude, location.longitude)
            # Append calculated location into list
            calculated_locations["Average"] = location

        # Calculate location with SciPy Clustering
        if clustering:
            logger.debug("Calculation of location data cluster centroid is Active.")
            location = Clustering.calculate(self.locations)
            f_map.add_calculated_marker("Clustering", self.ip_address, location.latitude, location.longitude)
            calculated_locations["Clustering"] = location

        # Calculate Median from given locations
        if median:
            logger.debug("Calculation of Median from locations is Active.")
            location = Median.calculate(self.locations)
            f_map.add_calculated_marker("Median", self.ip_address, location.latitude, location.longitude)
            calculated_locations["Median"] = location

        # Generate map file?
        if self.generate_map:
            logger.debug("Generating map file.")

            if len(calculated_locations) > 0:
                # Create PolyLines for calculated locations
                f_map.add_poly_lines(self.locations, calculated_locations)
            else:
                # If no calculation succeded, generate map only from db data, focus is on first location entry in locations dist.
                location = Location(self.locations[next(iter(self.locations))].latitude, self.locations[next(iter(self.locations))].longitude)

            # Generate map file
            f_map.generate_map(location, self.map_file_name)

        if calculated_locations is not True:
            logger.warning("Calculations could not be finished due to invalid settings or bad data.")
        # Return calculated or uncalculated locations
        return calculated_locations

    def get_locations(self):
        """Method returns dictionary of gathered location objects."""
        return self.locations

    def get_settings(self):
        """Method returns loaded configuration in from of dictionary."""
        return self.settings

    def set_settings(self, settings):
        """Method returns loaded configuration in from of dictionary."""
        self.settings = settings

    def save_settings(self):
        """Method returns loaded configuration in from of dictionary."""
        with open("settings.json", "w") as write_file:
            json.dump(self.settings, write_file, indent=4, sort_keys=True)
            logger.info("Settings are saved into settings.json file.")
