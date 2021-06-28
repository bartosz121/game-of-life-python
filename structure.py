class Structure:
    def __init__(self, start_pos, end_pos, name="Untitled"):
        self.name = name
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.n_cells = self._calculate_n_cells()
        self.n_cells_alive = None
        self.bounding_box = self._get_bounding_box()

    def __repr__(self):
        return f"Structure({self.start_pos}, {self.end_pos}, '{self.name}')"

    def __str__(self):
        return f"{'-' * (len(self.name)+10)}\n" \
               f"Name: {self.name}\n" \
               f"Position: {self.start_pos} => {self.end_pos}\n" \
               f"Bounding Box: {self.bounding_box}\n" \
               f"Cells:\n" \
               f"\tArea: {self.n_cells}\n" \
               f"\tAlive: {self.n_cells_alive}\n" \
               f"{'-' * (len(self.name)+10)}"

    def _calculate_side_length(self, side):
        if side == "x":
            return self.end_pos[0]-self.start_pos[0]
        elif side == "y":
            return self.end_pos[1]-self.start_pos[1]
        else:
            raise ValueError("Side not recognized. Must be 'x' or 'y'.")

    def _calculate_n_cells(self):
        x_side_length = self._calculate_side_length("x")
        y_side_length = self._calculate_side_length("y")
        return x_side_length*y_side_length

    def _get_bounding_box(self):
        return f"{self._calculate_side_length('x')}x{self._calculate_side_length('y')}"

    @classmethod
    def load_from_file(cls, path_to_file):
        pass

    def save_to_file(self):
        pass