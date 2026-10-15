import json
import os

from campusflow.validation import (
    ValidationError,
    check_affected_users,
    check_category,
    check_title,
    check_urgency,
)

ticket_dict = {}
FILENAME = "tickets.json"

allowed_categories = ("Network", "Hardware", "Software", "Other")
allowed_urgencies = ("low", "medium", "high")



def _prompt_until_valid(prompt, check):
    """Ask repeatedly until `check` accepts the text; print its message otherwise."""
    while True:
        text = input(prompt)
        try:
            return check(text)
        except ValidationError as error:
            print(error)


def _parse_affected_users(text):
    text = text.strip()
    if not text.isdigit():
        raise ValidationError("Entry must be a positive integer greater than 0")
    return check_affected_users(int(text))


def validate_title() -> str:
    return _prompt_until_valid("Ticket title: ", check_title)


def validate_category() -> str:
    return _prompt_until_valid(
        "Select category (Network, Software, Hardware, Other): ",
        check_category,
    )


def validate_urgency() -> str:
    return _prompt_until_valid(
        "Urgency level (high, medium or low): ", check_urgency
    )


def validate_affected_users() -> int:
    return _prompt_until_valid("Number of affected users: ", _parse_affected_users)


def calculate_priority(urgency: str, affected_users: int) -> str:
    if urgency == "high" and affected_users >= 10:
        return "critical"
    elif urgency == "high" or affected_users >= 10:
        return "high"
    elif urgency == "medium" or affected_users >= 3:
        return "medium"
    else:
        return "low"


def save_ticket(ticket: dict):
    filename = FILENAME

    if os.path.exists(filename):
        with open(filename, "r") as f:
            all_tickets = json.load(f)

            if isinstance(all_tickets, dict):
                all_tickets = [all_tickets]
    else:
        all_tickets = []

    all_tickets.append(ticket)

    with open(filename, "w") as f:
        json.dump(all_tickets, f, indent=4)


def create_ticket(tickets: list[dict]) -> dict:
    last_num = max(
        (int(ticket["id"][1:]) for ticket in tickets),
        default=0,
    )

    ticket_id = f"T{last_num + 1:03d}"

    ticket = {
        "id": ticket_id,
        "title": validate_title(),
        "category": validate_category(),
        "urgency": validate_urgency(),
        "affected_users": validate_affected_users(),
        "priority": "",
        "status": "open",
        "assigned_to": None,
        "notes": [],
    }

    ticket["priority"] = calculate_priority(
        ticket["urgency"],
        ticket["affected_users"],
    )

    tickets.append(ticket)

    print(f"Ticket {ticket_id} created successfully.")
    return ticket


def list_tickets(tickets: list[dict]) -> None:
    if not tickets:
        print("No tickets found.")
        return

    for ticket in tickets:
        for key, value in ticket.items():
            print(f"{key}: {value}")
        print()


def view_ticket(tickets: list[dict]) -> None:
    ticket_id = input("Input ticket ID: ").strip().upper()

    for ticket in tickets:
        if ticket["id"] == ticket_id:
            for key, value in ticket.items():
                print(f"{key}: {value}")
            return

    print("Ticket not found.")