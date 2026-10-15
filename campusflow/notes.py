"""Follow-up notes: business rules only (no input(), no print())."""

from campusflow.validation import (
    ValidationError,
    check_note_author,
    check_note_message,
)
from campusflow.workflow import find_ticket

NOTE_ALLOWED_STATUSES = ("open", "in_progress")


def next_note_id(ticket: dict) -> str:
    """Return the next free note ID for one ticket (N001, N002, ...).

    Derived from the notes that already exist, so a rejected note can never
    consume an ID and a reload continues the sequence automatically.
    """
    numbers = [int(note["note_id"][1:]) for note in ticket.get("notes", [])]
    return f"N{max(numbers, default=0) + 1:03d}"


def add_note(
    tickets: list[dict],
    ticket_id: str,
    author: str,
    message: str,
) -> dict:
    """Add a note to an open or in_progress ticket and return the new note.

    Raises ValidationError (and changes nothing) if the author or message is
    invalid, the ticket does not exist, or the ticket is resolved.
    """
    author = check_note_author(author)
    message = check_note_message(message)
    ticket = find_ticket(tickets, ticket_id)

    if ticket["status"] not in NOTE_ALLOWED_STATUSES:
        raise ValidationError(
            "Resolved tickets cannot receive notes; reopen the ticket first"
        )

    note = {
        "note_id": next_note_id(ticket),
        "author": author,
        "message": message,
    }
    ticket.setdefault("notes", []).append(note)
    return note


def get_notes(tickets: list[dict], ticket_id: str) -> list[dict]:
    """Return a copy of the ticket's notes in note-ID order."""
    ticket = find_ticket(tickets, ticket_id)
    notes = ticket.get("notes", [])
    return sorted(notes, key=lambda note: int(note["note_id"][1:]))