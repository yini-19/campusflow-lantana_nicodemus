# CampusFlow Design Decisions

## 1. Purpose

This document records the team's agreements on how CampusFlow modules communicate. It started as the contract for the first version and is now updated for CampusFlow Next. Section 12 lists decisions that changed during the upgrade and why.

Items marked **(proposed)** are waiting for Engineer B to confirm. Everything else describes code that exists on the feature branch.

## 2. Ticket Collection

**Decision:** The ticket collection is a Python list of dictionaries, managed by `main.py`.

- Each ticket is a dictionary.
- `main.py` loads the tickets when the application starts and passes the same list to every function that needs it.
- Functions that create tickets return a new ticket dictionary. `main.py` saves after each successful change.
- Functions that assign tickets, change status, reopen tickets or add notes update the matching ticket in place and return the result.

We do not use a database or a custom ticket class.

## 3. Error Handling and Validate-Before-Mutate

**Decision:** Business functions raise `ValidationError`, a subclass of `ValueError` defined in `campusflow/validation.py`.

- Existing `except ValueError` handlers still work, because `ValidationError` is a `ValueError`.
- Business functions never print and never call `input()`.
- `main.py` catches the error and shows a friendly message.
- **Every function checks all of its inputs and the ticket's current state first, and changes data only afterwards.** A rejected action therefore leaves the whole collection unchanged.

Expected errors include blank titles, unsupported categories or urgencies, invalid `affected_users`, unknown ticket IDs, blank staff names, illegal status transitions, invalid notes and invalid JSON data. Unexpected errors are not swallowed.

## 4. Function Contracts and Return Values

| Operation | Function | Returns | Raises `ValidationError` when |
| --- | --- | --- | --- |
| Create ticket | `create_ticket(tickets)` in `tickets.py` | New ticket dict (appended to the list) | Input is invalid (prompts retry until valid) |
| Next ticket ID | `next_ticket_id(tickets)` in `tickets.py` | ID string such as `T008` | n/a |
| Assign ticket | `assign_ticket(tickets, ticket_id, staff_name)` | Updated ticket | Name is blank, ID unknown, or ticket is resolved |
| Change status | `change_status(tickets, ticket_id, new_status)` | Updated ticket | Status invalid, ID unknown, or move is illegal |
| Check a move | `check_transition(ticket, new_status)` | `None` | The move is illegal. Never changes the ticket |
| Reopen ticket | `reopen_ticket(tickets, ticket_id)` | Updated ticket | Ticket is not resolved or ID unknown |
| Find ticket | `find_ticket(tickets, ticket_id)` | The ticket dict | ID unknown |
| Open Work Queue | `get_work_queue(tickets)` | New sorted list of **open** tickets | n/a |
| Add note | `add_note(tickets, ticket_id, author, message)` in `notes.py` | The new note dict | Author or message invalid, ID unknown, or ticket resolved |
| Read notes | `get_notes(tickets, ticket_id)` | Notes sorted by numeric note ID | ID unknown |
| Next note ID | `next_note_id(ticket)` | ID string such as `N003` | n/a |
| Validate one ticket | `validate_ticket(ticket)` in `storage.py` | `None` | Any rule is broken |
| Validate a collection | `validate_collection(tickets)` | `None` | Any record is invalid or an ID is duplicated |
| Load | `load_tickets(path=None)` | New validated list (`[]` if the file is missing) | JSON is invalid or any record is invalid |
| Reload in place | `reload_tickets(tickets, path=None)` | `None` | The file is invalid. `tickets` is then left unchanged |
| Save | `save_tickets(tickets, path=None)` | `None` | The collection is invalid. The existing file is then left untouched |
| Report | `generate_report(tickets)` | Dict with totals and breakdowns | n/a |

When `path` is omitted, the functions use `FILENAME` in `storage.py` (`tickets.json`).

## 5. Ticket Data Structure

```python
{
    "id": "T001",
    "title": "Network unavailable",
    "category": "Network",
    "urgency": "high",
    "affected_users": 12,
    "priority": "critical",
    "status": "open",
    "assigned_to": None,
    "notes": [
        {"note_id": "N001", "author": "Mentor A", "message": "Router reboot attempted"},
    ],
}
```

Agreed values:

