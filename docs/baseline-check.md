# CampusFlow Next — Baseline Check

## Project information

- **Project:** CampusFlow Next
- **Engineer:** Engineer A
- **Branch:** `feat/21-validation-and-notes`
- **Date:** 2026-10-14

## 1. Original automated test results

**Command:**

```bash
python3 -m unittest discover -s tests -v
```

**Original result before the work-queue test was changed:**
- Tests run: 38
- Passed: 38
- Failed: 0
- Errors: 0

**Current result after subsequent changes:** 
File "/home/student/campusflow-lantana_nicodemus/tests/test_workflow.py", line 1
    ``
    ^
SyntaxError: invalid syntax


----------------------------------------------------------------------
Ran 20 tests in 0.038s

FAILED (errors=1)

## 2. Manual input tests

Record the actual results after running `python3 main.py`.

| Test | Input | Actual result |
|---|---|---|
| 1 | Blank ticket title | It returned: Title field must not be empty and prompted user to input correct title |
| 2 | Invalid category: `Food` | It returned: Unsupported category. Please try again. |
| 3 | Affected users: `0` | It returned: Entry must be a positive integer greater than 0 |

Do not record a test as passed unless you observed the expected behaviour.

## 3. Areas identified for improvement

The project brief identifies the following areas for investigation and improvement:

1. Centralized validation of ticket data.
2. Safe assignment and status transitions.
3. Structured follow-up notes with validation and unique IDs.
4. Safe JSON loading and saving, including validation of the complete collection.
5. Ticket and note ID continuity after reload.
6. More automated negative-case and regression tests.
7. An Open Work Queue that includes only open tickets, ordered by priority and numeric ticket ID.

These are improvement requirements. Each suspected defect must be checked against the implementation and tests before it is described as a confirmed bug.

## 4. Baseline conclusion

The original automated test suite passed all 38 tests. Further work is needed to verify the new acceptance requirements, strengthen validation and storage safety, and add tests for invalid operations and unchanged state.

The baseline results will be used to compare behaviour after implementation changes.