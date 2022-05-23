import cv2
import math
import numpy as np
from spectral import *

class Hypercube:
    def __init__(self, header_path):
        self._path = header_path
        self._hypercube = open_image(header_path).load()
        self._wavelength_labels = self._hypercube.bands.centers

    def band_to_cv_image(self, band):
        band = self._hypercube.read_band(band)
        uint_img = np.array(band).astype('uint8')
        grayImage = cv2.cvtColor(uint_img, cv2.COLOR_GRAY2BGR)

        return grayImage

    def calculate_NDVI(self):
        print(self._wavelength_labels[self.__search_nearest_layer(700)])

    def __search_nearest_layer(self, wl):
        begin, end, index = 0, len(self._wavelength_labels) - 1, 0

        while True:
            middle = math.floor((begin + end) / 2.0)

            if begin == end or self._wavelength_labels[middle] <= wl < self._wavelength_labels[middle + 1]:
                index = middle
                break
            elif wl < self._wavelength_labels[middle]:
                end = middle - 1
            else:
                begin = middle + 1

        if index == (len(self._wavelength_labels) - 1):
            return index
        else:
            if abs(wl - self._wavelength_labels[index]) < abs(wl - self._wavelength_labels[index + 1]):
                return index
            else:
                return index + 1
