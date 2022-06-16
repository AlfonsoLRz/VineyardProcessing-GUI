import cv2
import hypercube
import singleton


class HSIDatabase(metaclass=singleton.SingletonMeta):
    def __init__(self):
        self._hsi_cube = None
        self._classification_img = None

    def get_classification_img(self):
        return self._classification_img

    def get_hsi_data(self):
        return self._hsi_cube

    def load_classification_img(self, path):
        self._classification_img = cv2.imread(path, cv2.IMREAD_COLOR)
        return self._classification_img is not None

    def load_hsi_data(self, path):
        self._hsi_cube = hypercube.Hypercube(path + '.hdr')
        return self._hsi_cube is not None

    def save_hsi_chunks(self, path, chunk_size, as_nparray=False):
        if self._hsi_cube is not None:
            self._hsi_cube.save_chunks(path, chunk_size, self._classification_img, as_nparray=as_nparray)

    def save_whole_hsi_cube(self, path):
        if self._hsi_cube is not None:
            self._hsi_cube.save_whole_cube(path, self._classification_img)

