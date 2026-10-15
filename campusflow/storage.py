"""Safe JSON storage: validate everything first, replace memory last."""

import json
import os
import re
from pathlib import Path

from campusflow.tickets import calculate_priority
from campusflow.validation import (
    ALLOWED_CATEGORIES,
    ALLOWED_STATUSES,
    ALLOWED_URGENCIES,
    ValidationError,
    check_affected_users,
    check_note_message,
    check_title,
)

FILENAME = Path("tickets.json")

REQUIRED_TICKET_KEYS = (
    "id",
    "title",
    "category",
    "urgency",
    "affected_users",
    "priority",
    "status",
    "assigned_to",
)
NOTE_KEYS = {"note_id", "author", "message"}
TICKET_ID_PATTERN = re.compile(r"T[0-9]{3,}")
NOTE_ID_PATTERN = re.compile(r"N[0-9]{3,}")


def validate_note(note) -> None:
    if not isinstance(note, dict) or set(note) != NOTE_KEYS:
        raise ValidationError(
            "each note must have exactly note_id, author and message"
        )
    note_id = note["note_id"]
    if not isinstance(note_id, str) or not NOTE_ID_PATTERN.fullmatch(note_id):
        raise ValidationError(f"invalid note_id {note_id!r}")
    if not isinstance(note["author"], str) or not note["author"].strip():
        raise ValidationError(f"note {note_id} has a blank author")
    check_note_message(note["message"])


def validate_ticket(ticket) -> None:
    """Raise ValidationError if the ticket breaks a rule. Never mutates."""
    if not isinstance(ticket, dict):
        raise ValidationError("ticket must be an object")

    missing = [key for key in REQUIRED_TICKET_KEYS if key not in ticket]
    if missing:
        raise ValidationError(f"missing keys: {', '.join(missing)}")

    ticket_id = ticket["id"]
    if not isinstance(ticket_id, str) or not TICKET_ID_PATTERN.fullmatch(
        ticket_id
    ):
        raise ValidationError(f"invalid ticket id {ticket_id!r}")

    check_title(ticket["title"])
    check_affected_users(ticket["affected_users"])

    if ticket["category"] not in ALLOWED_CATEGORIES:
        raise ValidationError(f"invalid category {ticket['category']!r}")
    if ticket["urgency"] not in ALLOWED_URGENCIES:
        raise ValidationError(f"invalid urgency {ticket['urgency']!r}")
    if ticket["status"] not in ALLOWED_STATUSES:
        raise ValidationError(f"invalid status {ticket['status']!r}")

    expected = calculate_priority(ticket["urgency"], ticket["affected_users"])
    if ticket["priority"] != expected:
        raise ValidationError(
            f"priority is {ticket['priority']!r} but should be {expected!r}"
        )

    assigned_to = ticket["assigned_to"]
    if assigned_to is not None and (
        not isinstance(assigned_to, str) or not assigned_to.strip()
    ):
        raise ValidationError("assigned_to must be a name or null")
    if ticket["status"] == "in_progress" and assigned_to is None:
        raise ValidationError("an in_progress ticket must be assigned")

    if "notes" in ticket:
        notes = ticket["notes"]
        if not isinstance(notes, list):
            raise ValidationError("notes must be a list")
        seen_note_ids = set()
        for note in notes:
            validate_note(note)
            if note["note_id"] in seen_note_ids:
                raise ValidationError(
                    f"duplicate note_id {note['note_id']}"
                )
            seen_note_ids.add(note["note_id"])


def validate_collection(tickets) -> None:
    """Validate every ticket and cross-ticket rules. Never mutates."""
    if not isinstance(tickets, list):
        raise ValidationError("tickets.json must contain a list of tickets")

    seen_ids = set()
    for position, ticket in enumerate(tickets, start=1):
        try:
            validate_ticket(ticket)
        except ValidationError as error:
            raise ValidationError(f"Ticket record {position}: {error}") from error
        if ticket["id"] in seen_ids:
            raise ValidationError(
                f"Ticket record {position}: duplicate ticket id {ticket['id']}"
            )
        seen_ids.add(ticket["id"])


def load_tickets(path=None) -> list[dict]:
    """Return a fully validated list of tickets, or raise without side effects."""
    path = Path(path) if path is not None else FILENAME

    if not path.exists():
        return []

    try:
        with path.open("r", encoding="utf-8") as file:
            tickets = json.load(file)
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        raise ValidationError(f"Invalid JSON in {path}: {error}") from error

    validate_collection(tickets)
    return tickets


def reload_tickets(tickets: list[dict], path=None) -> None:
    """Replace `tickets` in place with the file's contents.

    The file is loaded and validated first; if that fails, `tickets` is
    left exactly as it was.
    """
    loaded = load_tickets(path)
    tickets[:] = loaded


def save_tickets(tickets: list[dict], path=None) -> None:
    """Validate, then write atomically so a failure never corrupts the file."""
    path = Path(path) if path is not None else FILENAME
    validate_collection(tickets)

    temp_path = path.with_name(path.name + ".tmp")
    try:
        with temp_path.open("w", encoding="utf-8") as file:
            json.dump(tickets, file, indent=4)
        os.replace(temp_path, path)
    finally:
        if temp_path.exists():
            temp_path.unlink()