import re
from pathlib import Path


class Structure:
    def __init__(self, name, desc, start_pos, end_pos, cells):
        self.name = name
        self.description = desc
        self._start_pos = start_pos
        self._end_pos = end_pos
        self.cells = cells
        self.n_cells = self._calculate_n_cells()
        self.n_cells_alive = None
        self.bounding_box = self._get_bounding_box()

    def __repr__(self):
        return f"Structure({self.start_pos}, {self.end_pos}, '{self.name}')"

    def __str__(self):
        return f"{'-' * (len(self.name)+10)}\n" \
               f"Name: {self.name}\n" \
               f"Desc: {self.description}\n" \
               f"Position: {self.start_pos} => {self.end_pos}\n" \
               f"Bounding Box: {self.bounding_box}\n" \
               f"Cells:\n" \
               f"\tArea: {self.n_cells}\n" \
               f"\tAlive: {self.n_cells_alive}\n" \
               f"{'-' * (len(self.name)+10)}"

    @property
    def start_pos(self):
        return self._start_pos

    @start_pos.setter
    def start_pos(self, value):
        self._start_pos = value
        self.end_pos = self.start_pos[0]+self.end_pos[0], self.start_pos[1]+self.end_pos[1]

    @property
    def end_pos(self):
        return self._end_pos

    @end_pos.setter
    def end_pos(self, value):
        self._end_pos = value

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
        relative = Path(path_to_file)
        if not relative.exists():
            raise FileNotFoundError(
                f"File {str(relative.absolute())} not found.")

        # Check if file is .cells or .rle
        file_format = path_to_file.split('.')[-1]
        if not Structure.check_file_format(file_format):
            raise TypeError("File must be in .cells or .rle format")
        file_content = Structure.get_file_content(relative.absolute())

        if file_format == "cells":
            s = Structure.serialize_cells(file_content)
        else:
            s = Structure.serialize_rle(file_content)

        return cls(s["name"], s["desc"], s["start_pos"], s["end_pos"], s["cells"])

    @staticmethod
    def get_file_content(abs_path):
        with open(abs_path, 'r') as f:
            content = f.read().splitlines()
        return content

    @staticmethod
    def serialize_cells(content):
        result = {
            "name": "Untitled",
            "desc": None,
            "cells": []
        }
        r = re.compile("^!")
        comments = list(filter(r.match, content))
        cells = list(filter(lambda v: v not in comments, content))
        if len(cells) < 1:
            raise ValueError("Error reading file. No data found.")

        if len(comments) > 0:
            # TODO delete '!' before name and desc
            result["name"] = comments[0]
            comments.pop(0)
            result["desc"] = "\n".join(comments)

        result["start_pos"] = (0, 0)
        result["end_pos"] = (len(cells[0]), len(cells))

        for i, row in enumerate(cells):
            print(i, row)
            bool_row = []
            for cell in row:
                bool_row.append(True if cell == "O" else False)
            result["cells"].append(bool_row)

        return result

    @staticmethod
    def serialize_rle(content):
        result = {}
        return result

    @staticmethod
    def check_file_format(filename):
        if filename in ("cells", "rle"):
            return True
        return False

    def save_to_file(self):
        pass
