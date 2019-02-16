"""Module for calculating estimate of median location"""
from ip2geotools_locator.utils import Location, LOGGER as logger

# pylint: disable=too-few-public-methods
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
        logger.info("%s: Calculation of Median location started.", __name__)
        # List of latitudes and longitudes
        __latitudes = []
        __longitudes = []
        __latitude = 0.0
        __longitude = 0.0
        __iteration = 0

        for loc in locations:
            # Locations divided into latitude longitude lists
            try:
                __latitudes.append(loc.latitude)
                __longitudes.append(loc.longitude)
                __iteration += 1

                logger.debug("%s: separation of latitudes and longitudes. %i iteration.", __name__,
                             __iteration)

            except AttributeError as exception:
                # None values from database are skipped
                logger.warning("%s: value excluded from iterration. AttributeError: %s", __name__,
                               str(exception))

        # If both lists have same length median can be calculated
        if len(__latitudes) == len(__longitudes):
            # Sorting of lists
            __latitudes.sort()
            __longitudes.sort()

            logger.debug("%s: sorting of values.", __name__)

            # If number of elements is even, median is calculated as average of two central values
            if len(__latitudes) % 2 == 0:
                logger.debug("""%s: len() of location list is even number. Calculating average of
                             closest middle values.""", __name__)

                index = int(len(__longitudes) / 2)
                __latitude = (__latitudes[index] + __latitudes[index - 1]) / 2
                __longitude = (__longitudes[index] + __longitudes[index - 1]) /2

                logger.info("%s Calculated Median location form %i DB responses is: %.3f N, %.3f",
                            __name__, __iteration, __latitude, __longitude)
                return Location(round(__latitude, 4), round(__longitude, 4))

            # If number of elements is odd, the median is in the middle of list
            if len(__latitudes) % 2 != 0:
                logger.debug("%s: len() of location list is odd number. Calculating real median.",
                             __name__)

                index = int((len(__latitudes) - 1) / 2)
                __latitude = __latitudes[index]
                __longitude = __longitudes[index]

                logger.info("%s: Calculated Median location form %i DB responses is: %.3f N, %.3f",
                            __name__, __iteration, __latitude, __longitude)
                return Location(round(__latitude, 4), round(__longitude, 4))

            # Handling for empty lists
            logger.error("%s: None database have returned values.", __name__)
            return 0

        logger.critical("%s: Calculation of median canceled due to OTHER error!", __name__)
        return 0
