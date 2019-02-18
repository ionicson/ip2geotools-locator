# -*- coding: utf-8 -*-
"""
Main applicaton module
======================

This module contains whole application logic

"""
import json
from collections import namedtuple

from ip2geotools_locator.database_connectors import (HostIpDB, IpCityDB, Ip2LocationDB, IpstackDB,
                                                     MaxMindLiteDB)
from ip2geotools_locator.database_connectors import (EurekDB, GeobytesCityDB, IpInfoDB, IpWebDB,
                                                     Ip2locationWebDB, MaxMindDB, NeustarWebDB,
                                                     SkyhookDB)
from ip2geotools_locator.calculations import Average, Median
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
    locations = []

    def __init__(self, generate_map=True):
        """
        __init__ method which reads settings.json file.
        """
        logger.info("%s: Reading settings.json file", __name__)

        # Should application generate Folium map file? (Default false)
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

        logger.debug(
            "%s: Settings parsed for commercial and noncommercial databases.", __name__)

    # pylint: disable=too-many-locals
    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements
    def get_locations(self, ip_address, databases=None):
        """
        Method which searches through selected databases for location of given IP address.
        Accepts selection of databases as list (defaultly settings are loaded from settings.json).
        Use ["commercial"], ["noncommercial"] databases or specify them ["host_ip", "ipstack", ...]
        Data are stored in "locations" list variable.
        """
        self.ip_address = ip_address
        logger.info(
            "%s: Gathering location records for IP address %s.", __name__, ip_address)

        # Change settings according to provided database list;
        if "noncommercial" in databases:
            logger.debug(
                "%s: Adjusting settings for all noncommercial databases.", __name__)

            # Each noncomercial database is activated
            for database in self.noncommercial:
                self.noncommercial[database]["active"] = True
            # Each comercial database is deactivated
            for database in self.commercial:
                self.commercial[database]["active"] = False

        elif "commercial" in databases:
            logger.debug(
                "%s: Adjusting settings for all commercial databases.", __name__)

            # Each noncomercial database is deactivated
            for database in self.noncommercial:
                self.noncommercial[database]["active"] = False
            # Each comercial database is activated
            for database in self.commercial:
                self.commercial[database]["active"] = True

        else:
            # Configure each DB
            for i in databases:
                logger.debug(
                    "%s: Adjusting settings for database %s.", __name__, i)
                if i in self.noncommercial:
                    self.noncommercial[i]["active"] = True
                elif i in self.commercial:
                    self.commercial[i]["active"] = True

        # Noncommercial databases
        # Json settings parsed for HostIP database
        if self.noncommercial["host_ip"]["active"]:
            logger.debug(
                "%s: database HostIP is set as Active in settings. Gathering location.", __name__)
            # Create object for accessing database and store returned location
            host_ip = HostIpDB()
            self.locations.append(host_ip.get_location(ip_address))

            # Add location to the map?
            if self.noncommercial["host_ip"]["generate_marker"]:
                logger.debug("""%s: Folium marker for HostIP database is set as Active in settings.
                             Calling add_to_map method.""", __name__)
                host_ip.add_to_map()

        # Json settings parsed for DbIpCity database
        if self.noncommercial["ip_city"]["active"]:
            logger.debug("%s: database DbIpCity is set as Active in settings. Gathering location.",
                         __name__)
            ip_city = IpCityDB()
            self.locations.append(ip_city.get_location(ip_address))

            if self.noncommercial["ip_city"]["generate_marker"]:
                logger.debug("""%s: Folium marker for DbIpCity database is set Active in settings.
                             Calling add_to_map method.""", __name__)
                ip_city.add_to_map()

        # Json settings parsed for Ip2location database
        if self.noncommercial["ip2location"]["active"]:
            logger.debug("""%s: database Ip2location is set as Active in settings. Gathering
                         location.""", __name__)
            ip2location = Ip2LocationDB(
                self.noncommercial["ip2location"]["db_file"])
            self.locations.append(ip2location.get_location(ip_address))

            if self.noncommercial["ip2location"]["generate_marker"]:
                logger.debug("""%s: Folium marker for Ip2location database is set as Active in
                             settings. Calling add_to_map method.""", __name__)
                ip2location.add_to_map()

        # Json settings parsed for Ipstack database
        if self.noncommercial["ipstack"]["active"]:
            logger.debug(
                "%s: database Ipstack is set as Active in settings. Gathering location.", __name__)
            ipstack = IpstackDB(self.noncommercial["ipstack"]["api_key"])
            self.locations.append(ipstack.get_location(ip_address))

            if self.noncommercial["ipstack"]["generate_marker"]:
                logger.debug("""%s: Folium marker for Ipstack database is set as Active in settings.
                             Calling add_to_map method.""", __name__)
                ipstack.add_to_map()

        # Json settings parsed for MaxMind GeoLite2City database
        if self.noncommercial["max_mind_lite"]["active"]:
            logger.debug("""%s: database MaxMind GeoLite2City is set as Active in settings.
                         Gathering location.""", __name__)
            max_mind_lite = MaxMindLiteDB(
                self.noncommercial["max_mind_lite"]["db_file"])
            self.locations.append(max_mind_lite.get_location(ip_address))

            if self.noncommercial["max_mind_lite"]["generate_marker"]:
                logger.debug("""%s: Folium marker for MaxMind GeoLite2City database is set as Active
                             in settings. Calling add_to_map method.""", __name__)
                max_mind_lite.add_to_map()

        # Commercial Databases
        # Json settings parsed for Eurek database
        if self.commercial["eurek"]["active"]:
            logger.debug("""%s: database Eurek is set as Active in settings. Gathering location.""",
                         __name__)
            eurek = EurekDB()
            self.locations.append(eurek.get_location(ip_address))

            if self.commercial["eurek"]["generate_marker"]:
                logger.debug("""%s: Folium marker for Eurek database is set as Active in settings.
                             Calling add_to_map method.""", __name__)
                eurek.add_to_map()

        # Json settings parsed for GeobytesCityDetails database
        if self.commercial["geobytes_city"]["active"]:
            logger.debug("""%s: database GeobytesCityDetails is set as Active in settings. Gathering
                         location.""", __name__)
            geobytes_city = GeobytesCityDB()
            self.locations.append(geobytes_city.get_location(ip_address))

            if self.commercial["geobytes_city"]["generate_marker"]:
                logger.debug("""%s: Folium marker for GeobytesCityDetails database is set as Active
                             in settings. Calling add_to_map method.""", __name__)
                geobytes_city.add_to_map()

        # Json settings parsed for IP Info database
        if self.commercial["ip_info"]["active"]:
            logger.debug(
                "%s: database IP Info is set as Active in settings. Gathering location.", __name__)
            ip_info = IpInfoDB(self.commercial["ip_info"]["api_key"])
            self.locations.append(ip_info.get_location(ip_address))

            if self.commercial["ip_info"]["generate_marker"]:
                logger.debug("""%s: Folium marker for IP Info database is set as Active in settings.
                             Calling add_to_map method.""", __name__)
                ip_info.add_to_map()

        # Json settings parsed for DbIpWeb database
        if self.commercial["ip_web"]["active"]:
            logger.debug("%s: database DbIpWeb is set as Active in settings. Gathering location.",
                         __name__)
            ip_web = IpWebDB()
            self.locations.append(ip_web.get_location(ip_address))

            if self.commercial["ip_web"]["generate_marker"]:
                logger.debug("""%s: Folium marker for DbIpWeb database is set as Active in settings.
                             Calling add_to_map method.""", __name__)
                ip_web.add_to_map()

        # Json settings parsed for DbIpWeb database
        if self.commercial["ip2location_web"]["active"]:
            logger.debug("%s: database DbIpWeb is set as Active in settings. Gathering location.",
                         __name__)
            ip2location_web = Ip2locationWebDB()
            self.locations.append(ip2location_web.get_location(ip_address))

            if self.commercial["ip2location_web"]["generate_marker"]:
                logger.debug("""%s: Folium marker for DbIpWeb database is set as Active in settings.
                             Calling add_to_map method.""", __name__)
                ip2location_web.add_to_map()

        # Json settings parsed for MaxMindGeoIp2City database
        if self.commercial["max_mind"]["active"]:
            logger.debug("""%s: database MaxMindGeoIp2City is set as Active in settings. Gathering
                         location.""", __name__)
            max_mind = MaxMindDB()
            self.locations.append(max_mind.get_location(ip_address))

            if self.commercial["max_mind"]["generate_marker"]:
                logger.debug("""%s: Folium marker for MaxMindGeoIp2City database is set as Active in
                             settings. Calling add_to_map method.""", __name__)
                max_mind.add_to_map()

        # Json settings parsed for NeustarWeb database
        if self.commercial["neustar_web"]["active"]:
            logger.debug("%s: database NeustarWeb is set Active in settings. Gathering location.",
                         __name__)
            neustar_web = NeustarWebDB()
            self.locations.append(neustar_web.get_location(ip_address))

            if self.commercial["neustar_web"]["generate_marker"]:
                logger.debug("""%s: Folium marker for NeustarWeb database is set as Active in
                             settings. Calling add_to_map method.""", __name__)
                neustar_web.add_to_map()

        # Json settings parsed for Skyhook database
        if self.commercial["skyhook"]["active"]:
            logger.debug("%s: database Skyhook is set as Active in settings. Gathering location.",
                         __name__)
            skyhook = SkyhookDB()
            self.locations.append(skyhook.get_location(ip_address))

            if self.commercial["skyhook"]["generate_marker"]:
                logger.debug("""%s: Folium marker for Skyhook database is set as Active in settings.
                             Calling add_to_map method.""", __name__)
                skyhook.add_to_map()

    def calculate(self, average=True, clustering=False, interval=False, median=False):
        """
        Method for calculating more acurate location with statistical calculation

        There are four available methods: Average (default method), Clustering, Confidence Interval
        and Median. For multiple selected methods returns namedtuple list:
        (Location.latitude, location.longitude).
        """
        logger.debug("%s: Method calculate has been called.", __name__)
        calculated_locations = {}
        f_map = FoliumMap()

        # Calculate average of locations (default method)
        if average:
            logger.debug(
                "%s: Calculation of Averaged location is Active.", __name__)
            # Get location from static method
            location = Average.calculate(self.locations)
            # Add marker
            f_map.add_calculated_marker("Average", self.ip_address, location.latitude,
                                        location.longitude)
            # Append calculated location into list
            calculated_locations["Average"] = location

        # Calculate location with SciPy Clustering
        if clustering:
            logger.debug("%s: Clustering of location is Active.", __name__)
            #location = Clustering.calculate(self.locations)
            f_map.add_calculated_marker("Clustering", self.ip_address, location.latitude,
                                        location.longitude)
            calculated_locations["Clustering"] = location

        # Calculate location from 90% Confdence interval
        if interval:
            logger.debug("%s: Calculation of Confidence Interval from location is Active.",
                         __name__)

        # Calculate Median from given locations
        if median:
            logger.debug(
                "%s: Calculation of Median from locations is Active.", __name__)
            location = Median.calculate(self.locations)
            f_map.add_calculated_marker("Median", self.ip_address, location.latitude,
                                        location.longitude)
            calculated_locations["Median"] = location

        # Generate map file?
        if self.generate_map:
            logger.debug("%s: Generating map file is set as Active", __name__)
            # Create PolyLines
            f_map.add_poly_lines(self.locations, calculated_locations)
            # Generate map file
            f_map.generate_map(location)

        # Return calculated Locations
        logger.info("%s: Returning list of locations: %s",
                    __name__, str(calculated_locations))
        return calculated_locations
