# Ballard Locks context manager exercise


class Locke(object):
    """
    Creates Locke objects
    """

    def __init__(self, size):
        self.size = size

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass
