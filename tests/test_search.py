import copy
import unittest

from campusflow.search import search_tickets, sort_by_priority_then_id


def make_ticket(tid, title, category, status, priority):
    return {"id": tid, "title": title, "category": category,
            "urgency": "low", "affected_users": 1, "priority": priority,
            "status": status, "assigned_to": None, "notes": []}


class SearchTests(unittest.TestCase):
    def setUp(self):
        self.tickets = [
            make_ticket("T001", "WiFi down in lab", "Network", "open", "high"),
            make_ticket("T002", "wifi slow", "Network", "resolved", "low"),
            make_ticket("T010", "Laptop wifi driver", "Hardware", "open", "critical"),
            make_ticket("T003", "Printer jam", "Hardware", "open", "medium"),
        ]

    def test_title_search_ignores_case_and_matches_substring(self):
        results = search_tickets(self.tickets, "WIFI")
        self.assertEqual([t["id"] for t in results], ["T001", "T002", "T010"])

    def test_combined_filters_use_and(self):
        results = search_tickets(self.tickets, "wifi", category="Network", status="open")
        self.assertEqual([t["id"] for t in results], ["T001"])

    def test_no_filters_returns_everything(self):
        self.assertEqual(len(search_tickets(self.tickets)), 4)

    def test_search_does_not_modify_tickets(self):
        before = copy.deepcopy(self.tickets)
        search_tickets(self.tickets, "wifi", category="Network", status="open")
        self.assertEqual(self.tickets, before)

    def test_sort_uses_numeric_id_for_ties(self):
        tickets = [
            make_ticket("T10", "a", "Other", "open", "high"),
            make_ticket("T2", "b", "Other", "open", "high"),
        ]
        ordered = sort_by_priority_then_id(tickets)
        self.assertEqual([t["id"] for t in ordered], ["T2", "T10"])


if __name__ == "__main__":
    unittest.main()