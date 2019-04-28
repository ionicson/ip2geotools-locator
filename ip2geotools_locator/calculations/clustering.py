"""Module for estimating geographical location by K-Means cluster center calculation"""
import numpy
from kneed import KneeLocator
from sklearn.cluster import KMeans

from ip2geotools_locator.utils import LOGGER as logger
from ip2geotools_locator.utils import Location


class Clustering():
    """
    Class for calculating Cluster centroid from list of Locations
    """
    @staticmethod
    def calculate(locations=None):
        """
        Static method calculates Data cluster centers of given location list.
        Locations list must be in form of namedtuple and is also returned like that:

        Location = namedtuple('Location', 'latitude longitude')
        """
        logger.info("Calculation of location data cluster centroid started.")
        # List of latitudes and longitudes
        latitudes = []
        longitudes = []
        sum_of_squared_distances = []
        calculated_kmeans_models = []
        iteration = 0

        for loc in locations:
            # Locations divided into latitude longitude lists
            try:
                latitudes.append(locations[loc].latitude)
                longitudes.append(locations[loc].longitude)
                iteration += 1

                logger.debug("Separation of latitudes and longitudes. %i iteration.", iteration)

            except AttributeError as exception:
                # None values from database are skipped
                logger.warning("Value excluded from iterration. AttributeError: %s", str(exception))
        if len(locations) < 3:
            logger.warning("Not enough location data for using this method. At least 3 entries are needed.")
            return None
        # Data transformation into numpy array
        X = numpy.array(list(zip(latitudes, longitudes))).reshape(len(latitudes), 2)

        # Estimating ideal K from elbow function
        K = range(1, iteration)
        for k in K:
            kmeans_model = (KMeans(n_clusters=k).fit(X))
            sum_of_squared_distances.append(kmeans_model.inertia_)
            calculated_kmeans_models.append(kmeans_model)

            logger.debug("Calculating K-Means model for K = %i", k)

        try:
            knee_func = KneeLocator(K, sum_of_squared_distances, curve='convex', direction='decreasing')

            # Sellecting fittest KMeans algorithm model
            final_kmeans_model = calculated_kmeans_models[knee_func.knee - 1]
            logger.debug("Finding local extremes of knee function. K = %i,", knee_func.knee)

        except (TypeError, ValueError):
            final_kmeans_model = calculated_kmeans_models[0]
            logger.warning("No extremes found in K-Means optimalization. Calculating for K = 1. Result will be silmilar to Average.")

        center_locations = numpy.array(final_kmeans_model.cluster_centers_).tolist()

        # Return calculated location. Biggest cluster has always index 0
        logger.info("Calculated Median location form %i DB responses is: %.3f N, %.3f", iteration, center_locations[0][0], center_locations[0][1])
        return Location(round(center_locations[0][0], 4), round(center_locations[0][1], 4))
