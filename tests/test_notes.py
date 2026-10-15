import copy
import unittest

from campusflow.notes import add_note, get_notes, next_note_id
from campusflow.validation import ValidationError
from campusflow.workflow import assign_ticket, change_status, reopen_ticket


def make_ticket(ticket_id="T001", status="open", assigned_to=None):
    return {
        "id": ticket_id,
        "title": f"Test ticket {ticket_id}",
        "category": "Network",
        "urgency": "medium",
        "affected_users": 2,
        "priority": "medium",
        "status": status,
        "assigned_to": assigned_to,
        "notes": [],
    }


class TestAddNote(unittest.TestCase):
    def test_valid_note_on_open_ticket_gets_first_id(self):
        tickets = [make_ticket()]

        note = add_note(tickets, "T001", "Mentor A", "Router reboot attempted")

        self.assertEqual(note["note_id"], "N001")
        self.assertEqual(note["author"], "Mentor A")
        self.assertEqual(tickets[0]["notes"], [note])

    def test_second_note_gets_next_id(self):
        tickets = [make_ticket()]
        add_note(tickets, "T001", "Mentor A", "Router reboot attempted")

        note = add_note(tickets, "T001", "Mentor B", "Investigating switches")

        self.assertEqual(note["note_id"], "N002")

    def test_in_progress_ticket_accepts_notes(self):
        tickets = [make_ticket(status="in_progress", assigned_to="Ada")]

        note = add_note(tickets, "T001", "Ada", "Replacing the cable")

        self.assertEqual(note["note_id"], "N001")

    def test_author_and_message_are_trimmed(self):
        tickets = [make_ticket()]

        note = add_note(tickets, "T001", "  Ada ", "   Cable replaced   ")

        self.assertEqual(note["author"], "Ada")
        self.assertEqual(note["message"], "Cable replaced")

    def test_note_ids_are_per_ticket(self):
        tickets = [make_ticket("T001"), make_ticket("T002")]
        add_note(tickets, "T001", "Ada", "First note here")

        note = add_note(tickets, "T002", "Ada", "Other ticket note")

        self.assertEqual(note["note_id"], "N001")


class TestNoteRejections(unittest.TestCase):
    def assert_note_rejected_and_unchanged(self, tickets, *args):
        before = copy.deepcopy(tickets)
        with self.assertRaises(ValidationError):
            add_note(tickets, *args)
        self.assertEqual(tickets, before)

    def test_blank_author_rejected(self):
        for author in ("", "   "):
            with self.subTest(author=author):
                self.assert_note_rejected_and_unchanged(
                    [make_ticket()], "T001", author, "A valid message"
                )

    def test_message_shorter_than_five_characters_rejected(self):
        self.assert_note_rejected_and_unchanged(
            [make_ticket()], "T001", "Ada", "abcd"
        )

    def test_message_length_is_measured_after_trimming(self):
        self.assert_note_rejected_and_unchanged(
            [make_ticket()], "T001", "Ada", "   abcd   "
        )

    def test_message_length_boundaries(self):
        tickets = [make_ticket()]
        add_note(tickets, "T001", "Ada", "a" * 5)
        add_note(tickets, "T001", "Ada", "a" * 300)
        self.assertEqual(len(tickets[0]["notes"]), 2)

        self.assert_note_rejected_and_unchanged(tickets, "T001", "Ada", "a" * 301)

    def test_rejected_note_does_not_consume_an_id(self):
        tickets = [make_ticket()]
        with self.assertRaises(ValidationError):
            add_note(tickets, "T001", "Ada", "bad")

        note = add_note(tickets, "T001", "Ada", "Now a valid message")

        self.assertEqual(note["note_id"], "N001")

    def test_unknown_ticket_rejected(self):
        self.assert_note_rejected_and_unchanged(
            [make_ticket()], "T999", "Ada", "A valid message"
        )

    def test_resolved_ticket_rejects_note_and_stays_unchanged(self):
        tickets = [make_ticket(status="resolved", assigned_to="Ada")]
        self.assert_note_rejected_and_unchanged(
            tickets, "T001", "Ada", "A valid message"
        )


class TestNotesThroughWorkflow(unittest.TestCase):
    def test_resolve_reject_reopen_then_accept_matches_the_spec_example(self):
        tickets = [make_ticket()]
        assign_ticket(tickets, "T001", "Ada")
        add_note(tickets, "T001", "Mentor A", "Wi-Fi router reboot attempted")
        add_note(tickets, "T001", "Mentor B", "Investigating switch ports")
        change_status(tickets, "T001", "in_progress")
        change_status(tickets, "T001", "resolved")

        with self.assertRaises(ValidationError):
            add_note(tickets, "T001", "Mentor A", "Should be rejected")
        self.assertEqual(len(tickets[0]["notes"]), 2)

        reopen_ticket(tickets, "T001")
        note = add_note(tickets, "T001", "Mentor A", "Back to investigating")

        self.assertEqual(note["note_id"], "N003")
        self.assertEqual(len(tickets[0]["notes"]), 3)


class TestReadingNotes(unittest.TestCase):
    def test_get_notes_returns_notes_in_id_order(self):
        ticket = make_ticket()
        ticket["notes"] = [
            {"note_id": "N010", "author": "A", "message": "tenth note"},
            {"note_id": "N002", "author": "A", "message": "second note"},
        ]

        notes = get_notes([ticket], "T001")

        self.assertEqual([n["note_id"] for n in notes], ["N002", "N010"])

    def test_next_note_id_continues_after_the_highest_existing_id(self):
        ticket = make_ticket()
        ticket["notes"] = [
            {"note_id": "N001", "author": "A", "message": "first note"},
            {"note_id": "N003", "author": "A", "message": "third note"},
        ]

        self.assertEqual(next_note_id(ticket), "N004")

    def test_old_ticket_without_notes_key_still_works(self):
        ticket = make_ticket()
        del ticket["notes"]
        tickets = [ticket]

        self.assertEqual(get_notes(tickets, "T001"), [])
        note = add_note(tickets, "T001", "Ada", "First note ever")

        self.assertEqual(note["note_id"], "N001")


if __name__ == "__main__":
    unittest.main()