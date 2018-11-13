import folium
from geopy import distance

class FoliumMap:
    """
    Class for creating Folium maps.
    """

    markers = []
    poly_lines = []
    FORMATTED_STRING= """
    <b>IP: %s</b>
    <p>Country: %s</p>
    <p>City: %s</p>
    <p>Location: %f, %f </p>
    """

    @classmethod
    def add_marker_noncommercial(cls, name, ip_address, country, city, latitude, longitude):
        """This method creates marker for noncommercial database"""
        try:
            cls.markers.append(folium.Marker([latitude, longitude], popup=cls.FORMATTED_STRING % (ip_address, country, city, latitude, longitude), 
            icon=folium.Icon(color='green'), tooltip=name))
        except TypeError:
            # None values are passed
            pass
    
    @classmethod
    def add_marker_commercial(cls, name, ip_address, country, city, latitude, longitude):
        """This method creates marker for commercial database"""
        try:
            cls.markers.append(folium.Marker([latitude, longitude], popup=cls.FORMATTED_STRING % (ip_address, country, city, latitude, longitude), 
            icon=folium.Icon(color='red'), tooltip=name))
        except TypeError:
            # None values are passed
            pass
    
    @classmethod
    def add_calculated_marker(cls, name, ip_address, latitude, longitude):
        """This method creates marker for calculated location"""
        try:
            cls.markers.append(folium.Marker([latitude, longitude], popup="<p><b>%s</b> location of IP: %s is:</p><p>%f N %f E</p>" % (name, ip_address, latitude, longitude), 
            icon=folium.Icon(color='blue', icon='screenshot'), tooltip=name))
        except TypeError:
            # None values are passed
            pass

    @classmethod
    def add_poly_lines(cls, locations, calculated_locations):
        """Method for creating Folium PolyLines"""
        
        for calculated_loc in calculated_locations:
            for loc in locations:
                try:
                    dist = distance.distance(loc, calculated_loc).km
                    cls.poly_lines.append(folium.PolyLine([loc, calculated_loc], tooltip = "Distance: %.3f km" % dist, weight=3, opacity=1))
                except TypeError:
                    # None values are passed
                    pass

    @classmethod  
    def generate_map(cls, center_location=[], file_name="locations"):
        """Method for generating map file."""
        try:
            # Create Folium map object
            map = folium.Map([center_location.latitude, center_location.longitude])

            # Add all markers to map
            for marker in cls.markers:
                marker.add_to(map)
            # Add all PolyLines to map
            for line in cls.poly_lines:
                line.add_to(map)

            # Save map in html format
            map.save(str(file_name)+".html")
        except TypeError:
            pass