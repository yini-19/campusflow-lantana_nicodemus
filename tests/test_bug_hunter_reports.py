"""Bug-hunter test (Engineer A for Engineer B's reports module).

Edge case: tickets that move through resolve and reopen must be counted
exactly once, under their CURRENT status, and building a report must not
change the tickets.
"""

import copy
import unittest

from campusflow.notes import add_note
from campusflow.reports import build_report
from campusflow.workflow import assign_ticket, change_status, reopen_ticket


def make_ticket(ticket_id, urgency="low", users=1, priority="low"):
    return {
        "id": ticket_id,
        "title": f"Ticket {ticket_id}",
        "category": "Software",
        "urgency": urgency,
        "affected_users": users,
        "priority": priority,
        "status": "open",
        "assigned_to": None,
        "notes": [],
    }


def build_fixture():
    """T001 resolved then reopened (open), T002 resolved, T003 in_progress,
    T004 untouched (open). Ticket T001 and T002 also carry notes."""
    tickets = [
        make_ticket("T001", "high", 12, "critical"),
        make_ticket("T002", "high", 2, "high"),
        make_ticket("T003", "medium", 1, "medium"),
        make_ticket("T004", "low", 1, "low"),
    ]
    for ticket_id in ("T001", "T002", "T003"):
        assign_ticket(tickets, ticket_id, "Ada")
        change_status(tickets, ticket_id, "in_progress")
    add_note(tickets, "T001", "Mentor A", "Checked the switch ports")
    change_status(tickets, "T001", "resolved")
    change_status(tickets, "T002", "resolved")
    reopen_ticket(tickets, "T001")
    return tickets


class TestReportCountsAfterResolveAndReopen(unittest.TestCase):
    def setUp(self):
        self.tickets = build_fixture()
        self.report = build_report(self.tickets)

    def test_status_counts_follow_the_current_status(self):
        self.assertEqual(
            self.report["by_status"],
            {"open": 2, "in_progress": 1, "resolved": 1},
        )

    def test_every_ticket_is_counted_exactly_once(self):
        total = self.report["total"]

        self.assertEqual(total, 4)
        self.assertEqual(sum(self.report["by_status"].values()), total)
        self.assertEqual(sum(self.report["by_priority"].values()), total)

    def test_priority_counts_match_the_fixture(self):
        self.assertEqual(
            self.report["by_priority"],
            {"critical": 1, "high": 1, "medium": 1, "low": 1},
        )

    def test_unresolved_and_resolved_add_up_to_the_total(self):
        self.assertEqual(self.report["unresolved"], 3)
        self.assertEqual(self.report["resolved"], 1)
        self.assertEqual(
            self.report["unresolved"] + self.report["resolved"],
            self.report["total"],
        )

    def test_resolution_percentage_and_category_counts(self):
        self.assertEqual(self.report["resolution_percentage"], 25.0)
        self.assertEqual(sum(self.report["by_category"].values()), 4)

    def test_building_a_report_does_not_change_the_tickets(self):
        before = copy.deepcopy(self.tickets)

        build_report(self.tickets)

        self.assertEqual(self.tickets, before)


if __name__ == "__main__":
    unittest.main()