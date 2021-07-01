import re
from itertools import groupby
from pathlib import Path
from structure import Structure


class StructureReader:
    @staticmethod
    def load_from_file(path_to_file):
        relative = Path(path_to_file)
        if not relative.exists():
            raise FileNotFoundError(
                f"File {str(relative.absolute())} not found.")

        # Check if file is .cells or .rle
        file_format = path_to_file.split('.')[-1]
        if not StructureReader._check_file_format(file_format):
            raise TypeError("File must be in .cells or .rle format")
        file_content = StructureReader._get_file_content(relative.absolute())

        if file_format == "cells":
            s = StructureReader._serialize_cells(file_content)
        else:
            s = StructureReader._serialize_rle(file_content)

        return Structure(s["name"], s["desc"], s["start_pos"], s["end_pos"],
                   s["cells"])

    @staticmethod
    def _get_file_content(abs_path):
        with open(abs_path, 'r') as f:
            content = f.read().splitlines()
        return content

    @staticmethod
    def _serialize_cells(content):
        result = {
            "name": "Untitled",
            "desc": "",
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
            bool_row = []
            for cell in row:
                bool_row.append(True if cell == "O" else False)
            result["cells"].append(bool_row)

        return result

    @staticmethod
    def _serialize_rle(content):
        """https://www.conwaylife.com/wiki/Run_Length_Encoded"""

        def add_cells(cell_type, n=1):
            if cell_type == 'b':
                # dead cell
                c = [False] * n
            elif cell_type == 'o':
                # alive cell
                c = [True] * n
            else:
                raise ValueError(f"cell type not recognized ({cell_type})")
            row.extend(c)

        result = {
            "name": "Untitled",
            "author": "Unknown",
            "desc": "",
            "cells": [],
            "start_pos": (0, 0)
        }
        # split content by header line
        grouped = [list(g) for k, g in groupby(content, lambda l: l[0] == 'x')]
        if len(grouped) > 2:
            # grouped[0] = hash_lines
            # grouped[1] = header line
            # grouped[2] = pattern
            header_line_index = 1
            pattern_index = 2
            for line in grouped[0]:
                if line[0] == '#':
                    letter = line[1].lower()
                    if letter == 'n':
                        result["name"] = line[2:].strip()
                    elif letter == 'c':
                        ".".join((result["desc"], line[2:].strip()))
                    elif letter == 'o':
                        result["author"] = line[2:].strip()
        else:
            # maybe there is no hash lines so grouped is < 2,
            # but its suspicious so be careful
            # grouped[0] = header line
            # grouped[1] = pattern
            header_line_index = 0
            pattern_index = 1

        header_line = grouped[header_line_index][0].split(',')
        result["end_pos"] = (
            int(header_line[0][header_line[0].rindex(' '):]),
            int(header_line[1][header_line[1].rindex(' '):])
        )
        pattern = "".join(grouped[pattern_index]).split('$')
        pattern[-1] = pattern[-1][:-1]  # delete '!' from the end

        for p in pattern:
            row = []
            n = ""
            for i in range(len(p)):
                char = p[i]
                if char in ('b', 'o'):
                    try:
                        if p[i - 1] in ('b', 'o'):
                            add_cells(char)
                        else:
                            add_cells(char, n=int(n))
                            n = ""
                    except ValueError:
                        add_cells(char)
                else:
                    # number
                    n += char
                    if i == len(p) - 1:
                        # if last char is number insert 'char'(n)-1 lines of empty rows
                        for j in range(
                                int(n) - 1):  # -1 bcs i already have one row done(the one above empty ones)
                            result["cells"].append(row)
                            row = []
                            add_cells('b', result["end_pos"][0])

            result["cells"].append(row)

        return result

    @staticmethod
    def _check_file_format(filename):
        if filename in ("cells", "rle"):
            return True
        return False