- Ticket IDs: `T001`, `T002`, ... Note IDs: `N001`, `N002`, ... (per ticket).
- Categories: `Network`, `Hardware`, `Software`, `Other` (stored in this exact form).
- Urgency: `low`, `medium`, `high`.
- Priority: `critical`, `high`, `medium`, `low`.
- Status: `open`, `in_progress`, `resolved`.
- New tickets start `open`, unassigned, with `notes: []`.
- A note is identified by its ticket ID plus its note ID.

## 6. Business Rules

### Priority

Evaluated in order, first match wins:

1. High urgency **and** at least 10 affected users gives `critical`.
2. High urgency **or** at least 10 affected users gives `high`.
3. Medium urgency **or** at least 3 affected users gives `medium`.
4. Otherwise `low`.

Priority is calculated by `calculate_priority` in `tickets.py`. The loader checks that a stored priority matches this rule.

### Status and assignment

- `open` to `in_progress` requires an assigned ticket.
- Only `in_progress` can move to `resolved`.
- A resolved ticket must be reopened (back to `open`) before it can be assigned, changed or given notes.
- Only a resolved ticket can be reopened.
- An `in_progress` ticket must be assigned. This is checked on load as well as on change.

### Open Work Queue

- Shows **only `open` tickets**.
- Order: critical, high, medium, low. Ties are broken by the **numeric** part of the ticket ID, so `T2` comes before `T10`.
- `in_progress` and `resolved` tickets never appear in this queue.
- The queue is not silently replaced by other filtered views. Search results are a separate view.

### Follow-up notes

- Only `open` and `in_progress` tickets accept notes.
- Author: not blank after trimming. Message: 5 to 300 characters after trimming. Both are stored trimmed.
- A rejected note does not consume an ID.
- Notes are kept when a ticket is resolved or reopened.

## 7. Validation Design

**Decision:** Rules live in one place, `campusflow/validation.py`, as pure functions with no input, printing or mutation: `check_title`, `check_category`, `check_urgency`, `check_affected_users`, `check_staff_name`, `check_note_author`, `check_note_message`.

- `check_category` and `check_urgency` normalize with `strip()` and `casefold()`. Category returns the canonical form (`"  nEtWoRk "` becomes `"Network"`).
- `check_affected_users` uses `type(value) is int`, not `isinstance`, because `isinstance(True, int)` is `True`. Booleans, floats and strings are rejected, as are zero and negatives.
- The CLI converts typed text to an `int` before calling the validators.
- The interactive prompt functions in `tickets.py` (`validate_title`, `validate_category`, `validate_urgency`, `validate_affected_users`) keep their original names and loop on `input()`, but now delegate to the `check_*` helpers. Existing tests patch these names, so they were not renamed.

## 8. JSON Persistence

**Decision:** `campusflow/storage.py` owns loading, saving and validating the data file. ID generation lives with the code that creates the records (`next_ticket_id` in `tickets.py`, `next_note_id` in `notes.py`).

- **Format:** a JSON list of ticket objects. There is no envelope.
- **Loading:** parse the JSON, validate the whole collection (structure, required keys, ID format and uniqueness, category, urgency and status values, priority consistency, assignment rules, note shape and note-ID uniqueness per ticket), and only then return it. A failure raises `ValidationError` and changes nothing.
- **Reloading:** `reload_tickets` replaces the list contents in place only after a successful load.
- **Saving:** validate first, write to a temporary file, then replace `tickets.json`, so a failed write cannot corrupt the existing file.
- **Old files:** tickets without a `notes` key are accepted and treated as having no notes. The key is added when the first note is written. No migration is needed.
- **ID continuity:** both next-ID functions use the highest existing number plus one, compared numerically. They store no counters, so they cannot drift from the data, rejected notes cannot consume an ID, and a reload continues the sequence.

The workflow and note modules never open or write the data file.

## 9. Testing Approach

**Decision:** Business logic takes its values as arguments, so tests call functions directly and never type input. Temporary files are used for persistence tests so project data is never overwritten.

