import unittest

from campusflow.reports import build_report


def t(tid, status, priority="low", category="Other"):
    return {"id": tid, "status": status, "priority": priority, "category": category}


class ReportTests(unittest.TestCase):
    def test_empty_report_is_zero_percent(self):
        report = build_report([])
        self.assertEqual(report["total"], 0)
        self.assertEqual(report["resolution_percentage"], 0.0)

    def test_counts_match_known_fixture(self):
        tickets = [
            t("T001", "open", "high", "Network"),
            t("T002", "in_progress", "low", "Hardware"),
            t("T003", "resolved", "low", "Network"),
            t("T004", "open", "critical", "Software"),  # e.g. reopened: counts as open
        ]
        report = build_report(tickets)
        self.assertEqual(report["total"], 4)
        self.assertEqual(report["unresolved"], 3)       # open + in_progress
        self.assertEqual(report["resolved"], 1)
        self.assertEqual(report["resolution_percentage"], 25.0)
        self.assertEqual(sum(report["by_status"].values()), 4)   # no double-counting


if __name__ == "__main__":
    unittest.main()