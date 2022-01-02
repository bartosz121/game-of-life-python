from pathlib import Path
from typing import Callable, Sequence

from PyQt6.QtWidgets import QFileDialog, QWidget

from grid import Grid
from reader.readers import ReaderFactory
from writer.writers import WriterFactory


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

    def _get_file_path(self, fn: Callable, caption: str) -> Path:
        """
        Return user selected file path from QFileDialog

        Parameters:
            fn: static method from 'QFileDialog' used to get path to file
            caption: String used as caption in fn
        """
        path_str, _ = fn(
            parent=self.parent,
            caption=caption,
            directory=str(Path.cwd()),
            filter=self.allowed_file_extensions,
        )

        if not path_str:
            # could be empty when user closed file dialog without choosing a file
            path_str = "no_file"

        return Path(path_str)

    def _get_open_file_path(self) -> Path:
        caption = "Select a file"
        return self._get_file_path(QFileDialog.getOpenFileName, caption)

    def _get_save_file_path(self) -> Path:
        caption = "Save as file"
        return self._get_file_path(QFileDialog.getSaveFileName, caption)

    def load_file(self) -> Grid | None:
        path = self._get_open_file_path()
        if path.name == "no_file":
            return None

        format = path.suffix
        reader = ReaderFactory.get_reader(format)
        return reader.create_grid(path)

    def save_file(self, data: Grid) -> None:
        path = self._get_save_file_path()
        if path.name == "no_file":
            return None

        format = path.suffix
        writer = WriterFactory.get_writer(format)
        return writer.save(path, data)
