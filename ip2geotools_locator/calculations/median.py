from collections import namedtuple
import math

#location is stored as namedtuple
Location = namedtuple('Location', 'latitude longitude')

class Median():   
    """
    Class for calculating Median from list of Locations
    """
    @staticmethod
    def calculate(locations = []):
        """
        Static method calculates Median of given location list.
        Locations list must be in form of namedtuple and is also returned like that:

        Location = namedtuple('Location', 'latitude longitude')
        """
        # List of latitudes and longitudes
        __latitudes = []
        __longitudes = []
        __latitude = 0.0
        __longitude = 0.0
        
        for loc in locations:
            # Locations divided into latitude longitude lists
            try:
                __latitudes.append(loc.latitude)
                __longitudes.append(loc.longitude)
            except AttributeError as e:
                # None values from database are skipped
                print("Module " + __name__ + " has skipped wrong value due to: " + e.with_traceback)

        # If both lists have same length median can be calculated    
        if len(__latitudes) == len(__longitudes):
            # Sorting of lists
            __latitudes.sort()
            __longitudes.sort()
            
            # If number of elements is even, the median is calculated as an average of two central values
            if len(__latitudes) % 2 == 0:
                index = int(len(__longitudes) / 2)
                __latitude = (__latitudes[index] + __latitudes[index - 1]) / 2
                __longitude = (__longitudes[index] + __longitudes[index - 1]) /2

                return Location(__latitude, __longitude)

            # If number of elements is odd, the median is in the middle of list
            elif len(__latitudes) > 0:
                index = int((len(__latitudes) - 1) / 2)
                __latitude = __latitudes[index]
                __longitude = __longitudes[index]

                return Location(__latitude, __longitude)

            # Handling for empty lists
            else:
                print("Calculation of median canceled: No values retrieved from databases!")
            
        else:
            print("Calculation of median canceled due to OTHER error!")