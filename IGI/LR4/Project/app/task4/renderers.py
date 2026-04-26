"""Renderers for task 4.

Lab work: LR4 - Files, classes, serializers, regular expressions and standard libraries.
Version: 1.0.0
Developer: Lozhachnik
Date: 2026-04-26
"""

from __future__ import annotations

import subprocess
import sys
from abc import ABC, abstractmethod
from pathlib import Path

from PIL import Image, ImageColor, ImageDraw, ImageFont

from app.task4.models import RegularHexagon


class FigureRenderer(ABC):
    """Abstract renderer for a geometric figure."""

    @abstractmethod
    def render(self, figure: RegularHexagon, output_path: Path | None = None) -> str:
        """Render the figure and return a status message."""


class PngRenderer(FigureRenderer):
    """PNG renderer based on Pillow."""

    image_width = 900
    image_height = 700
    padding = 90
    base_pixels_per_unit = 60.0
    font_candidates = (
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial.ttf",
    )

    @classmethod
    def _load_font(cls, font_size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
        """Load the first available readable font."""
        for font_path in cls.font_candidates:
            try:
                return ImageFont.truetype(font_path, font_size)
            except OSError:
                continue
        return ImageFont.load_default()

    @staticmethod
    def _fit_font(
        draw: ImageDraw.ImageDraw,
        label: str,
        max_width: float,
        max_height: float,
    ) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
        """Choose the largest available font that fits into the center area."""
        for font_size in range(120, 13, -2):
            font = PngRenderer._load_font(font_size)
            bbox = draw.textbbox((0, 0), label, font=font, anchor="lt")
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            if text_width <= max_width and text_height <= max_height:
                return font
        return PngRenderer._load_font(14)

    @staticmethod
    def _text_color(fill_color: str) -> str:
        """Choose a readable text color for the selected fill color."""
        red, green, blue = ImageColor.getrgb(fill_color)
        luminance = 0.299 * red + 0.587 * green + 0.114 * blue
        return "black" if luminance > 160 else "white"

    def render(self, figure: RegularHexagon, output_path: Path | None = None) -> str:
        """Render a centered regular hexagon into a PNG file."""
        if output_path is None:
            raise ValueError("PNG renderer requires an output path.")

        output_path.parent.mkdir(parents=True, exist_ok=True)
        image = Image.new("RGB", (self.image_width, self.image_height), "white")
        draw = ImageDraw.Draw(image)

        max_radius = min(
            (self.image_width - 2 * self.padding) / 2,
            (self.image_height - 2 * self.padding) / 2,
        )
        radius = min(figure.side * self.base_pixels_per_unit, max_radius)
        center = (self.image_width / 2, self.image_height / 2)

        draw.regular_polygon(
            bounding_circle=(center[0], center[1], radius),
            n_sides=6,
            rotation=30,
            fill=figure.color.name,
            outline="black",
            width=4,
        )

        font = self._fit_font(draw, figure.label, max_width=radius * 1.45, max_height=radius * 0.62)
        draw.text(
            center,
            figure.label,
            fill=self._text_color(figure.color.name),
            font=font,
            anchor="mm",
            align="center",
        )

        image.save(output_path)
        return f"Figure saved to {output_path}"


class TkRenderer(FigureRenderer):
    """Renderer that shows the already generated image in a Tk window."""

    def render(self, figure: RegularHexagon, output_path: Path | None = None) -> str:
        """Display the generated PNG file in a separate safe process."""
        if output_path is None:
            raise ValueError("Tk renderer requires a ready image path.")

        child_code = f"""
import tkinter as tk

root = tk.Tk()
root.title({figure.get_figure_name()!r})
image = tk.PhotoImage(file={str(output_path)!r})
label = tk.Label(root, image=image, bg='white')
label.pack(fill='both', expand=True)
root.configure(bg='white')
root.mainloop()
"""
        try:
            completed = subprocess.run(
                [sys.executable, "-c", child_code],
                capture_output=True,
                text=True,
                check=False,
            )
        except Exception:
            return "The image file was created, but the screen display is unavailable in this environment."

        if completed.returncode != 0:
            return "The image file was created, but the screen display is unavailable in this environment."
        return "Figure displayed on the screen."
