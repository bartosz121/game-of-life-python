from typing import NamedTuple


class Color(NamedTuple):
    r: int
    g: int
    b: int

    @property
    def rgb(self) -> tuple[int, int, int]:
        return self.r, self.g, self.b