| Test file | Covers |
| --- | --- |
| `test_tickets.py` | Prompts, priority rules, ticket creation |
| `test_workflow.py` | Assignment, transitions, queue ordering |
| `test_storage.py` | Basic JSON save, load and malformed files |
| `test_validation.py` | Every `check_*` helper, including booleans and normalization |
| `test_ticket_safety.py` | Rejected actions leave the collection unchanged |
| `test_notes.py` | Note IDs, length limits, resolved tickets, reopen |
| `test_storage_safety.py` | Corrupt JSON, duplicate IDs, invalid records, ID continuity, atomic save |
| `test_bug_hunter_reports.py` | Report counts after resolve and reopen |

Techniques:

- **Prove "unchanged".** Take `copy.deepcopy` of the collection, run the action, assert it raised, then assert the collection equals the copy.
- **Check tests can fail.** Break the code temporarily, confirm the right tests fail, then restore it.

Run the suite from the repository root:

```bash
python -m unittest discover -s tests -v
```

All engineers run the full suite before opening or approving a pull request.

## 10. Team Responsibilities

**Engineer A**

- `validation.py`, status and assignment safety in `workflow.py`, `notes.py`, `storage.py`, `next_ticket_id`.
- Tests: `test_validation.py`, `test_ticket_safety.py`, `test_notes.py`, `test_storage_safety.py`.

**Engineer B**

- Search and filtering, `reports.py`, the notes menus in `main.py`, the Engineering Understanding Check.
- Their own tests for search, reports and the check.

**Shared:** function contracts, `main.py` integration, reviewing each other's pull requests, the README and the learning logs.

## 11. Pending Contracts with Engineer B (proposed)

These are not yet implemented or confirmed. Engineer B should accept or change them.

- B's code uses the same convention: raise `ValidationError`, never print from business functions, never change tickets during search or reporting.
- `generate_report` keeps the existing keys `total_tickets`, `status_breakdown` and `priority_breakdown`, and adds the new fields (category counts, unresolved and resolved counts, resolution percentage) alongside them. An empty collection reports 0%.
- Search filters combine with AND. An empty filter means "do not filter by that field".
- The notes menus call `add_note` and `get_notes` and show `str(error)` when a `ValidationError` is raised.

## 12. Decisions Changed During the Sprint

| Original decision | Change | Reason |
| --- | --- | --- |
| Work queue shows open and in-progress tickets | Shows open tickets only | The CampusFlow Next specification, reproduced as a failing test first (see `baseline-check.md`) |
| Errors are `ValueError` | `ValidationError`, a subclass of `ValueError` | One clear error type, old handlers still work |
| `generate_ticket_id(tickets)` in `storage.py` | `next_ticket_id(tickets)` in `tickets.py` | `storage.py` now imports `calculate_priority` from `tickets.py`; keeping ID creation in `tickets.py` avoids a circular import |
| Old tickets without `notes` load as `notes: []` | They load unchanged and `notes` is added on first note | The first-version storage tests compare loaded data exactly, so rewriting records on load would weaken them |
| Staff-name error text `"must not be blank"` | `"cannot be empty"` | An existing test checks that text; changing the helper was safer than changing the test |
| Storage fixture in `test_storage.py` (ticket with high urgency, 12 users and `low` priority) | Fixture changed to low urgency and 1 user | The stricter loader correctly flagged it as inconsistent; only the fixture changed, not the assertions |
| Planned `tests/test_integration.py` | Not created | Safety, notes and storage tests combine the modules instead |
| Work queue filter `in ("open")` | `== "open"` | `("open")` is a string, so `in` was a substring test |

## 13. Bug-Hunter Case (Engineer A for Engineer B's module)

- **Initial state:** four tickets. T001 is resolved then reopened (and has a note), T002 is resolved, T003 is `in_progress`, T004 is untouched.
- **Input:** `generate_report(tickets)`.
- **Expected:** each ticket is counted once under its current status (open 2, in_progress 1, resolved 1); priority counts also sum to 4; the tickets are not changed.
- **Actual:** passes against the current `reports.py`. No code change was needed.
- **Test:** `TestReportCountsAfterResolveAndReopen` in `tests/test_bug_hunter_reports.py`. It fails if open tickets are counted in more than one status bucket.

## 14. Agreement

These decisions are the shared contract for the sprint. Any change to function signatures, ticket fields or return values must be agreed by both engineers and recorded here before code that depends on it is merged.