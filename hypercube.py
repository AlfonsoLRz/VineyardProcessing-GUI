import app_params as ap
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
        self._name = self._hypercube.filename.split('/')[-1].split('.')[0]

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

    def _combine(self, binary_mask, classification_image):
        return cv2.bitwise_and(binary_mask, classification_image)

    def export_binary_file(self, path, threshold):
        # Write with OpenCV the binary file
        cv2.imwrite(path, self.calculate_ndvi(threshold=threshold, thresholding=True))

    def num_layers(self):
        return self._dimensions[2]

    def save_chunks(self, path, chunk_size, overlapping, classification_img, as_nparray=False):
        num_divs = (self._dimensions[0] // chunk_size, self._dimensions[1] // chunk_size)
        diff = (self._dimensions[0] - num_divs[0] * chunk_size, self._dimensions[1] - num_divs[1] * chunk_size)
        start_index = (diff[0] // 2, diff[1] // 2)
        jump = chunk_size - overlapping

        # Transform classification image to match the NDVI mask
        app_params = ap.ApplicationParameters()
        if classification_img is not None:
            classification_img = self._combine(classification_img, self.calculate_ndvi(thresholding=True,
                                                                                       threshold=app_params.get_threshold()))
            classification_img_id = self._to_id_image(classification_img)

        chunk_idx = 0
        x, y = 0, 0

        while x + chunk_size < self._dimensions[0]:
            y = 0

            while y + chunk_size < self._dimensions[1]:
                chunk = self._hypercube.read_subregion((int(x), int(x + chunk_size)), (int(y), int(y + chunk_size)))

                if as_nparray:
                    chunk = np.array(chunk)
                    np.save(path + 'chunk_{}'.format(chunk_idx), chunk)
                else:
                    envi.save_image(path + self._name + '_' + str(chunk_idx) + '.hdr', chunk, force=True)
                save_rgb(path + self._name + '_' + str(chunk_idx) + '.png', chunk, format='png')

                # Save classification image
                if classification_img is not None:
                    classification_img_chunk = classification_img[int(x):int(x + chunk_size),
                                                                  int(y):int(y + chunk_size), :]
                    classification_img_id_chunk = classification_img_id[int(x):int(x + chunk_size),
                                                                        int(y):int(y + chunk_size)]
                    cv2.imwrite(path + self._name + '_' + str(chunk_idx) + '_class.png', classification_img_chunk)
                    np.save(path + self._name + '_' + str(chunk_idx) + '_class.png', classification_img_id_chunk)

                y += jump
                chunk_idx += 1

            x += jump

    def save_whole_cube(self, path, classification_image):
        np.save(path + 'cube', self._hypercube)

        if classification_image is not None:
            # Transform classification image to match the NDVI mask
            app_params = ap.ApplicationParameters()
            classification_image = self._combine(classification_image, self.calculate_ndvi(thresholding=True,
                                                                                           threshold=app_params.
                                                                                           get_threshold()))

            cv2.imwrite(path + self._name + '_class.png', classification_image)

            classification_id_image = self._to_id_image(classification_image)
            np.save(path + self._name + '_class', classification_id_image)

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

    def _to_id_image(self, img):
        h = img.shape[0]
        w = img.shape[1]
        id_image = np.zeros(shape=(h, w))
        color_dict = { (0, 0, 0): 0 }

        for y in range(0, h):
            for x in range(0, w):
                color = (int(img[y, x, 0]), int(img[y, x, 1]), int(img[y, x, 2]))
                if color not in color_dict:
                    color_dict[color] = len(color_dict)

                id_image[y, x] = color_dict[color]

        return id_image

    def __to_uint_img(self, flt_img):
        uint_img = flt_img.astype('uint8')      # To 8 bits
        gray_img = cv2.cvtColor(uint_img, cv2.COLOR_GRAY2BGR)

        return gray_img