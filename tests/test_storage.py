import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from campusflow.storage import load_tickets, save_tickets


class TestTicketStorage(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.filename = Path(self.temp_dir.name) / "tickets.json"
        self.patcher = patch(
            "campusflow.storage.FILENAME",
            self.filename,
        )
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()
        self.temp_dir.cleanup()

    def make_ticket(self):
        return {
            "id": "T001",
            "title": "Internet is down",
            "category": "Network",
            "urgency": "high",
            "affected_users": 12,
            "priority": "critical",
            "status": "open",
            "assigned_to": None,
        }

    def test_missing_file_returns_empty_list(self):
        self.assertFalse(self.filename.exists())

        result = load_tickets()

        self.assertEqual(result, [])

    def test_save_tickets_creates_json_file(self):
        tickets = [self.make_ticket()]

        save_tickets(tickets)

        self.assertTrue(self.filename.exists())

        with self.filename.open(encoding="utf-8") as file:
            saved_data = json.load(file)

        self.assertEqual(saved_data, tickets)

    def test_load_tickets_reads_saved_data(self):
        tickets = [self.make_ticket()]
        save_tickets(tickets)

        result = load_tickets()

        self.assertEqual(result, tickets)

    def test_save_and_load_multiple_tickets(self):
        tickets = [
            self.make_ticket(),
            {
                **self.make_ticket(),
                "id": "T002",
                "title": "Broken keyboard",
                "urgency": "low",
                "affected_users": 1,
                "priority": "low",
            },
        ]

        save_tickets(tickets)
        result = load_tickets()

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["id"], "T001")
        self.assertEqual(result[1]["id"], "T002")

    def test_malformed_json_raises_value_error(self):
        self.filename.write_text(
            '{"id": "T001", invalid json',
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ValueError, "Invalid JSON"):
            load_tickets()

    def test_malformed_json_is_not_overwritten_by_loading(self):
        original_content = '{"broken": json'

        self.filename.write_text(
            original_content,
            encoding="utf-8",
        )

        with self.assertRaises(ValueError):
            load_tickets()

        self.assertEqual(
            self.filename.read_text(encoding="utf-8"),
            original_content,
        )

    def test_non_list_json_is_rejected(self):
        self.filename.write_text(
            json.dumps({"id": "T001"}),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ValueError, "must contain a list"):
            load_tickets()

    def test_empty_list_is_saved_and_loaded(self):
        save_tickets([])

        self.assertEqual(load_tickets(), [])


if __name__ == "__main__":
    unittest.main()