from campusflow.search import (
    VALID_CATEGORIES, VALID_STATUSES, VALID_PRIORITIES,
    normalize_filter, search_tickets, sort_by_priority_then_id,
)
from campusflow.reports import build_report, format_report

# PLACEHOLDERS: replace with the real names agreed with Engineer A in Stage 1
from campusflow.notes import add_note, get_notes
from campusflow.storage import get_all_tickets


def prompt_filter(label, allowed, input_fn=input, output_fn=print):
    """Re-prompts until the user gives a valid option or leaves it blank."""
    while True:
        raw = input_fn(f"{label} ({'/'.join(allowed)}, blank = any): ")
        try:
            return normalize_filter(raw, allowed)
        except ValueError as error:
            output_fn(f"{error}. Please try again.")


def show_tickets(tickets, output_fn=print):
    if not tickets:
        output_fn("No tickets found.")
        return
    for t in tickets:
        output_fn(
            f"{t['id']} | {t['title']} | {t['category']} | "
            f"{t['priority']} | {t['status']} | {t.get('assigned_to') or 'unassigned'}"
        )


def search_view(input_fn=input, output_fn=print):
    title = input_fn("Title contains (blank = any): ")
    category = prompt_filter("Category", VALID_CATEGORIES, input_fn, output_fn)
    status = prompt_filter("Status", VALID_STATUSES, input_fn, output_fn)
    priority = prompt_filter("Priority", VALID_PRIORITIES, input_fn, output_fn)

    results = search_tickets(get_all_tickets(), title, category, status, priority)

    sort_choice = input_fn("Sort by priority then ID? (y/n): ").strip().casefold()
    if sort_choice == "y":
        results = sort_by_priority_then_id(results)
    show_tickets(results, output_fn)


def report_view(output_fn=print):
    for line in format_report(build_report(get_all_tickets())):
        output_fn(line)


def add_note_view(input_fn=input, output_fn=print):
    ticket_id = input_fn("Ticket ID: ").strip()
    author = input_fn("Author: ")
    message = input_fn("Note message (5-300 characters): ")
    try:
        # PLACEHOLDER: adapt to A's error convention (exceptions vs results)
        note = add_note(ticket_id, author, message)
        output_fn(f"Note {note['note_id']} added to {ticket_id}.")
    except ValueError as error:
        output_fn(f"Could not add note: {error}")


def view_notes_view(input_fn=input, output_fn=print):
    ticket_id = input_fn("Ticket ID: ").strip()
    try:
        notes = get_notes(ticket_id)  # PLACEHOLDER
    except ValueError as error:
        output_fn(f"Could not read notes: {error}")
        return
    if not notes:
        output_fn("This ticket has no notes yet.")
        return
    for n in sorted(notes, key=lambda n: n["note_id"]):
        output_fn(f"{n['note_id']} | {n['author']}: {n['message']}")