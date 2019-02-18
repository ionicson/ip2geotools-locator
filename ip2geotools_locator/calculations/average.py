"""Module for calculating estimate of average location"""
from ip2geotools_locator.utils import Location, LOGGER as logger

# pylint: disable=too-few-public-methods
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
        logger.info("%s: Calculation of Average location started.", __name__)

        __latitude = 0.0
        __longitude = 0.0
        # Tracking of calculable locations
        __items = 0.0

        for loc in locations:
            # sum of locations (None locations are skipped)
            try:
                __latitude += loc.latitude
                __longitude += loc.longitude
                __items += 1

                logger.debug("""%s: Calculation of Average. Iteration: %.0f, Latitude sum: %.3f,
                             Longitude sum: %.3f""", __name__, __items, __latitude, __longitude)
            except AttributeError as exception:
                logger.warning("%s: value excluded from calculation. AttributeError: %s",
                               __name__, str(exception))

        try:
            # Calculate Average and return as Location
            logger.info("%s: Calculated Average location form %.0f DB responses is: %.3f N, %.3f",
                        __name__, __items, __latitude / __items, __longitude / __items)
            return Location(round(__latitude / __items, 4), round(__longitude / __items, 4))
        except ZeroDivisionError as exception:
            # If None locations were provided
            logger.critical("%s: None database have returned values. ZeroDivisionError: %s",
                            __name__, str(exception))
