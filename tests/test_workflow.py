import unittest

from campusflow.workflow import (
    assign_ticket,
    change_status,
    get_work_queue,
    reopen_ticket,
)


def make_ticket(
    ticket_id="T001",
    priority="medium",
    status="open",
    assigned_to=None,
):
    return {
        "id": ticket_id,
        "title": f"Test ticket {ticket_id}",
        "category": "Software",
        "urgency": "medium",
        "affected_users": 2,
        "priority": priority,
        "status": status,
        "assigned_to": assigned_to,
    }


class TestAssignTicket(unittest.TestCase):
    def test_assign_ticket_to_staff(self):
        tickets = [make_ticket()]

        result = assign_ticket(tickets, "T001", " Ada ")

        self.assertEqual(result["assigned_to"], "Ada")
        self.assertIs(result, tickets[0])

    def test_assign_ticket_rejects_empty_staff_name(self):
        with self.assertRaisesRegex(ValueError, "cannot be empty"):
            assign_ticket([make_ticket()], "T001", "   ")

    def test_assign_ticket_rejects_unknown_id(self):
        with self.assertRaisesRegex(ValueError, "not found"):
            assign_ticket([make_ticket()], "T999", "Ada")

    def test_assign_ticket_rejects_resolved_ticket(self):
        tickets = [make_ticket(status="resolved")]

        with self.assertRaisesRegex(ValueError, "Reopen"):
            assign_ticket(tickets, "T001", "Ada")


class TestChangeStatus(unittest.TestCase):
    def test_assigned_ticket_can_move_to_in_progress(self):
        tickets = [make_ticket(assigned_to="Ada")]

        result = change_status(tickets, "T001", "in_progress")

        self.assertEqual(result["status"], "in_progress")

    def test_unassigned_ticket_cannot_start_work(self):
        tickets = [make_ticket()]

        with self.assertRaisesRegex(ValueError, "unassigned"):
            change_status(tickets, "T001", "in_progress")

        self.assertEqual(tickets[0]["status"], "open")

    def test_in_progress_ticket_can_be_resolved(self):
        tickets = [
            make_ticket(status="in_progress", assigned_to="Ada")
        ]

        result = change_status(tickets, "T001", "resolved")

        self.assertEqual(result["status"], "resolved")

    def test_open_ticket_cannot_be_resolved_directly(self):
        tickets = [make_ticket(assigned_to="Ada")]

        with self.assertRaisesRegex(ValueError, "in-progress"):
            change_status(tickets, "T001", "resolved")

    def test_invalid_status_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Invalid status"):
            change_status([make_ticket()], "T001", "pending")

    def test_same_status_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "already open"):
            change_status([make_ticket()], "T001", "open")

    def test_resolved_ticket_must_be_reopened_first(self):
        tickets = [make_ticket(status="resolved")]

        with self.assertRaisesRegex(ValueError, "reopened"):
            change_status(tickets, "T001", "in_progress")

    def test_unknown_ticket_cannot_change_status(self):
        with self.assertRaisesRegex(ValueError, "not found"):
            change_status([make_ticket()], "T999", "in_progress")


class TestReopenTicket(unittest.TestCase):
    def test_reopen_resolved_ticket(self):
        tickets = [make_ticket(status="resolved")]

        result = reopen_ticket(tickets, "T001")

        self.assertEqual(result["status"], "open")

    def test_cannot_reopen_ticket_that_is_not_resolved(self):
        with self.assertRaisesRegex(ValueError, "Only resolved"):
            reopen_ticket([make_ticket()], "T001")

    def test_reopening_unknown_ticket_fails(self):
        with self.assertRaisesRegex(ValueError, "not found"):
            reopen_ticket([], "T999")


class TestWorkQueue(unittest.TestCase):
    def test_queue_sorts_by_priority_then_numeric_id(self):
        tickets = [
            make_ticket("T010", "low"),
            make_ticket("T008", "high"),
            make_ticket("T002", "critical"),
            make_ticket("T001", "critical"),
            make_ticket("T003", "medium"),
        ]

        queue = get_work_queue(tickets)

        self.assertEqual(
            [ticket["id"] for ticket in queue],
            ["T001", "T002", "T008", "T003", "T010"],
        )

    def test_queue_contains_only_open_tickets(self):
        tickets = [
            make_ticket("T001", "critical", "open"),
            make_ticket("T002", "high", "resolved"),
            make_ticket("T003", "low", "in_progress", "Ada"),
        ]

        queue = get_work_queue(tickets)

        self.assertEqual([t["id"] for t in queue], ["T001"])

    def test_empty_queue_returns_empty_list(self):
        self.assertEqual(get_work_queue([]), [])

    def test_queue_does_not_mutate_original_list(self):
        tickets = [
            make_ticket("T002", "low"),
            make_ticket("T001", "critical"),
        ]
        original_ids = [ticket["id"] for ticket in tickets]

        get_work_queue(tickets)

        self.assertEqual(
            [ticket["id"] for ticket in tickets],
            original_ids,
        )


if __name__ == "__main__":
    unittest.main()