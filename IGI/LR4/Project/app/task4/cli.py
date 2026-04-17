"""Console interface for task 4.

Lab work: LR4 - Files, classes, serializers, regular expressions and standard libraries.
Version: 1.0.0
Developer: Lozhachnik
Date: 2026-04-17
"""

from __future__ import annotations

from pathlib import Path

from app.common.base import LabTask
from app.common.io_utils import InputHelper
from app.task4.models import RegularHexagon
from app.task4.renderers import SvgRenderer, TkRenderer


class Task4Runner(LabTask):
    """Interactive runner for task 4."""

    task_name = "Task 4 - Regular hexagon"

    def run(self, **kwargs: object) -> None:
        """Build, color, label and export a regular hexagon."""
        show_gui = bool(kwargs.get("show_gui", True))
        side = InputHelper.ask_float("Enter the side length a: ", minimum=0.01)
        color = InputHelper.ask_text("Enter the figure color: ")
        label = InputHelper.ask_text("Enter the figure label: ")

        figure = RegularHexagon(side=side, color=color, label=label)
        svg_path = Path("data/task4/regular_hexagon.svg")
        SvgRenderer().render(figure, svg_path)

        print("\nFigure information:")
        print(figure.describe())
        print(f"Number of vertices: {len(figure)}")
        print(f"SVG file: {svg_path}")

        if show_gui:
            message = TkRenderer().render(figure)
            print(message)
