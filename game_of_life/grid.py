from numpy import array, ndarray

from grid_object import GridObject


class Grid:
    def __init__(self, rows: int, columns: int) -> None:
        self._y = rows
        self._x = columns
        self.objects: ndarray[list[GridObject | bool | None]] = array(
            [*(None for _ in range(rows * columns))]
        ).reshape(rows, columns)

    def __repr__(self):
        return f"Grid({self.y}, {self.x})"

    def __iter__(self):
        return (row for row in self.objects)

    def __getitem__(self, n: int):
        return self.objects[n]

    def __setitem__(self, n: int, item: GridObject):
        self.objects[n] = item

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def shape(self):
        return self.objects.shape

    def _swap_x_y(self):
        self._x, self._y = self._y, self._x

    def obj_count(self):
        return len(self.objects.flatten())

    def transpose(self):
        self.objects = self.objects.transpose()
        self._swap_x_y()

    def anti_transpose(self):
        """
        Transpose but over the other diagonal
        """
        self.objects = self.objects = self.objects[::-1, ::-1].transpose()
        self._swap_x_y()
