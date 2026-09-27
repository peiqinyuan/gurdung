
Enter file contents here
"""Data storage layer for gurdung.

Data is persisted as JSON at ``~/.gurdung/data.json`` so no external
service or database is required.
"""

import json
import os
from datetime import datetime
from pathlib import Path

DATA_DIR = Path.home() / ".gurdung"
DATA_FILE = DATA_DIR / "data.json"


class Storage:
    """Loads and saves notes and todos as JSON."""

    def __init__(self, data_file: Path = DATA_FILE):
        self.data_file = Path(data_file)

    def _ensure_file(self) -> None:
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.data_file.exists():
            self._write({"notes": [], "todos": []})

    def _read(self) -> dict:
        self._ensure_file()
        try:
            with open(self.data_file, "r", encoding="utf-8") as fh:
                data = json.load(fh)
        except (json.JSONDecodeError, OSError):
            data = {}
        data.setdefault("notes", [])
        data.setdefault("todos", [])
        return data

    def _write(self, data: dict) -> None:
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.data_file.with_suffix(".json.tmp")
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
        os.replace(tmp, self.data_file)

    # ---- notes ----

    def add_note(self, text: str) -> dict:
        data = self._read()
        note = {
            "id": self._next_id(data["notes"]),
            "text": text.strip(),
            "created_at": self._now(),
        }
        data["notes"].append(note)
        self._write(data)
        return note

    def list_notes(self) -> list:
        return self._read()["notes"]

    def remove_note(self, note_id: int) -> bool:
        data = self._read()
        before = len(data["notes"])
        data["notes"] = [n for n in data["notes"] if n["id"] != note_id]
        if len(data["notes"]) == before:
            return False
        self._write(data)
        return True

    # ---- todos ----

    def add_todo(self, text: str) -> dict:
        data = self._read()
        todo = {
            "id": self._next_id(data["todos"]),
            "text": text.strip(),
            "done": False,
            "created_at": self._now(),
        }
        data["todos"].append(todo)
        self._write(data)
        return todo

    def list_todos(self) -> list:
        return self._read()["todos"]

    def mark_done(self, todo_id: int, done: bool = True) -> bool:
        data = self._read()
        for todo in data["todos"]:
            if todo["id"] == todo_id:
                todo["done"] = done
                self._write(data)
                return True
        return False

    def remove_todo(self, todo_id: int) -> bool:
        data = self._read()
        before = len(data["todos"])
        data["todos"] = [t for t in data["todos"] if t["id"] != todo_id]
        if len(data["todos"]) == before:
            return False
        self._write(data)
        return True

    def clear_todos(self) -> int:
        data = self._read()
        count = len(data["todos"])
        data["todos"] = []
        self._write(data)
        return count

    # ---- helpers ----

    def stats(self) -> dict:
        data = self._read()
        todos = data["todos"]
        return {
            "notes": len(data["notes"]),
            "todos_total": len(todos),
            "todos_done": sum(1 for t in todos if t["done"]),
        }

    @staticmethod
    def _next_id(items: list) -> int:
        return max((item["id"] for item in items), default=0) + 1

    @staticmethod
    def _now() -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
