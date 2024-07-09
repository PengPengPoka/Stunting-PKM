import numpy as np

class Utils():
    def __init__(self):
        self.init = True

    def get_euclidean_dist(self, array1, array2):
        euclidean_distance = np.sqrt(((array2[1] - array1[1]) ** 2) + ((array2[2] - array1[2]) ** 2))
        return euclidean_distance

    def pixel_per_metric(self, cam_dist): # nonsense results
        ppm = ((0.0944*(cam_dist**2)) - (5.5989*cam_dist) + 105.16)
        return ppm
    
    def convert_to_cm(self, cam_dist):
        cm = ((0.0003*(cam_dist**2)) + (0.7504*cam_dist) + 0.2809)
        return cm
