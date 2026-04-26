"""Console interface for task 4.

Lab work: LR4 - Files, classes, serializers, regular expressions and standard libraries.
Version: 1.0.0
Developer: Lozhachnik
Date: 2026-04-26
"""

from __future__ import annotations

from pathlib import Path

from app.common.base import LabTask
from app.common.io_utils import InputHelper
from app.task4.models import RegularHexagon
from app.task4.renderers import PngRenderer, TkRenderer


class Task4Runner(LabTask):
    """Interactive runner for task 4."""

    task_name = "Task 4 - Regular hexagon"

    def run(self, **kwargs: object) -> None:
        """Build, color, label and export a regular hexagon."""
        show_gui = bool(kwargs.get("show_gui", True))
        side = InputHelper.ask_float("Enter the side length a: ", minimum=0.01)
        label = InputHelper.ask_text("Enter the figure label: ")
        while True:
            color = InputHelper.ask_text("Enter the figure color: ")
            try:
                figure = RegularHexagon(side=side, color=color, label=label)
                break
            except ValueError as error:
                print(error)

        image_path = Path("data/task4/regular_hexagon.png")
        image_path.parent.mkdir(parents=True, exist_ok=True)
        PngRenderer().render(figure, image_path)

        print("\nFigure information:")
        print(figure.describe())
        print(f"Number of vertices: {len(figure)}")
        print(f"Image file: {image_path}")

        if show_gui:
            message = TkRenderer().render(figure, image_path)
            print(message)
