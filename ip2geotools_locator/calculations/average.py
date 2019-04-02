"""Module for calculating estimate of average location"""
from ip2geotools_locator.utils import Location, LOGGER as logger

class Average():
    """
    Class for calculating Average location from list of Locations
    """
    @staticmethod
    def calculate(locations=None):
        """
        Static method calculates Average of given location list.
        Locations list must be in form of namedtuple and is also returned like that:

        Location = namedtuple('Location', 'latitude longitude')
        """
        logger.info("Calculation of Average location started.")

        __latitude = 0.0
        __longitude = 0.0
        # Tracking of calculable locations
        __items = 0.0

        for loc in locations:
            # sum of locations (None locations are skipped)
            try:
                __latitude += locations[loc].latitude
                __longitude += locations[loc].longitude
                __items += 1

                logger.debug("""Calculation of Average. Iteration: %.0f, Latitude sum: %.3f,
                             Longitude sum: %.3f""", __items, __latitude, __longitude)
            except AttributeError as exception:
                logger.warning("Value excluded from calc. AttributeError: %s", str(exception))

        try:
            # Calculate Average and return as Location
            logger.info("Calculated Average location form %.0f DB responses is: %.3f N, %.3f",
                        __items, __latitude / __items, __longitude / __items)
            return Location(round(__latitude / __items, 4), round(__longitude / __items, 4))
        except ZeroDivisionError as exception:
            # If None locations were provided
            logger.critical("Databases not returned values. ZeroDivisionError: %s", str(exception))
