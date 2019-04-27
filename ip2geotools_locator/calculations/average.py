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

        latitude = 0.0
        longitude = 0.0
        # Tracking of calculable locations
        items = 0.0

        for loc in locations:
            # sum of locations (None locations are skipped)
            try:
                latitude += locations[loc].latitude
                longitude += locations[loc].longitude
                items += 1

                logger.debug("""Calculation of Average. Iteration: %.0f, Latitude sum: %.3f, Longitude sum: %.3f""", items, latitude, longitude)
            except AttributeError as exception:
                logger.warning("Value excluded from calc. AttributeError: %s", str(exception))

        try:
            # Calculate Average and return as Location
            logger.info("Calculated Average location form %.0f DB responses is: %.3f N, %.3f E", items, latitude / items, longitude / items)
            return Location(round(latitude / items, 4), round(longitude / items, 4))
        except ZeroDivisionError as exception:
            # If None locations were provided
            logger.critical("Databases not returned values. ZeroDivisionError: %s", str(exception))
