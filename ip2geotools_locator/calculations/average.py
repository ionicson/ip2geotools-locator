from collections import namedtuple

#location is stored as namedtuple
Location = namedtuple('Location', 'latitude longitude')

class Average():   
    """
    Class for calculating Average location from list of Locations
    """
    @staticmethod
    def calculate(locations = []):
        __latitude  = 0.0
        __longitude = 0.0
        #Tracking of calculable locations
        __items = 0.0
        
        for loc in locations:
            #sum of locations (None locations are skipped)
            try:
                __latitude += loc.latitude
                __longitude += loc.longitude
                __items += 1
            except AttributeError as e:
                print(e)

        try:
            #Calculate Average and return as Location
            return Location(__latitude / __items, __longitude / __items)
        except ZeroDivisionError as e:
            #If None locations were provided
            print(e)
    