"""Geometry models for task 4.

Lab work: LR4 - Files, classes, serializers, regular expressions and standard libraries.
Version: 1.0.0
Developer: Lozhachnik
Date: 2026-04-26
"""

from __future__ import annotations

import math
from abc import ABC, abstractmethod
from PIL import ImageColor

from app.common.mixins import PositiveValueMixin, PrettyReprMixin


class FigureColor:
    """Store and validate the figure color."""

    def __init__(self, name: str) -> None:
        """Store the color name."""
        self._name = ""
        self.name = name

    @property
    def name(self) -> str:
        """Return the color name."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Validate and set the color name."""
        clean_value = value.strip()
        if not clean_value:
            raise ValueError("Color name cannot be empty.")
        try:
            ImageColor.getrgb(clean_value)
        except ValueError as error:
            raise ValueError("Unsupported color name. Use a standard color like red, blue or green.") from error
        self._name = clean_value


class GeometricFigure(ABC, PrettyReprMixin):
    """Abstract geometric figure."""

    figure_name = "Geometric figure"
    created_count = 0

    def __init__(self, color: str, label: str) -> None:
        """Store common figure data."""
        type(self).created_count += 1
        self.color = FigureColor(color)
        self._label = ""
        self.label = label

    @property
    def label(self) -> str:
        """Return the figure label."""
        return self._label

    @label.setter
    def label(self, value: str) -> None:
        """Validate and set the figure label."""
        clean_value = value.strip()
        if not clean_value:
            raise ValueError("Label cannot be empty.")
        self._label = clean_value

    @classmethod
    def get_figure_name(cls) -> str:
        """Return the class-level figure name."""
        return cls.figure_name

    @abstractmethod
    def area(self) -> float:
        """Return the figure area."""

    @abstractmethod
    def vertices(self) -> list[tuple[float, float]]:
        """Return the figure vertices."""


class PolygonFigure(GeometricFigure, PositiveValueMixin):
    """Base polygon class with a side length."""

    def __init__(self, side: float, color: str, label: str) -> None:
        """Store the common polygon data."""
        super().__init__(color, label)
        self._side = 0.0
        self.side = side

    @property
    def side(self) -> float:
        """Return the polygon side length."""
        return self._side

    @side.setter
    def side(self, value: float) -> None:
        """Validate and set the side length."""
        self._side = self.validate_positive(float(value), "Side")


class RegularHexagon(PolygonFigure):
    """Regular hexagon for the seventh variant."""

    figure_name = "Regular hexagon"

    def area(self) -> float:
        """Compute the regular hexagon area."""
        return (3 * math.sqrt(3) * (self.side ** 2)) / 2

    def vertices(self) -> list[tuple[float, float]]:
        """Return six vertices of the hexagon around the center."""
        radius = self.side
        points = []
        for index in range(6):
            angle = math.radians(60 * index - 30)
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            points.append((x, y))
        return points

    def describe(self) -> str:
        """Return the main parameters in a formatted string."""
        return "{0} with side {1:.2f}, color {2}, label '{3}', area {4:.2f}".format(
            self.get_figure_name(),
            self.side,
            self.color.name,
            self.label,
            self.area(),
        )

    def __len__(self) -> int:
        """Return the number of polygon vertices."""
        return 6

    def __str__(self) -> str:
        """Return the readable description of the hexagon."""
        return self.describe()
