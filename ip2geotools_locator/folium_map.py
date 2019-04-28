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
    <div><b>IP: %s</b><p>Country: %s</p><p>Region: %s</p><p>City: %s</p><p>Location: Latitude - %.3f, Longitude - %.3f</p></div>
    """
    @classmethod
    def add_marker(cls, name, location_data, commercial):
        """This method creates marker for noncommercial database"""
        if commercial is True:
            color = 'red'
            db_type = 'commercial'
        else:
            color = 'green'
            db_type = 'noncommercial'
        # Adding debug record
        logger.info("Adding Marker for %s DB %s", db_type, name)
        # append Folium Marker into class variable
        cls.markers.append(folium.Marker([location_data.latitude, location_data.longitude], popup=cls.FORMATTED_STRING %
                                         (location_data.ip_address, location_data.country, location_data.region, location_data.city, location_data.latitude, location_data.longitude),
                                         icon=folium.Icon(color=color), tooltip=name))


    @classmethod
    def add_calculated_marker(cls, name, ip_address, latitude, longitude):
        """This method creates marker for calculated location"""

        # Adding debug record
        logger.info("%s: Adding Marker for %s calculation method", __name__, name)
        # append Folium Marker into class variable
        cls.markers.append(folium.Marker([latitude, longitude], popup="""<p><b>%s</b> location of IP: %s is:</p><p>%f N %f E</p>""" % (name, ip_address, latitude, longitude),
                                         icon=folium.Icon(color='blue', icon='screenshot'), tooltip=name))

    @classmethod
    def add_poly_lines(cls, locations, calculated_locations):
        """Method for creating Folium PolyLines"""

        # Add polylines from each calculated location
        for calc_loc in calculated_locations:
            logger.info("Creating Folium PolyLines for %s", str(calc_loc))
            # For each DB location
            for loc in locations:
                # Calculate distance between coordinates
                dist = distance.distance([locations[loc].latitude, locations[loc].longitude], calculated_locations[calc_loc]).km
                # Add Folium PolyLine
                cls.poly_lines.append(folium.PolyLine([[locations[loc].latitude, locations[loc].longitude], calculated_locations[calc_loc]], tooltip="Distance: %.3f km" % dist, weight=3, opacity=1))


    @classmethod
    def generate_map(cls, center_location=None, file_name="locations"):
        """Method for generating map file."""
        try:
            # Create Folium map object
            f_map = folium.Map([center_location.latitude, center_location.longitude])

            # Add all markers to map
            logger.debug("Adding Markers into map.")
            for marker in cls.markers:
                marker.add_to(f_map)

            # Add all PolyLines to map
            logger.debug("Adding PolyLines into map.")
            for line in cls.poly_lines:
                line.add_to(f_map)

            # Save map in html format
            logger.info("Generating map file %s.html", file_name)

            f_map.save(str(file_name)+".html")

        except TypeError as exception:
            logger.error("Error creating map file! TypeError: %s", str(exception))
