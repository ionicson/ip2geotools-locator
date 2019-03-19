"""Module for interaction with folium map package"""
import folium
from geopy import distance

from ip2geotools_locator.utils import LOGGER as logger

class FoliumMap:
    """
    Class for creating Folium maps.
    """
    markers = []
    poly_lines = []
    FORMATTED_STRING = """
    <b>IP: %s</b><p>Country: %s</p><p>Region: %s</p><p>City: %s</p><p>Location: %.3f N, %.3f E</p>
    """
    # pylint: disable=too-many-arguments
    @classmethod
    def add_marker_noncommercial(cls, name, ip_address, country, region, city, latit, longit):
        """This method creates marker for noncommercial database"""

        try:
            # Adding debug record
            logger.info("%s: Adding Marker for noncommercial DB %s", __name__, name)
            # append Folium Marker into class variable
            cls.markers.append(folium.Marker([latit, longit],
                                             popup=cls.FORMATTED_STRING %
                                             (ip_address, country, region, city, latit, longit),
                                             icon=folium.Icon(color='green'), tooltip=name))

        except TypeError as exception:
            # Invalid values are skipped
            logger.warning("%s: TypeError: %s. Marker from %s DB skipped.", __name__,
                           str(exception), name)

    # pylint: disable=too-many-arguments
    @classmethod
    def add_marker_commercial(cls, name, ip_address, country, region, city, latit, longit):
        """This method creates marker for commercial database"""

        try:
            # Adding debug record
            logger.info("%s: Adding Marker for commercial DB %s", __name__, name)
            # append Folium Marker into class variable
            cls.markers.append(folium.Marker([latit, longit], popup=cls.FORMATTED_STRING %
                                             (ip_address, country, region, city, latit, longit),
                                             icon=folium.Icon(color='red'), tooltip=name))

        except TypeError as exception:
            # Invalid values are skipped
            logger.warning("%s: TypeError: %s. Marker from %s DB skipped.", __name__,
                           str(exception), name)


    @classmethod
    def add_calculated_marker(cls, name, ip_address, latitude, longitude):
        """This method creates marker for calculated location"""

        try:
            # Adding debug record
            logger.info("%s: Adding Marker for %s calculation method", __name__, name)
            # append Folium Marker into class variable
            cls.markers.append(folium.Marker([latitude, longitude],
                                             popup="""<p><b>%s</b> location of IP: %s is:</p><p>%f N
                                             %f E</p>""" % (name, ip_address, latitude, longitude),
                                             icon=folium.Icon(color='blue', icon='screenshot'),
                                             tooltip=name))

        except TypeError as exception:
            # Invalid values are skipped
            logger.warning("%s: TypeError: %s. Marker from %s method skipped.", __name__,
                           str(exception), name)


    @classmethod
    def add_poly_lines(cls, locations, calculated_locations):
        """Method for creating Folium PolyLines"""

        # Add polylines from each calculated location
        for calc_loc in calculated_locations:
            logger.info("%s: Creating Folium PolyLines for %s", __name__, str(calc_loc))
            # For each DB location
            for loc in locations:
                try:
                    # Calculate distance between coordinates
                    dist = distance.distance(locations[loc], calculated_locations[calc_loc]).km
                    # Add Folium PolyLine
                    cls.poly_lines.append(folium.PolyLine([locations[loc],
                                                           calculated_locations[calc_loc]],
                                                          tooltip="Distance: %.3f km" % dist,
                                                          weight=3, opacity=1))

                except TypeError as exception:
                    #Invalid values are skipped
                    logger.warning("%s: TypeError: %s. PolyLine skipped.", __name__, str(exception))


    @classmethod
    def generate_map(cls, center_location=None, file_name="locations"):
        """Method for generating map file."""

        try:
            # Create Folium map object
            f_map = folium.Map([center_location.latitude, center_location.longitude])

            # Add all markers to map
            logger.debug("%s: Adding Markers into map.", __name__)
            for marker in cls.markers:
                marker.add_to(f_map)

            # Add all PolyLines to map
            logger.debug("%s: Adding PolyLines into map.", __name__)
            for line in cls.poly_lines:
                line.add_to(f_map)

            # Save map in html format
            logger.info("%s: Generating map file %s.html", __name__, file_name)

            f_map.save(str(file_name)+".html")

        except TypeError as exception:
            logger.error("%s: Error creating map file! TypeError: %s", __name__, str(exception))
