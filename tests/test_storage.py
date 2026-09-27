"""Unit tests for gurdung.storage."""

import json
import tempfile
import unittest
from pathlib import Path

from gurdung.storage import Storage


class StorageTestCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.data_file = Path(self.tmp.name) / "data.json"
        self.storage = Storage(self.data_file)

    def tearDown(self):
        self.tmp.cleanup()

    def test_add_and_list_notes(self):
        self.storage.add_note("first idea")
        self.storage.add_note("second idea")
        notes = self.storage.list_notes()
        self.assertEqual(len(notes), 2)
        self.assertEqual(notes[0]["text"], "first idea")
        self.assertEqual(notes[1]["id"], 2)

    def test_remove_note(self):
        self.storage.add_note("keep me")
        self.storage.add_note("drop me")
        self.assertTrue(self.storage.remove_note(2))
        notes = self.storage.list_notes()
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0]["text"], "keep me")
        self.assertFalse(self.storage.remove_note(99))

    def test_todo_lifecycle(self):
        self.storage.add_todo("write report")
        self.storage.add_todo("book doctor")
        todos = self.storage.list_todos()
        self.assertEqual(len(todos), 2)
        self.assertFalse(todos[0]["done"])

        self.assertTrue(self.storage.mark_done(1))
        todos = self.storage.list_todos()
        self.assertTrue(todos[0]["done"])
        self.assertFalse(todos[1]["done"])

        self.assertTrue(self.storage.remove_todo(2))
        self.assertEqual(len(self.storage.list_todos()), 1)

    def test_clear_todos(self):
        self.storage.add_todo("a")
        self.storage.add_todo("b")
        self.assertEqual(self.storage.clear_todos(), 2)
        self.assertEqual(self.storage.list_todos(), [])

    def test_stats(self):
        self.storage.add_note("n1")
        self.storage.add_todo("t1")
        self.storage.add_todo("t2")
        self.storage.mark_done(1)
        stats = self.storage.stats()
        self.assertEqual(stats["notes"], 1)
        self.assertEqual(stats["todos_total"], 2)
        self.assertEqual(stats["todos_done"], 1)

    def test_persistence_across_instances(self):
        self.storage.add_note("persisted")
        other = Storage(self.data_file)
        self.assertEqual(len(other.list_notes()), 1)
        self.assertEqual(other.list_notes()[0]["text"], "persisted")

    def test_file_is_valid_json(self):
        self.storage.add_todo("x")
        with open(self.data_file, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        self.assertIn("notes", data)
        self.assertIn("todos", data)


if __name__ == "__main__":
    unittest.main()
