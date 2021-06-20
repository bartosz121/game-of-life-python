class Color:
    def __init__(self, r, g ,b):
        self._r = r
        self._g = g
        self._b = b
        self.RGB = (self._r, self._g, self._b)

    def __repr__(self):
        return f"{self.RGB}"
