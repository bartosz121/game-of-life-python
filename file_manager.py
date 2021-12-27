from pathlib import Path
from typing import Sequence
from PyQt6.QtWidgets import QFileDialog, QWidget

from reader.readers import ReaderFactory
from grid import Grid


class FileManager:
    def __init__(self, parent, allowed_file_extensions: Sequence[str]) -> None:
        self.parent: QWidget = parent
        self.allowed_file_extensions: str = self._create_file_filter(
            allowed_file_extensions
        )

    def _create_file_filter(self, extensions: Sequence[str]) -> str:
        s = "Game of Life file"
        ext_str = "(" + " ".join(extensions) + ")"

        return f"{s} {ext_str}"

    def _get_file_path(self) -> Path:
        path_str, _ = QFileDialog.getOpenFileName(
            parent=self.parent,
            caption="Select a file",
            directory=str(Path.cwd()),
            filter=self.allowed_file_extensions,
        )

        if not path_str:
            # could be empty when user closed file dialog without choosing a file
            path_str = "no_file"

        return Path(path_str)

    def load_file(self) -> Grid | None:
        path = self._get_file_path()
        if path.name == "no_file":
            return None

        format = path.suffix
        reader = ReaderFactory.get_reader(format)
        return reader.create_grid(path)
