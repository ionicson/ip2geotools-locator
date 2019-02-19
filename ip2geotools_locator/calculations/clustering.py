"""Module for estimating geographical location by K-Means cluster center calculation"""
import numpy
from sklearn.cluster import KMeans
from kneed import KneeLocator

from ip2geotools_locator.utils import Location, LOGGER as logger


class Clustering():
    """
    Class for calculating Cluster centroid from list of Locations
    """
    # pylint: disable=too-few-public-methods, invalid-name, too-many-locals
    @staticmethod
    def calculate(locations=None):
        """
        Static method calculates Data cluster centers of given location list.
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

        # Data transformation
        X = numpy.array(list(zip(__latitudes, __longitudes))).reshape(len(__latitudes), 2)

        sum_of_squared_distances = []

        # Estimating ideal K from elbow function
        K = range(1, __iteration)
        for k in K:
            kmeans_model = KMeans(n_clusters=k).fit(X)
            sum_of_squared_distances.append(kmeans_model.inertia_)

        kn = KneeLocator(K, sum_of_squared_distances, curve='convex', direction='decreasing')

        # KMeans algorithm
        K = kn.knee
        kmeans_model = KMeans(n_clusters=K).fit(X)
        centers = numpy.array(kmeans_model.cluster_centers_)

        center_locations = centers.tolist()
        __latitude = center_locations[0][0]
        __longitude = center_locations[0][1]

        return Location(round(__latitude, 4), round(__longitude, 4))
