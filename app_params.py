import singleton


class ApplicationParameters(metaclass=singleton.SingletonMeta):
    def __init__(self):
        self._threshold = .5

    def get_threshold(self):
        return self._threshold