# CampusFlow Design Decisions

## 1. Purpose

This document records the team's agreements on how CampusFlow modules communicate. All engineers should follow these decisions when implementing features and tests.

## 2. Ticket Collection

**Decision:** The ticket collection is a Python list of dictionaries, managed by `main.py`.

* Each ticket is represented by a dictionary.
* `main.py` loads the tickets when the application starts.
* The same ticket list is passed to functions that need to read or update tickets.
* Functions that create tickets return a new ticket dictionary. `main.py` appends it to the collection.
* Functions that assign tickets or change their status update the matching ticket in the collection and return the updated dictionary.

We will not introduce a database or a custom ticket class for this sprint.

## 3. Input Validation and Error Handling

**Decision:** Business logic functions raise `ValueError` when user input or a requested operation is invalid.

Examples include:

* Blank ticket titles.
* Unsupported categories or urgency values.
* Zero or negative affected-user counts.
* Unknown ticket IDs.
* Blank staff names.
* Invalid status transitions.

The CLI in `main.py` catches expected `ValueError` exceptions and displays a helpful error message. Invalid input should not crash the application or silently change ticket data.

Unexpected errors should not be silently swallowed.

## 4. Function Return Values

**Decision:** Functions return their results directly. They do not print messages or request interactive input.

| Operation            | Expected return value                                         |
| -------------------- | ------------------------------------------------------------- |
| Create ticket        | The newly created ticket dictionary                           |
| Assign ticket        | The updated ticket dictionary                                 |
| Change ticket status | The updated ticket dictionary                                 |
| Reopen ticket        | The reopened ticket dictionary                                |
| Get one ticket       | The matching ticket dictionary                                |
| List tickets         | A list of ticket dictionaries                                 |
| Get work queue       | A sorted list of unresolved ticket dictionaries               |
| Generate report      | A dictionary containing totals and status/priority breakdowns |
| Load tickets         | A list of ticket dictionaries                                 |
| Save tickets         | `None` when saving succeeds                                   |
| Generate ticket ID   | A unique ID string, such as `T001`                            |

Functions that fail because of invalid input or an invalid operation raise `ValueError`.

## 5. Ticket Data Structure

**Decision:** All modules use the same ticket dictionary structure.

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
}
```

The following values are agreed:

* Ticket IDs use the format `T001`, `T002`, `T003`, and so on.
* Categories are `Network`, `Hardware`, `Software`, or `Other`.
* Urgency values are `low`, `medium`, or `high`.
* Priority values are `critical`, `high`, `medium`, or `low`.
* Status values are `open`, `in_progress`, or `resolved`.
* New tickets start with status `open` and an empty `assigned_to` value.

Priority is calculated by the ticket creation logic, not by the workflow module.

## 6. JSON Persistence

**Decision:** `campusflow/storage.py` owns JSON loading, saving, and ticket ID generation.

* `load_tickets(path)` loads saved tickets and returns a list.
* If the file does not exist, loading returns an empty list.
* Malformed JSON or invalid stored ticket data raises a clear `ValueError`.
* `save_tickets(tickets, path)` saves the current ticket collection.
* `generate_ticket_id(tickets)` creates an ID that does not duplicate an existing ticket ID.

`main.py` calls the storage functions when the application starts, after ticket creation or modification, and when appropriate before exiting.

The workflow and ticket creation modules do not open or write the JSON file directly.

## 7. Testing Without Interactive Input

**Decision:** Business logic functions accept their required values as arguments and never call `input()` or print CLI messages.

* `tests/test_tickets.py` tests ticket validation, creation, and priority calculation.
* `tests/test_workflow.py` tests assignment, status transitions, ticket lookup, and queue ordering.
* `tests/test_storage.py` tests JSON persistence, malformed files, and ID generation.
* `tests/test_integration.py` tests interactions between modules.

Tests call functions directly, pass sample data, and use assertions to check results or expected exceptions. Temporary files are used for persistence tests so real project data is not overwritten.

The CLI is responsible for collecting input and displaying results. This separation allows business logic to be tested automatically.

## 8. Team Responsibilities

**Engineer A: `campusflow/tickets.py`**

* Ticket creation.
* Input validation.
* Priority calculation.
* Automated tests in `tests/test_tickets.py`.

**Engineer B: `campusflow/workflow.py`**

* Ticket assignment.
* Status transitions and reopening.
* Ticket lookup and listing.
* Work queue sorting.
* Automated tests in `tests/test_workflow.py`.

**Shared responsibilities**

* `campusflow/storage.py`: JSON persistence and ticket ID generation.
* `campusflow/reports.py`: report generation.
* `main.py`: CLI interaction and coordination of modules.
* Integration tests: verify that the modules work together.

## 9. Running the Tests

The team will use Python's standard `unittest` framework.

```bash
python -m unittest discover -s tests -v
```

All engineers should run the full test suite before submitting their changes for integration.

## 10. Agreement

These decisions serve as the shared contract for the sprint. Any changes to function signatures, ticket fields, or return values must be agreed upon by both fellows and documented here before integrating code that could introduce incompatibilities.


Initial state:
Input:
Expected result:
Actual result:
Test name:
Code change made (if any):