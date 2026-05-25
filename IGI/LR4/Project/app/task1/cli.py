"""Console interface for task 1.

Lab work: LR4 - Files, classes, serializers, regular expressions and standard libraries.
Version: 1.0.0
Developer: Lozhachnik
Date: 2026-04-17
"""

from __future__ import annotations

from pathlib import Path

from app.common.base import LabTask
from app.common.io_utils import InputHelper
from app.task1.repository import CsvStudentStorage, PickleStudentStorage, StudentStorage
from app.task1.service import GTORegistry


class Task1Runner(LabTask):
    """Interactive runner for task 1."""

    task_name = "Task 1 - GTO standards"

    def __init__(self) -> None:
        """Prepare the storage map."""
        super().__init__()
        self._storages: dict[str, StudentStorage] = {
            "csv": CsvStudentStorage(),
            "pickle": PickleStudentStorage(),
        }

    def _choose_storage(self) -> StudentStorage:
        """Ask the user which serializer should be used."""
        choice = InputHelper.ask_choice("Choose serializer (csv/pickle): ", {"csv", "pickle"})
        return self._storages[choice]

    def _save_all_formats(self, registry: GTORegistry) -> dict[str, Path]:
        """Save the source dictionary in both required formats."""
        output_dir = InputHelper.ensure_directory(Path("data/task1"))
        saved_files: dict[str, Path] = {}
        for storage_name, storage in self._storages.items():
            file_path = output_dir / f"gto_students{storage.extension}"
            storage.save(file_path, registry.students)
            saved_files[storage_name] = file_path
        return saved_files

    def run(self, **kwargs: object) -> None:
        """Serialize, load and analyze GTO student records."""
        registry = GTORegistry.from_seed_data()
        saved_files = self._save_all_formats(registry)
        storage = self._choose_storage()
        file_path = saved_files["csv" if isinstance(storage, CsvStudentStorage) else "pickle"]
        loaded_students = storage.load(file_path)
        loaded_registry = GTORegistry(loaded_students)

        print("\nGTO norms:")
        print(f"100 m sprint: up to {loaded_students[next(iter(loaded_students))].sprint_norm_seconds:.1f} seconds")
        print(f"Long jump: from {loaded_students[next(iter(loaded_students))].long_jump_norm_cm} cm")

        print("\nStudents who did not pass at least one norm:")
        failed_students = loaded_registry.failed_students()
        if failed_students:
            for student in failed_students:
                print(f"- {student}")
        else:
            print("All students passed the norms.")

        print(f"\nNumber of students who passed both norms: {loaded_registry.passed_count()}")

        print("\nTop 3 students:")
        for index, student in enumerate(loaded_registry.top_three(), start=1):
            print(f"{index}. {student} | rating score = {student.rating_score}")

        student_name = InputHelper.ask_text("\nEnter the full name of a student: ")
        student = loaded_registry.find_student(student_name)
        if student is None:
            print("Student not found.")
        else:
            print(f"Student information: {student}")

        print("\nCreated files:")
        for storage_name, saved_path in saved_files.items():
            print(f"- {storage_name}: {saved_path}")
        print(f"Loaded data from: {file_path}")
