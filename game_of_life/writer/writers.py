from abc import ABC, abstractmethod
from pathlib import Path

from grid import Grid
from numpy import ndarray


class WriterError(Exception):
    """Raised when there is an error when writing to a file"""
    pass


class Writer(ABC):
    @abstractmethod
    def save(self, file_path: Path, data: Grid) -> bool:
        pass


class RleWriter(Writer):
    """
    Writes grid data in .rle file

    https://www.conwaylife.com/wiki/Run_Length_Encoded
    """
    def _serialize_to_rle(self, row: ndarray) -> str:
        row_iter = iter(row)
        current_c = next(row_iter)
        counter = 1
        result = ''

        while True:
            try:
                c = next(row_iter)
            except StopIteration:
                result += self._get_run_count_with_tag(current_c, counter)
                break

            if c == current_c:
                counter += 1
            else:
                result += self._get_run_count_with_tag(current_c, counter)
                current_c = c
                counter = 1


        return result


    def _get_run_count_with_tag(self, cell_state: bool, count: int) -> str:
        if cell_state:
            tag = 'o'
        else:
            tag = 'b'

        if count == 1:
            return tag
        return str(count) + tag

    def save(self, file_path: Path, data: Grid) -> bool:
        header = f"x = {data.x}, y = {data.y}, rule = B3/S23\n"
        line_char_count = 0
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(header)
            for i, row in enumerate(data):
                serialized = self._serialize_to_rle(row)

                if i != data.y - 1:
                    # Append '$' to all 'rows' except last one
                    serialized += '$'

                if line_char_count + len(serialized) > 70:
                    f.write('\n')
                    line_char_count = 0

                f.write(serialized)
                line_char_count += len(serialized)

            f.write('!')

        return True


class CellsWriter(Writer):
    """
    Writes grid data in .cells file

    https://www.conwaylife.com/wiki/Plaintext
    """

    def _serialize_row(self, row: ndarray) -> str:
        result = ''
        for c in row:
            if c:
                result += 'O'
            else:
                result += '.'

        return result

    def save(self, file_path: Path, data: Grid) -> bool:
        with open(file_path, "w", encoding="utf-8") as f:
            for row in data:
                to_save = self._serialize_row(row)
                to_save += '\n'
                f.write(to_save)

        return True


class WriterFactory:
    @staticmethod
    def get_writer(file_format: str) -> Writer:
        """
        Returns appropriate reader by file format
        """
        match file_format:
            case '.rle':
                return RleWriter()
            case '.cells':
                return CellsWriter()
            case _:
                raise WriterError(f"File format {file_format!r} not supported for writing")
