"""Module for calculating estimate of median location"""
from ip2geotools_locator.utils import Location, LOGGER as logger

class Median():
    """
    Class for calculating Median from list of Locations
    """
    @staticmethod
    def calculate(locations=None):
        """
        Static method calculates Median of given location list.
        Locations list must be in form of namedtuple and is also returned like that:

        Location = namedtuple('Location', 'latitude longitude')
        """
        logger.info("Calculation of Median location started.")
        # List of latitudes and longitudes
        latitudes = []
        longitudes = []
        latitude = 0.0
        longitude = 0.0
        iteration = 0

        for loc in locations:
            # Locations divided into latitude longitude lists
            try:
                latitudes.append(locations[loc].latitude)
                longitudes.append(locations[loc].longitude)
                iteration += 1

                logger.debug("separation of latitudes and longitudes. %i iteration.", iteration)

            except AttributeError as exception:
                # None values from database are skipped
                logger.warning("value excluded from iterration. AttributeError: %s", str(exception))

        # If both lists have same length median can be calculated
        if len(latitudes) == len(longitudes):
            # Sorting of lists
            latitudes.sort()
            longitudes.sort()

            logger.debug("sorting of values.")

            # If number of elements is even, median is calculated as average of two central values
            if len(latitudes) % 2 == 0:
                logger.debug("""len() of location list is even number. Calculating average of closest middle values.""")

                index = int(len(longitudes) / 2)
                latitude = (latitudes[index] + latitudes[index - 1]) / 2
                longitude = (longitudes[index] + longitudes[index - 1]) /2

                logger.info("Calculated Median location form %i DB responses is: %.3f N, %.3f", iteration, latitude, longitude)
                return Location(round(latitude, 4), round(longitude, 4))

            # If number of elements is odd, the median is in the middle of list
            if len(latitudes) % 2 != 0:
                logger.debug("len() of location list is odd number. Calculating real median.")

                index = int((len(latitudes) - 1) / 2)
                latitude = latitudes[index]
                longitude = longitudes[index]

                logger.info("Calculated Median location form %i DB responses is: %.3f N, %.3f", iteration, latitude, longitude)
                return Location(round(latitude, 4), round(longitude, 4))

            # Handling for empty lists
            logger.error("None database have returned values.")
            return 0

        logger.critical("Calculation of median canceled due to OTHER error!")
        return 0
