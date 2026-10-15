VALID_CATEGORIES = ["Network", "Hardware", "Software", "Other"]
VALID_STATUSES = ["open", "in_progress", "resolved"]
VALID_PRIORITIES = ["critical", "high", "medium", "low"]

PRIORITY_RANK = {"critical": 0, "high": 1, "medium": 2, "low": 3}


def ticket_number(ticket_id):
    """'T010' -> 10, so ordering is numeric, not text-based."""
    return int(ticket_id[1:])


def normalize_filter(value, allowed):
    """Return the canonical option, or None if blank.
    Raises ValueError if the value is not an allowed option."""
    cleaned = value.strip().casefold()
    if cleaned == "":
        return None
    for option in allowed:
        if option.casefold() == cleaned:
            return option
    raise ValueError(f"Invalid option: {value!r}. Allowed: {', '.join(allowed)}")


def search_tickets(tickets, title_text="", category=None, status=None, priority=None):
    """Read-only. Returns a NEW list of tickets matching ALL supplied filters."""
    needle = title_text.strip().casefold()
    results = []
    for ticket in tickets:
        if needle and needle not in ticket["title"].casefold():
            continue
        if category is not None and ticket["category"] != category:
            continue
        if status is not None and ticket["status"] != status:
            continue
        if priority is not None and ticket["priority"] != priority:
            continue
        results.append(ticket)
    return results


def sort_by_priority_then_id(tickets):
    """Separate optional view. Does NOT replace the Open Work Queue."""
    return sorted(
        tickets,
        key=lambda t: (PRIORITY_RANK[t["priority"]], ticket_number(t["id"])),
    )