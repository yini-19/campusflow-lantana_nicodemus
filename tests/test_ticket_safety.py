import copy
import unittest

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


class TestRejectedActionsChangeNothing(unittest.TestCase):
    def assert_rejected_and_unchanged(self, tickets, action, *args):
        before = copy.deepcopy(tickets)
        with self.assertRaises(ValidationError):
            action(tickets, *args)
        self.assertEqual(tickets, before)

    def test_unassigned_open_ticket_cannot_start_work(self):
        tickets = [make_ticket("T001", "open", None)]
        self.assert_rejected_and_unchanged(
            tickets, change_status, "T001", "in_progress"
        )

    def test_resolved_ticket_cannot_be_reassigned(self):
        tickets = [make_ticket("T001", "resolved", "Ada")]
        self.assert_rejected_and_unchanged(
            tickets, assign_ticket, "T001", "Grace"
        )

    def test_blank_staff_name_is_rejected(self):
        tickets = [make_ticket("T001", "open", None)]
        self.assert_rejected_and_unchanged(
            tickets, assign_ticket, "T001", "   "
        )

    def test_unknown_ticket_id_is_rejected_for_every_action(self):
        tickets = [make_ticket("T001", "open", "Ada")]
        for action, args in (
            (assign_ticket, ("T999", "Ada")),
            (change_status, ("T999", "in_progress")),
            (reopen_ticket, ("T999",)),
        ):
            with self.subTest(action=action.__name__):
                self.assert_rejected_and_unchanged(tickets, action, *args)

    def test_invalid_status_name_is_rejected(self):
        tickets = [make_ticket("T001", "open", "Ada")]
        self.assert_rejected_and_unchanged(
            tickets, change_status, "T001", "closed"
        )

    def test_open_ticket_cannot_jump_straight_to_resolved(self):
        tickets = [make_ticket("T001", "open", "Ada")]
        self.assert_rejected_and_unchanged(
            tickets, change_status, "T001", "resolved"
        )

    def test_resolved_ticket_cannot_change_status_without_reopen(self):
        tickets = [make_ticket("T001", "resolved", "Ada")]
        self.assert_rejected_and_unchanged(
            tickets, change_status, "T001", "in_progress"
        )

    def test_only_resolved_tickets_can_be_reopened(self):
        tickets = [make_ticket("T001", "in_progress", "Ada")]
        self.assert_rejected_and_unchanged(tickets, reopen_ticket, "T001")

    def test_rejected_action_on_one_ticket_leaves_the_others_untouched(self):
        tickets = [
            make_ticket("T001", "open", "Ada"),
            make_ticket("T002", "open", None),
        ]
        self.assert_rejected_and_unchanged(
            tickets, change_status, "T002", "in_progress"
        )


class TestValidActionsStillWork(unittest.TestCase):
    def test_full_lifecycle_open_to_resolved_and_back(self):
        tickets = [make_ticket("T001", "open", None)]

        assign_ticket(tickets, "T001", "  Ada ")
        self.assertEqual(tickets[0]["assigned_to"], "Ada")

        change_status(tickets, "T001", "in_progress")
        change_status(tickets, "T001", "resolved")
        self.assertEqual(tickets[0]["status"], "resolved")

        reopen_ticket(tickets, "T001")
        self.assertEqual(tickets[0]["status"], "open")


if __name__ == "__main__":
    unittest.main()