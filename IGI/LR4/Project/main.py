"""
Lab work 4 - Files, classes, serializers, regular expressions and standard libraries.
Version: 1.0
Developer: Ivan Lozhachnik
Date: 2026-04-17
"""

from __future__ import annotations

import argparse

from app.common.io_utils import InputHelper
from app.task1.cli import Task1Runner
from app.task2.cli import Task2Runner
from app.task3.cli import Task3Runner
from app.task4.cli import Task4Runner
from app.task5.cli import Task5Runner


def build_tasks() -> dict[str, object]:
    """Create and return the task map."""
    return {
        "1": Task1Runner(),
        "2": Task2Runner(),
        "3": Task3Runner(),
        "4": Task4Runner(),
        "5": Task5Runner(),
    }


def show_menu() -> None:
    """Print the main menu."""
    print("\nLaboratory work 4 menu")
    print("1. Task 1 - GTO standards")
    print("2. Task 2 - Text analysis and archiving")
    print("3. Task 3 - Series and graph")
    print("4. Task 4 - Regular hexagon")
    print("5. Task 5 - NumPy matrix")
    print("0. Exit")


def run_once(choice: str, show_gui: bool = True) -> None:
    """Run one task selected by menu key."""
    tasks = build_tasks()
    task = tasks.get(choice)
    if task is None:
        print("Unknown task number.")
        return
    if choice == "4":
        task.run(show_gui=show_gui)
    else:
        task.run()


def interactive_loop() -> None:
    """Run the menu loop until the user exits the program."""
    while True:
        show_menu()
        choice = InputHelper.ask_choice("Choose a task number: ", {"0", "1", "2", "3", "4", "5"})
        if choice == "0":
            print("Program finished.")
            break
        run_once(choice)
        input("\nPress Enter to return to the menu...")


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Laboratory work 4 launcher")
    parser.add_argument("--task", choices=["1", "2", "3", "4", "5"], help="Run one task without the menu")
    parser.add_argument("--no-gui", action="store_true", help="Do not open the Tk window for task 4")
    return parser.parse_args()


def main() -> None:
    """Start the program in interactive or single-task mode."""
    args = parse_args()
    if args.task:
        run_once(args.task, show_gui=not args.no_gui)
    else:
        interactive_loop()


if __name__ == "__main__":
    main()
