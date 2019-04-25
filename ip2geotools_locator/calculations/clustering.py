"""Module for estimating geographical location by K-Means cluster center calculation"""
import numpy
from sklearn.cluster import KMeans
from kneed import KneeLocator

from ip2geotools_locator.utils import Location, LOGGER as logger


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
        logger.info("Calculation of Median location started.")
        # List of latitudes and longitudes
        __latitudes = []
        __longitudes = []
        sum_of_squared_distances = []
        calculated_kmeans_models = []
        clustered_data = [[]]
        clusters_inertia_list = []
        __iteration = 0

        for loc in locations:
            # Locations divided into latitude longitude lists
            try:
                __latitudes.append(locations[loc].latitude)
                __longitudes.append(locations[loc].longitude)
                __iteration += 1

                logger.debug("separation of latitudes and longitudes. %i iteration.",
                             __iteration)

            except AttributeError as exception:
                # None values from database are skipped
                logger.warning("value excluded from iterration. AttributeError: %s",
                               str(exception))

        # Data transformation into numpy array
        X = numpy.array(list(zip(__latitudes, __longitudes))).reshape(len(__latitudes), 2)

        # Estimating ideal K from elbow function
        K = range(1, __iteration)
        for k in K:
            kmeans_model = (KMeans(n_clusters=k).fit(X))
            sum_of_squared_distances.append(kmeans_model.inertia_)
            calculated_kmeans_models.append(kmeans_model)

        try:
            knee_func = KneeLocator(K, sum_of_squared_distances)

            # Sellecting fittest KMeans algorithm model
            final_kmeans_model = calculated_kmeans_models[knee_func.knee - 1]
        except (TypeError, ValueError):
            final_kmeans_model = calculated_kmeans_models[0]

        # Divide data into separate clusters
        for index, label in enumerate(final_kmeans_model.labels_):

            # Adds new array for each new label
            if label + 1 > len(clustered_data):
                clustered_data.append([])

            # Parse data into list
            clustered_data[label].append(X[index])

        # Calculates inertia for each cluster with K = 1
        for cluster in clustered_data:
            kmeans_model = (KMeans(n_clusters=1).fit(cluster))
            clusters_inertia_list.append(kmeans_model.inertia_)

        # Best data cluster has minimal inertia value
        index_of_fittest_cluster = clusters_inertia_list.index(min(clusters_inertia_list))

        # Extracts all cluster centers from array and convert to list
        center_locations = numpy.array(final_kmeans_model.cluster_centers_).tolist()

        return Location(round(center_locations[index_of_fittest_cluster][0], 4),
                        round(center_locations[index_of_fittest_cluster][1], 4))
