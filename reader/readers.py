import re
import itertools
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from grid import Grid


# TODO figure out type hints


class ReaderError(Exception):
    """Raised when there is an error when reading a file"""

    pass


class Reader(ABC):
    file_extension: str

    @abstractmethod
    def create_grid(self, file_path: Path) -> Any:
        pass

    def _get_file_content(self, file_path: Path) -> list[str]:
        with open(file_path, "r", encoding="utf-8") as file:
            content = [line.strip() for line in file]
        return content


class RleReader(Reader):
    """
    Reads cells from '.rle' file and creates 'Grid' object

    https://www.conwaylife.com/wiki/Run_Length_Encoded
    """

    file_extension = ".rle"

    def _create_grid_info(self, header: str) -> dict[str, str]:
        """
        The first line is a header line, which has the form

        x = m, y = n
        """
        info = dict()
        header = header.split(",")
        for d in header:
            d = d.strip()
            k, v = d.split(" = ")
            info[k] = v

        return info

    def _format_to_grid(self, data: list[str]) -> Grid:
        data = [line for line in data if not line[0].startswith(("#"))]

        grid_info = self._create_grid_info(data.pop(0))

        try:
            grid_x = int(grid_info["x"])
            grid_y = int(grid_info["y"])
        except KeyError:
            raise ReaderError(f"Could not read data from {self.file_extension!r} file")

        grid = Grid(grid_y, grid_x)

        # TODO what if this is really big???
        lines = "".join(data).split("$")

        RE = re.compile(r"[o|b]")

        # if line ends with a number then it means next 'number' - 1 rows are empty dead cells (f.e. 'o6bo2$')
        RE_EMPTY_LINE = re.compile(r"\d+$")

        # Travese through line char by char
        y_count = 0
        for line in lines:
            matches = re.finditer(RE, line)
            matches_empty = re.findall(RE_EMPTY_LINE, line)
            last_index = 0
            last_num = 0
            for m in matches:
                s = m.start()

                # could be empty string (see wiki)
                try:
                    num = int(line[last_index:s])
                except ValueError:
                    num = 1

                match m.group():
                    case 'o':
                        state = True
                    case 'b':
                        state = False
                    case _:
                        raise ValueError("_format_to_grid unknown tag {_!r}")

                for x in range(last_num, last_num + num):
                    grid[y_count][x] = state

                last_num += num
                last_index = s + 1

            # 'Dead cells at the end of a pattern line do not need to be encoded'
            grid[y_count] = [state if state is not None else False for state in grid[y_count]]


            if matches_empty:
                # there can be only one match
                n_empty_lines = int(matches_empty.pop()) - 1
                for _ in range(n_empty_lines):
                    y_count += 1
                    grid[y_count] = [False] * grid_x

            y_count += 1

        return grid

    def create_grid(self, file_path: Path) -> Grid:
        data = self._get_file_content(file_path)
        grid = self._format_to_grid(data)

        return grid


class CellsReader(Reader):
    """
    Reads cells from '.cells' file and creates 'Grid' object

    https://www.conwaylife.com/wiki/Plaintext
    """

    file_extension = ".cells"

    def _format_to_grid(self, data: list[str]) -> Grid:
        data = [line for line in data if line[0].startswith((".", "O"))]

        try:
            grid_shape = (len(data), len(data[0]))
        except IndexError:
            raise ReaderError(f"Could not read data from {self.file_extension!r} file")

        grid = Grid(*grid_shape)

        for y, line in enumerate(data):
            for x, value in enumerate(line):
                cell_state = True if value == "O" else False
                grid[y][x] = cell_state

            # 'Dead cells at the end of a pattern line do not need to be encoded'
            grid[y] = [state if state is not None else False for state in grid[y]]

        return grid

    def create_grid(self, file_path: Path) -> Grid:
        data = self._get_file_content(file_path)
        grid = self._format_to_grid(data)

        return grid


class ReaderFactory:
    # TODO can be a normal function in global scope
    @staticmethod
    def get_reader(file_format: str) -> Reader:
        """
        Returns appropriate reader by file format
        """
        match file_format:
            case '.rle':
                return RleReader()
            case '.cells':
                return CellsReader()
            case _:
                raise ReaderError(f"File format {file_format!r} not supported")