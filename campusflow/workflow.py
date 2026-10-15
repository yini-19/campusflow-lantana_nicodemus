from campusflow.validation import (
    ALLOWED_STATUSES,
    ValidationError,
    check_staff_name,
)


def find_ticket(tickets: list[dict], ticket_id: str) -> dict:
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            return ticket
    raise ValidationError(f"Ticket '{ticket_id}' not found")


def check_transition(ticket: dict, new_status: str) -> None:
    """Raise ValidationError if the move is illegal. Never changes the ticket."""
    current_status = ticket["status"]

    if current_status == "resolved":
        raise ValidationError("Resolved tickets must be reopened first")

    if new_status == current_status:
        raise ValidationError(f"Ticket is already {current_status}")

    if new_status == "open":
        raise ValidationError("Use reopen_ticket() to reopen a resolved ticket")

    if new_status == "in_progress" and not ticket["assigned_to"]:
        raise ValidationError("Cannot start work on an unassigned ticket")

    if new_status == "resolved" and current_status != "in_progress":
        raise ValidationError("Only an in-progress ticket can be resolved")


def assign_ticket(
    tickets: list[dict],
    ticket_id: str,
    staff_name: str,
) -> dict:
    staff_name = check_staff_name(staff_name)
    ticket = find_ticket(tickets, ticket_id)

    if ticket["status"] == "resolved":
        raise ValidationError("Reopen the ticket before modifying it")

    ticket["assigned_to"] = staff_name
    return ticket


def change_status(
    tickets: list[dict],
    ticket_id: str,
    new_status: str,
) -> dict:
    new_status = new_status.strip().lower()

    if new_status not in ALLOWED_STATUSES:
        raise ValidationError(f"Invalid status: {new_status}")

    ticket = find_ticket(tickets, ticket_id)
    check_transition(ticket, new_status)

    ticket["status"] = new_status
    return ticket


def get_work_queue(
    tickets: list[dict],
) -> list[dict]:
    priority_order = {
        "critical": 0,
        "high": 1,
        "medium": 2,
        "low": 3,
    }

    unresolved_tickets = [
        ticket
        for ticket in tickets
        if ticket["status"] in ("open")
    ]

    return sorted(
        unresolved_tickets,
        key=lambda ticket: (
            priority_order[ticket["priority"]],
            int(ticket["id"][1:]),
        ),
    )

def reopen_ticket(
    tickets: list[dict],
    ticket_id: str,
) -> dict:
    ticket = find_ticket(tickets, ticket_id)

    if ticket["status"] != "resolved":
        raise ValidationError("Only resolved tickets can be reopened")

    ticket["status"] = "open"
    return ticket