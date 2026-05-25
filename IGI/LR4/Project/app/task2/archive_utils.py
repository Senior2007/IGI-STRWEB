"""Archiving helpers for task 2.

Lab work: LR4 - Files, classes, serializers, regular expressions and standard libraries.
Version: 1.0.0
Developer: Lozhachnik
Date: 2026-04-17
"""

from __future__ import annotations

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


class ResultArchiver:
    """Create an archive with the analysis result file."""

    def __init__(self, archive_path: Path) -> None:
        """Store the output archive path."""
        self.archive_path = archive_path

    def archive(self, source_file: Path) -> None:
        """Archive the source file with ZIP compression."""
        with ZipFile(self.archive_path, "w", compression=ZIP_DEFLATED) as archive:
            archive.write(source_file, arcname=source_file.name)

    def get_info(self) -> str:
        """Return basic information about the archived file."""
        with ZipFile(self.archive_path, "r") as archive:
            info = archive.infolist()[0]
            return (
                f"Archive name: {self.archive_path.name}\n"
                f"File in archive: {info.filename}\n"
                f"Compressed size: {info.compress_size} bytes\n"
                f"Original size: {info.file_size} bytes"
            )
