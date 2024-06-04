import numpy as np

class Utils():
    def __init__(self):
        self.init = True

    def get_euclidean(self, array1, array2):
        euclidean_distance = np.sqrt(((array2[1] - array1[1]) ** 2) + ((array2[2] - array1[2]) ** 2))
        return euclidean_distance

    def pixel_per_metric(self):
        return 1.0
