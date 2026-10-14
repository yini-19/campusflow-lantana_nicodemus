
def assign_ticket(
    tickets: list[dict],
    ticket_id: str,
    staff_name: str,
) -> dict:
    staff_name = staff_name.strip()

    if not staff_name:
        raise ValueError("Staff name cannot be empty")

    for ticket in tickets:
        if ticket["id"] == ticket_id:
            if ticket["status"] == "resolved":
                raise ValueError(
                    "Reopen the ticket before modifying it"
                )

            ticket["assigned_to"] = staff_name
            return ticket

    raise ValueError(f"Ticket '{ticket_id}' not found")


def change_status(
    tickets: list[dict],
    ticket_id: str,
    new_status: str,
) -> dict:
    allowed_statuses = {"open", "in_progress", "resolved"}

    new_status = new_status.strip().lower()

    if new_status not in allowed_statuses:
        raise ValueError(f"Invalid status: {new_status}")

    for ticket in tickets:
        if ticket["id"] == ticket_id:
            current_status = ticket["status"]

            if current_status == "resolved":
                raise ValueError(
                    "Resolved tickets must be reopened first"
                )

            if new_status == current_status:
                raise ValueError(
                    f"Ticket is already {current_status}"
                )

            if new_status == "open":
                raise ValueError(
                    "Use reopen_ticket() to reopen a resolved ticket"
                )

            if new_status == "in_progress":
                if current_status != "open":
                    raise ValueError(
                        "Ticket must be open before work starts"
                    )

                if not ticket["assigned_to"]:
                    raise ValueError(
                        "Cannot start work on an unassigned ticket"
                    )

            elif new_status == "resolved":
                if current_status != "in_progress":
                    raise ValueError(
                        "Only an in-progress ticket can be resolved"
                    )

            ticket["status"] = new_status
            return ticket

    raise ValueError(f"Ticket '{ticket_id}' not found")

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
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            if ticket["status"] != "resolved":
                raise ValueError(
                    "Only resolved tickets can be reopened"
                )

            ticket["status"] = "open"
            return ticket

    raise ValueError(f"Ticket '{ticket_id}' not found")