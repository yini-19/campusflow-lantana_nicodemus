STATUSES = ["open", "in_progress", "resolved"]
PRIORITIES = ["critical", "high", "medium", "low"]
CATEGORIES = ["Network", "Hardware", "Software", "Other"]


def build_report(tickets):
    """Pure calculation. Returns a dict. No printing."""
    total = len(tickets)
    by_status = {s: 0 for s in STATUSES}
    by_priority = {p: 0 for p in PRIORITIES}
    by_category = {c: 0 for c in CATEGORIES}

    for ticket in tickets:
        by_status[ticket["status"]] += 1
        by_priority[ticket["priority"]] += 1
        by_category[ticket["category"]] += 1

    resolved = by_status["resolved"]
    unresolved = by_status["open"] + by_status["in_progress"]
    percentage = (resolved / total * 100) if total > 0 else 0.0

    return {
        "total": total,
        "by_status": by_status,
        "by_priority": by_priority,
        "by_category": by_category,
        "unresolved": unresolved,
        "resolved": resolved,
        "resolution_percentage": percentage,
    }


def format_report(report):
    """Turns the dict into text lines. The CLI prints them."""
    lines = [
        f"Total tickets: {report['total']}",
        f"Unresolved (open + in_progress): {report['unresolved']}",
        f"Resolved: {report['resolved']}",
        f"Resolution rate: {report['resolution_percentage']:.1f}%",
        "By status:",
    ]
    lines += [f"  {k}: {v}" for k, v in report["by_status"].items()]
    lines.append("By priority:")
    lines += [f"  {k}: {v}" for k, v in report["by_priority"].items()]
    lines.append("By category:")
    lines += [f"  {k}: {v}" for k, v in report["by_category"].items()]
    return lines