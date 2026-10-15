import copy
import json
import tempfile
import unittest
from pathlib import Path

from campusflow.notes import add_note, next_note_id
from campusflow.storage import (
    load_tickets,
    reload_tickets,
    save_tickets,
    validate_ticket,
)
from campusflow.tickets import next_ticket_id
from campusflow.validation import ValidationError


def make_ticket(ticket_id="T001", **overrides):
    ticket = {
        "id": ticket_id,
        "title": "Wi-Fi is down",
        "category": "Network",
        "urgency": "high",
        "affected_users": 12,
        "priority": "critical",
        "status": "open",
        "assigned_to": None,
        "notes": [],
    }
    ticket.update(overrides)
    return ticket


class StorageTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.path = Path(self.temp_dir.name) / "tickets.json"

    def write_raw(self, content):
        self.path.write_text(content, encoding="utf-8")

    def write_json(self, data):
        self.write_raw(json.dumps(data))


class TestSaveAndReload(StorageTestCase):
    def test_notes_and_next_note_id_survive_save_and_load(self):
        tickets = [make_ticket()]
        add_note(tickets, "T001", "Mentor A", "Router reboot attempted")
        add_note(tickets, "T001", "Mentor B", "Investigating switches")

        save_tickets(tickets, self.path)
        reloaded = load_tickets(self.path)

        self.assertEqual(reloaded, tickets)
        self.assertEqual(next_note_id(reloaded[0]), "N003")

    def test_next_ticket_id_continues_after_reload(self):
        tickets = [make_ticket("T001"), make_ticket("T010")]
        save_tickets(tickets, self.path)

        reloaded = load_tickets(self.path)

        # numeric comparison: T010 is bigger than T002
        self.assertEqual(next_ticket_id(reloaded), "T011")

    def test_old_ticket_without_notes_key_still_loads(self):
        old_ticket = make_ticket()
        del old_ticket["notes"]
        self.write_json([old_ticket])

        self.assertEqual(load_tickets(self.path), [old_ticket])

    def test_missing_file_loads_as_empty_collection(self):
        self.assertEqual(load_tickets(self.path), [])

    def test_save_leaves_no_temporary_file_behind(self):
        save_tickets([make_ticket()], self.path)

        self.assertEqual([p.name for p in self.path.parent.iterdir()],
                         ["tickets.json"])


class TestRejectedLoadsKeepMemory(StorageTestCase):
    def assert_reload_rejected(self, memory):
        before = copy.deepcopy(memory)
        file_before = self.path.read_text(encoding="utf-8")

        with self.assertRaises(ValidationError):
            reload_tickets(memory, self.path)

        self.assertEqual(memory, before)
        self.assertEqual(self.path.read_text(encoding="utf-8"), file_before)

    def test_corrupt_json_rejected_and_memory_kept(self):
        memory = [make_ticket("T001")]
        self.write_raw('[{"id": "T001", broken')
        self.assert_reload_rejected(memory)

    def test_duplicate_ticket_ids_rejected_and_memory_kept(self):
        memory = [make_ticket("T001")]
        self.write_json([make_ticket("T002"), make_ticket("T002")])
        self.assert_reload_rejected(memory)

    def test_one_bad_record_rejects_the_whole_file(self):
        memory = [make_ticket("T001")]
        self.write_json([
            make_ticket("T002"),
            make_ticket("T003"),
            make_ticket("T004", status="weird"),
        ])
        self.assert_reload_rejected(memory)

    def test_successful_reload_replaces_memory_in_place(self):
        memory = [make_ticket("T001")]
        same_list = memory
        self.write_json([make_ticket("T005")])

        reload_tickets(memory, self.path)

        self.assertIs(memory, same_list)
        self.assertEqual([t["id"] for t in memory], ["T005"])


class TestInvalidRecordsAreRejected(StorageTestCase):
    def test_each_kind_of_bad_record_is_rejected(self):
        broken_notes = {"note_id": "N001", "author": "Ada", "message": "ok!!!"}
        cases = {
            "not a dict": "T001",
            "missing key": {k: v for k, v in make_ticket().items() if k != "title"},
            "bad ticket id": make_ticket("X1"),
            "blank title": make_ticket(title="  "),
            "bad category": make_ticket(category="network"),
            "bad urgency": make_ticket(urgency="urgent"),
            "bad status": make_ticket(status="closed"),
            "bool affected_users": make_ticket(affected_users=True),
            "float affected_users": make_ticket(affected_users=12.0),
            "wrong priority": make_ticket(priority="low"),
            "in_progress but unassigned": make_ticket(
                status="in_progress", assigned_to=None
            ),
            "blank assignee": make_ticket(assigned_to="  "),
            "notes not a list": make_ticket(notes="none"),
            "note with extra key": make_ticket(
                notes=[{**broken_notes, "extra": 1}]
            ),
            "note message too short": make_ticket(
                notes=[{**broken_notes, "message": "abc"}]
            ),
            "duplicate note ids": make_ticket(
                notes=[broken_notes, dict(broken_notes)]
            ),
        }
        for name, record in cases.items():
            with self.subTest(case=name):
                self.write_json([record])
                with self.assertRaises(ValidationError):
                    load_tickets(self.path)

    def test_non_list_top_level_is_rejected(self):
        self.write_json({"id": "T001"})
        with self.assertRaises(ValidationError):
            load_tickets(self.path)

    def test_valid_ticket_passes_validation(self):
        validate_ticket(make_ticket())


class TestSaveRefusesBadData(StorageTestCase):
    def test_saving_invalid_collection_leaves_existing_file_untouched(self):
        save_tickets([make_ticket("T001")], self.path)
        good_content = self.path.read_text(encoding="utf-8")

        with self.assertRaises(ValidationError):
            save_tickets([make_ticket("T001"), make_ticket("T001")], self.path)

        self.assertEqual(self.path.read_text(encoding="utf-8"), good_content)


if __name__ == "__main__":
    unittest.main()