"""Business logic for task 6.

Lab work: LR4 - Files, classes, serializers, regular expressions and standard libraries.
Version: 1.0.0
Developer: Lozhachnik
Date: 2026-04-27
"""

from __future__ import annotations

from io import StringIO
from pathlib import Path

import pandas as pd

from app.task6.models import DatasetInfo, PercentileThresholds

def display(value: object) -> None:
    """Fallback display function for a console environment."""
    print(value)


class PandasDataset:
    """Base wrapper around a pandas DataFrame."""

    loaded_count = 0

    def __init__(self, dataset_info: DatasetInfo) -> None:
        """Store the dataset info object."""
        type(self).loaded_count += 1
        self.dataset_info = dataset_info
        self._dataframe: pd.DataFrame | None = None

    @property
    def dataframe(self) -> pd.DataFrame:
        """Return the loaded DataFrame."""
        if self._dataframe is None:
            raise ValueError("Dataset is not loaded yet.")
        return self._dataframe

    def load(self) -> pd.DataFrame:
        """Load the DataFrame from CSV."""
        self._dataframe = pd.read_csv(self.dataset_info.file_path)
        return self.dataframe

    def __len__(self) -> int:
        """Return the number of rows in the DataFrame."""
        return len(self.dataframe)


class NetflixStockDataset(PandasDataset):
    """Task 6 dataset service for the Netflix Stock CSV."""

    def load(self) -> pd.DataFrame:
        """Load the Netflix stock DataFrame and prepare the types."""
        frame = super().load().copy()
        frame["Date"] = pd.to_datetime(frame["Date"])
        for column in ["Open", "High", "Low", "Close", "Volume"]:
            frame[column] = pd.to_numeric(frame[column], errors="coerce")
        if "Adj Close" in frame.columns:
            frame["Adj Close"] = pd.to_numeric(frame["Adj Close"], errors="coerce")
        self._dataframe = frame.dropna(subset=["Close", "Volume"])
        return self.dataframe

    def task_a_series(self) -> pd.Series:
        """Build the required Series."""
        volume_series = self.dataframe["Volume"].copy()
        average_volume = float(volume_series.mean())
        volume_series.loc["average"] = average_volume
        return volume_series

    def dataframe_info_text(self) -> str:
        """Return detailed DataFrame info as plain text."""
        buffer = StringIO()
        self.dataframe.info(buf=buffer)
        return buffer.getvalue().strip()

    def thresholds(self) -> PercentileThresholds:
        """Return the 5th and 95th percentiles for Close."""
        low_value = float(self.dataframe["Close"].quantile(0.05))
        high_value = float(self.dataframe["Close"].quantile(0.95))
        return PercentileThresholds(low_value, high_value)

    def statistical_ratio(self) -> tuple[float, float, float, PercentileThresholds]:
        """Return average volumes and their ratio for task B."""
        thresholds = self.thresholds()
        high_group = self.dataframe.loc[self.dataframe["Close"] > thresholds.high_percentile, "Volume"]
        low_group = self.dataframe.loc[self.dataframe["Close"] < thresholds.low_percentile, "Volume"]
        high_mean = float(high_group.mean())
        low_mean = float(low_group.mean())
        ratio = round(high_mean / low_mean, 2)
        return high_mean, low_mean, ratio, thresholds

    def short_preview(self) -> pd.DataFrame:
        """Return a small preview for display."""
        return self.dataframe[["Date", "Close", "Volume"]].head(10)

    def describe_numeric(self) -> pd.DataFrame:
        """Return standard statistics for numeric columns."""
        return self.dataframe.describe().round(2)

    def null_counts(self) -> pd.Series:
        """Return null counts for every column."""
        return self.dataframe.isna().sum()

    def dtypes_series(self) -> pd.Series:
        """Return DataFrame column types."""
        return self.dataframe.dtypes.astype(str)

    @staticmethod
    def display_object(value: object, title: str) -> None:
        """Display an object with a short text title."""
        print(f"\n{title}:")
        display(value)
