import copy
import unittest

from campusflow.cli_views import add_note_view, search_view, view_notes_view


def make_ticket(ticket_id, title="Wi-Fi down", status="open"):
    return {
        "id": ticket_id,
        "title": title,
        "category": "Network",
        "urgency": "low",
        "affected_users": 1,
        "priority": "low",
        "status": status,
        "assigned_to": "Ada" if status != "open" else None,
        "notes": [],
    }


def scripted(*answers):
    """Return an input() replacement that feeds the given answers in order."""
    feed = iter(answers)
    return lambda prompt="": next(feed)


class TestNoteViews(unittest.TestCase):
    def test_add_note_view_adds_the_note_and_reports_success(self):
        tickets = [make_ticket("T001")]
        output = []

        added = add_note_view(
            tickets,
            input_fn=scripted("t001", "Mentor A", "Router reboot attempted"),
            output_fn=output.append,
        )

        self.assertTrue(added)
        self.assertEqual(tickets[0]["notes"][0]["note_id"], "N001")
        self.assertIn("N001", output[0])

    def test_rejected_note_shows_message_and_changes_nothing(self):
        tickets = [make_ticket("T001", status="resolved")]
        before = copy.deepcopy(tickets)
        output = []

        added = add_note_view(
            tickets,
            input_fn=scripted("T001", "Mentor A", "Should be rejected"),
            output_fn=output.append,
        )

        self.assertFalse(added)
        self.assertEqual(tickets, before)
        self.assertTrue(output[0].startswith("Could not add note"))

    def test_view_notes_shows_notes_in_id_order(self):
        tickets = [make_ticket("T001")]
        tickets[0]["notes"] = [
            {"note_id": "N002", "author": "B", "message": "second note"},
            {"note_id": "N001", "author": "A", "message": "first note"},
        ]
        output = []

        view_notes_view(tickets, input_fn=scripted("T001"), output_fn=output.append)

        self.assertEqual(
            output, ["N001 | A: first note", "N002 | B: second note"]
        )

    def test_view_notes_for_unknown_ticket_is_friendly(self):
        output = []

        view_notes_view([], input_fn=scripted("T999"), output_fn=output.append)

        self.assertTrue(output[0].startswith("Could not read notes"))


class TestSearchView(unittest.TestCase):
    def test_search_view_filters_and_does_not_change_tickets(self):
        tickets = [
            make_ticket("T001", "Wi-Fi down"),
            make_ticket("T002", "Laptop screen", status="in_progress"),
        ]
        before = copy.deepcopy(tickets)
        output = []

        # title, category, status, priority, sort?
        search_view(
            tickets,
            input_fn=scripted("WI-FI", "network", "", "", "n"),
            output_fn=output.append,
        )

        self.assertEqual(len(output), 1)
        self.assertTrue(output[0].startswith("T001"))
        self.assertEqual(tickets, before)


if __name__ == "__main__":
    unittest.main()
