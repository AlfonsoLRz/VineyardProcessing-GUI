import cv2
import math
import numpy as np
from spectral import *


class Hypercube:
    RED_WL = 670
    GREEN_WL = 540
    BLUE_WL = 480
    NIR_WL = 800

    def __init__(self, header_path):
        self._path = header_path
        self._hypercube = open_image(header_path).load()
        self._wavelength_labels = self._hypercube.bands.centers
        self._dimensions = self._hypercube.shape

    def band_to_cv_image(self, band):
        band_list = self._hypercube.read_band(band)
        flt_img = np.array(band_list)

        # Normalize image
        max, min = np.max(flt_img), np.min(flt_img)
        flt_img = (flt_img - min) / (max - min) * 255.0

        return self.__to_uint_img(flt_img)

    def calculate_ndvi(self, thresholding=True, threshold=.5):
        nir_band = np.array(self._hypercube.read_band(self.__search_nearest_layer(self.NIR_WL)))
        red_band = np.array(self._hypercube.read_band(self.__search_nearest_layer(self.RED_WL)))
        ndvi = (nir_band - red_band) / (nir_band + red_band)

        if thresholding:
            ndvi = np.where(ndvi > threshold, 255.0, .0)
        else:
            ndvi = ndvi

        return self.__to_uint_img(ndvi)

    def export_binary_file(self, path, threshold):
        # Write with OpenCV the binary file
        cv2.imwrite(path, self.calculate_ndvi(threshold=threshold, thresholding=True))

    def num_layers(self):
        return self._dimensions[2]

    def save_chunks(self, path, chunk_size, classification_img):
        num_divs = (self._dimensions[0] // chunk_size, self._dimensions[1] // chunk_size)
        diff = (self._dimensions[0] - num_divs[0] * chunk_size, self._dimensions[1] - num_divs[1] * chunk_size)
        start_index = (diff[0] // 2, diff[1] // 2.0)

        chunk_idx = 0
        for i in range(num_divs[0]):
            for j in range(num_divs[1]):
                chunk = self._hypercube.read_subregion(
                    (int(start_index[0] + i * chunk_size), int(start_index[0] + (i + 1) * chunk_size)),
                    (int(start_index[1] + j * chunk_size), int(start_index[1] + (j + 1) * chunk_size)))

                envi.save_image(path + 'chunk_' + str(chunk_idx) + '.hdr', chunk, force=True)
                save_rgb(path + 'chunk_' + str(chunk_idx) + '.png', chunk, format='png')

                # Save classification image
                if classification_img is not None:
                    classification_img_chunk = classification_img[int(start_index[0] + i * chunk_size):
                                                                  int(start_index[0] + (i + 1) * chunk_size),
                                                                  int(start_index[1] + j * chunk_size):
                                                                  int(start_index[1] + (j + 1) * chunk_size), :]
                    cv2.imwrite(path + 'chunk_' + str(chunk_idx) + '_classification.png', classification_img_chunk)

                chunk_idx += 1

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

    def __to_uint_img(self, flt_img):
        uint_img = flt_img.astype('uint8')      # To 8 bits
        gray_img = cv2.cvtColor(uint_img, cv2.COLOR_GRAY2BGR)

        return gray_img