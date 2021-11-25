from typing import NamedTuple


class Color(NamedTuple):
    r: int
    g: int
    b: int

    def hex(self) -> str:
        """Returns string Hex color code from RGB.

        Example:

        Color(0, 0, 0).hex() -> '#000000'

        Color(255, 255, 255).hex() -> '#ffffff'

        Color(255, 105, 180).hex() -> '#ff69b4'
        """
        return "#{:02x}{:02x}{:02x}".format(self.r, self.g, self.b)
