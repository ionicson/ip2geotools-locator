import folium

class FoliumMap:
    """
    Class for creating Folium maps.
    """

    markers = []
    formatted_string= """
    <b>IP: %s</b>
    <p>Country: %s</p>
    <p>City: %s</p>
    <p>Location: %f, %f </p>
    """

    @classmethod
    def add_marker_noncommercial(cls, name, ip_address, country, city, latitude, longitude):

        cls.markers.append(folium.Marker([latitude, longitude], popup=cls.formatted_string % (ip_address, country, city, latitude, longitude), 
        icon=folium.Icon(color='blue'), tooltip=name))
    
    @classmethod
    def add_marker_commercial(cls, name, ip_address, country, city, latitude, longitude):

        cls.markers.append(folium.Marker([latitude, longitude], popup=cls.formatted_string % (ip_address, country, city, latitude, longitude), 
        icon=folium.Icon(color='red'), tooltip=name))
    
    @classmethod
    def add_calculated_marker(cls, name, ip_address, latitude, longitude):

        cls.markers.append(folium.Marker([latitude, longitude], popup="<p><b>%s</b> location of IP: %s is:</p><p>%f N %f E</p>" % (name, ip_address, latitude, longitude), 
        icon=folium.Icon(color='blue', icon='screenshot'), tooltip=name))

    @classmethod  
    def generate_map(cls, center_location=[], file_name="locations"):
        
        map = folium.Map(location = center_location)

        for marker in cls.markers:
            marker.add_to(map)

        map.save(str(file_name)+".html")