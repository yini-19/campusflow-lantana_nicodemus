# CampusFlow — Individual AI Learning Log

### Fellow: YIYAKAZAH NICODEMUS 
### Role: Engineer A 
### Project: CampusFlow


# Interaction
# 1 — Validating Ticket Input

### Problem

CampusFlow requires users to provide valid information when creating a ticket. The ticket title must not be empty, the category must belong to a supported list, urgency must be low, medium, or high, and the number of affected users must be a positive integer.

I needed to understand how to validate user input in Python and prevent invalid information from being stored in the ticket system.

### My initial understanding

I understood how to collect information using Python's `input()` function, but I was unsure how to repeatedly request input when the user entered an invalid value. I also needed to understand how to validate different data types and handle variations in capitalization.

### Prompt to AI

"Explain how Python functions, while loops, and conditional statements can be used to validate user input. Use an unrelated example involving a student registration system. Show how to reject empty strings, restrict choices to a predefined list, and validate a positive integer. Do not write my CampusFlow implementation for me."

### Useful AI guidance

I learned that a `while True` loop can repeatedly request input until a valid value is entered. Conditional statements check whether the input meets specific requirements, while `return` exits the function once valid input has been obtained.

For example, a student registration system could validate a student's department:


```python
def validate_department():
    allowed_departments = ("Science", "Arts", "Business")

    while True:
        department = input("Enter department: ").strip().capitalize()

        if department in allowed_departments:
            return department

        print("Invalid department. Try again.")
```

The `strip()` method removes unnecessary spaces, while `capitalize()` normalizes the first letter. The function returns only when the department matches one of the allowed options.

I also learned that `isdigit()` can help validate positive whole-number input, although additional checks may be required depending on the accepted input format.

### My independent experiment/test

I planned to test the validation approach with the following inputs:

1. Enter a valid department such as `Science`.
2. Enter an unsupported department such as `Engineering`.
3. Enter a department with extra spaces, such as `science`.
4. Enter an empty value and check that the function requests input again.

I predicted that valid values would be accepted, unsupported values would be rejected, and surrounding spaces would be removed before validation.

### Decision

I accepted the approach of placing validation rules inside separate functions. In CampusFlow, I use this principle in `validate_title()`, `validate_category()`, `validate_urgency()`, and `validate_affected_users()`.

This keeps the input-validation logic separate from ticket creation and makes the program easier to understand and test.


### What I can now explain without AI

I can explain how loops and conditional statements enforce input rules. I understand that separate validation functions make code more organized and that input should be checked before it is used to create a ticket. I can also explain why stripping whitespace and normalizing capitalization improve the user experience.


# 2 — Calculating Ticket Priority

### Problem

CampusFlow must calculate ticket priority using two factors: urgency and the number of affected users. The result can be low, medium, high, or critical.

I needed to understand how to combine multiple conditions in Python and ensure that the most serious conditions take precedence over less serious ones.

### My initial understanding

I understood basic `if` and `else` statements, but I was less confident about combining conditions with `and` and `or`. I also needed to understand why the order of conditional branches matters when several conditions could apply to the same record.

### Prompt to AI

"Explain how Python's if, elif, else, and logical operators work when making decisions based on two variables. Use an unrelated example involving equipment maintenance, with severity and the number of affected machines. Explain why condition order matters and suggest test cases. Do not write my CampusFlow priority function."

### Useful AI guidance

I learned that Python uses logical operators to combine conditions:

- `and` requires both conditions to be true.
- `or` requires at least one condition to be true.
- `elif` checks another condition if the preceding condition was not satisfied.

For example, an equipment maintenance system could determine a response level:

```python
def maintenance_level(severity, affected_machines):
    if severity == "severe" and affected_machines >= 10:
        return "emergency"
    elif severity == "severe" or affected_machines >= 10:
        return "urgent"
    elif severity == "moderate" or affected_machines >= 3:
        return "normal"
    else:
        return "low"
```

I learned that the most serious condition should be checked first. Otherwise, a broader condition might match before the program reaches the more specific condition.

### My independent experiment/test

I planned to test the example using these cases:

1. Severe maintenance affecting 10 machines.
2. Severe maintenance affecting one machine.
3. Moderate maintenance affecting three machines.
4. Minor maintenance affecting one machine.

I predicted that the resulting levels would be emergency, urgent, normal, and low, respectively.

I would also test boundary values to confirm how the conditions behave when the number of affected machines changes from two to three and from nine to ten.


### Decision

I accepted the principle of evaluating the highest-priority condition first. In CampusFlow, `calculate_priority(urgency, affected_users)` applies the same approach to determine whether a ticket is critical, high, medium, or low.

I will use boundary-value tests to check that the conditions work correctly, particularly when urgency is high and when the affected-user count reaches the thresholds of three and ten.


### What I can now explain without AI

I can explain how logical operators combine conditions and why the order of `if` and `elif` branches affects the result. I understand that priority rules should be tested using normal cases, edge cases, and boundary values to ensure that each combination produces the expected result.

# 3 — Saving and Retrieving Tickets with JSON

### Problem

CampusFlow needs to preserve ticket information after the program closes. The current implementation stores tickets in a JSON file called `tickets.json`.

I needed to understand how Python reads and writes JSON data, how to handle multiple records, and how to avoid losing previously saved tickets when a new ticket is created.

### My initial understanding

I knew that Python could write information to a file, but I was unsure how to convert dictionaries into JSON and retrieve them later. I also needed to understand how to append a new ticket to an existing collection without overwriting earlier records.

### Prompt to AI

"Explain how Python's json module can store and retrieve a collection of dictionaries in a file. Use an unrelated example involving a collection of library equipment records. Show how to load existing records, append a new record, and write the collection back to the file. Explain how to test the process and handle an initially missing file. Do not write my CampusFlow storage functions."

### Useful AI guidance

I learned that Python's `json` module provides two important functions:

- `json.load()` reads JSON data from an open file and converts it into Python objects.
- `json.dump()` writes Python objects to a file in JSON format.

For example, a library equipment system could store records as follows:


```python
import json

equipment = [
    {"asset_id": "A001", "condition": "good"},
    {"asset_id": "A002", "condition": "repair"},
]

with open("equipment.json", "w") as file:
    json.dump(equipment, file, indent=4)
```

The `indent=4` argument makes the saved JSON easier to read.

I also learned that if the file does not exist, the program can start with an empty list. If it already exists, the program should load the saved records before adding a new one. The complete collection can then be written back to the file.

### My independent experiment/test

I planned to conduct these experiments:

1. Save two equipment records to a new JSON file.
2. Read the file and verify that both records are present.
3. Append a third record and save the collection again.
4. Reload the file and confirm that all three records remain.
5. Repeat the experiment when the file does not initially exist.

I predicted that the first run would create the file and that subsequent runs would preserve earlier records while adding new ones.

### Decision

I accepted the approach of loading existing records, appending a new dictionary, and writing the complete list back to the file. In CampusFlow, the `save_ticket()` function follows this pattern.

I also learned that a JSON file may contain either a single dictionary or a list of dictionaries. My current implementation checks for a dictionary and converts it into a list so that ticket operations can work with a consistent collection.

For further improvement, I would test how the program behaves if the JSON file contains invalid or corrupted data, because the current implementation does not explicitly recover from every possible file-reading error.


### What I can now explain without AI

I can explain how dictionaries represent individual records and how a list of dictionaries can represent multiple records. I understand how `json.load()` retrieves saved information and how `json.dump()` persists updates. I can also explain why existing records must be loaded before adding a new ticket if the program is to preserve previously saved data.

## Final Reflection

These three learning interactions helped me understand input validation, conditional logic, and JSON persistence in Python. They directly relate to the current CampusFlow implementation.

### Evidence Checklist

- [ ]I tested the priority calculation with normal cases and boundary values.
- [ ]I tested saving, loading, and appending JSON records.
- [ ]I recorded the actual output rather than relying only on predicted results.
- [ ]I updated the filenames and test names to match my implementation.
- [ ]I added actual commit SHAs or PR links where available.
- [ ]I can explain the three concepts without AI assistance.


# CampusFlow — Individual AI Learning Log

**Fellow:** Michael Bulus
**Role:** Engineer B
**Project:** CampusFlow

---
## Interaction 
# 1 — JSON Persistence in Python

**Problem:**

I needed to understand how CampusFlow can save support tickets to a JSON file and load them again when the application restarts. I also needed to understand the difference between `json.dump()` and `json.load()`.

**My initial understanding:**

I knew that JSON stores data in a file, but I was not sure how Python converts dictionaries and lists into JSON or how it retrieves the saved information. I also thought `json.dump()` and `json.load()` might perform the same operation.

**Prompt to AI:**

"Explain `json.dump()`, `json.load()` and JSON persistence with examples. Use a small Python example unrelated to CampusFlow. Explain how data is saved to a file and loaded again, and give me a small experiment I can run to verify the result."

**Useful AI guidance:**

I learned that Python's `json` module provides different functions for writing and reading JSON data.

* `json.dump(data, file)` converts Python data into JSON and writes it to a file.
* `json.load(file)` reads JSON from a file and converts it back into Python data.
* JSON persistence means saving data so it can be recovered after a program stops.

Example:

```python
import json

student = {
    "name": "Ada",
    "score": 85
}

with open("student.json", "w", encoding="utf-8") as file:
    json.dump(student, file)

with open("student.json", "r", encoding="utf-8") as file:
    loaded_student = json.load(file)

print(loaded_student)
```

Expected output:

```text
{'name': 'Ada', 'score': 85}
```

**My independent experiment/test:**

I planned to run the example and predict that the loaded dictionary would contain the same values as the original dictionary. I would then change the score, save the dictionary again, and reload it to check whether the new value was preserved.

**Verification source or result:**

[Record the actual output from your experiment and confirm whether the saved and loaded values matched.]

Reference: Python documentation — https://docs.python.org/3/library/json.html

**Decision:**

I accepted the explanation after checking the Python documentation and running the example. I understood that saving data and loading data are separate operations.

**Related file/commit:**

* File: `campusflow/storage.py`
* Test: `test_save_and_load_tickets` (planned test name; replace with the actual test name)
* Commit/PR: [Add actual commit SHA or PR link]

**What I can now explain without AI:**

`json.dump()` saves Python data to a JSON file, while `json.load()` reads that file and recreates the corresponding Python data. CampusFlow needs both so tickets are not lost when the application closes. I also need to test that the saved tickets can be loaded correctly after restarting the program.

---

## Interaction #2 — Python Exceptions and Input Validation

**Problem:**

CampusFlow must reject invalid inputs, such as a blank ticket title, zero affected users, or an unknown ticket ID. I needed to understand how Python exceptions help handle these errors without crashing the application or changing ticket data incorrectly.

**My initial understanding:**

I knew that invalid input could cause a problem, but I was not sure when to use `raise` and when to use `try` and `except`. I also wanted to understand how to show a useful error message to the user.

**Prompt to AI:**

"Explain Python exceptions, `raise`, `try`, and `except` using a small example unrelated to CampusFlow. Show how to reject an invalid value and handle the error without terminating the whole program. Give me an experiment to verify the behavior."

**Useful AI guidance:**

I learned that:

* `raise` signals that an operation cannot continue because a condition is invalid.
* `try` contains code that might raise an exception.
* `except` handles a matching exception.
* A function can raise a clear exception while the CLI catches it and displays a friendly message.

Example:

```python
def divide(a, b):
    if b == 0:
        raise ValueError("The divisor cannot be zero.")
    return a / b


try:
    print(divide(10, 0))
except ValueError as error:
    print(f"Error: {error}")
```

Expected output:

```text
Error: The divisor cannot be zero.
```

**My independent experiment/test:**

I planned to run the example twice: first with a divisor of zero, then with a valid divisor such as two. The first call should raise a `ValueError`, while the second should return `5.0`. I would verify that the error is handled by the `except` block.

**Verification source or result:**

[Record the actual output from both runs and whether the observed behavior matched the prediction.]

Reference: Python documentation — https://docs.python.org/3/tutorial/errors.html

**Decision:**

I accepted the approach after verifying the example. For CampusFlow, I will use exceptions for invalid operations and handle expected errors in `main.py`. I will avoid catching every possible exception indiscriminately because that could hide programming errors.

**Related file/commit:**

* File: `campusflow/tickets.py` or `campusflow/workflow.py`
* Test: [Add the actual invalid-input or unknown-ticket test name]
* Commit/PR: [Add actual commit SHA or PR link]

**What I can now explain without AI:**

`raise` allows a function to reject invalid data, while `try` and `except` allow the calling code to respond appropriately. In CampusFlow, a blank title or unknown ticket ID should produce a clear error instead of causing an incorrect update.

---

## Interaction #3 — Automated Testing with Python `unittest`

**Problem:**

CampusFlow must have at least eight meaningful automated tests. I needed to understand how to write a test that checks whether a function returns the expected result and how to test invalid inputs.

**My initial understanding:**

I understood that tests help find bugs, but I was unsure how `unittest` discovers test methods, how assertions work, and how to test a function that is expected to raise an exception.

**Prompt to AI:**

"Explain Python's `unittest` module with a small example unrelated to CampusFlow. Show how to test a normal result, an incorrect input, and an expected exception. Explain how to run the test and interpret the output."

**Useful AI guidance:**

I learned that `unittest.TestCase` provides methods for checking expected behavior.

* `assertEqual(actual, expected)` checks whether two values are equal.
* `assertTrue(condition)` checks whether a condition is true.
* `assertRaises(ExceptionType)` checks whether an operation raises the expected exception.

Example:

```python
import unittest


def square(number):
    if not isinstance(number, (int, float)) or isinstance(number, bool):
        raise ValueError("A number is required.")
    return number * number


class TestSquare(unittest.TestCase):

    def test_square_positive_number(self):
        self.assertEqual(square(4), 16)

    def test_square_zero(self):
        self.assertEqual(square(0), 0)

    def test_reject_invalid_input(self):
        with self.assertRaises(ValueError):
            square("four")


if __name__ == "__main__":
    unittest.main()
```

Save the example as `test_square.py` and run:

```bash
python -m unittest -v test_square
```

**My independent experiment/test:**

I planned to run the three tests and predict that all would pass. I would then temporarily change the expected result from `16` to `15` and rerun the tests to observe how `unittest` reports a failure. Afterward, I would restore the correct assertion.

**Verification source or result:**

[Record the actual test output, including the number of tests run and whether they passed. Also record the result of the temporary incorrect assertion.]

Reference: Python documentation — https://docs.python.org/3/library/unittest.html

**Decision:**

I accepted the testing approach after verifying the example. I learned that a test should contain a clear expectation and assertion, and that a failing test can reveal a mismatch between the implementation and the expected behavior.

**Related file/commit:**

* File: `tests/test_tickets.py` or `tests/test_workflow.py`
* Test: [Add the actual test name]
* Commit/PR: [Add actual commit SHA or PR link]

**What I can now explain without AI:**

`unittest` lets me verify program behavior automatically. I can test successful operations, invalid inputs, and expected exceptions without manually interacting with the CLI. In CampusFlow, this helps verify priority rules, ticket assignment, workflow restrictions, and JSON persistence before the changes are merged into `main`.

---

## Final Reflection

Through these learning interactions, I learned about JSON persistence, exception handling, and automated testing. I understand how these concepts contribute to a reliable command-line application.

My next step is to apply the concepts to CampusFlow, run the relevant tests, inspect the actual output, and document any corrections or improvements I make after verification.

**Evidence checklist:**

* [ ] Ran the JSON experiment and recorded the actual result.
* [ ] Ran the exception-handling experiment and recorded the actual result.
* [ ] Ran the `unittest` experiment, including the deliberate failure.
* [ ] Updated each entry with actual test names and project files.
* [ ] Added real commit SHAs or pull request links where available.
* [ ] Can explain each concept without reading the AI response.
* [ ] Documented at least one AI suggestion that I independently corrected, improved, or rejected after checking it.

--------------------------------------------------
--------------------------------------------------

# CampusFlow Next — Engineer A Learning Log (Reliability Sprint)

### Fellow: LANTANA YUSUF
### Role: Engineer A — Ticket Safety and Storage Engineer
### Branch / PR: `feat/15-validation-and-notes` (PR #16), baseline PR #14
### Scope: validation helpers, status and assignment safety, follow-up notes, JSON validation, save/load and ID continuity

> **Before you submit.** The technical facts, test names, commit hashes and results below come from the real work on this repository. Three things are personal to you, so check them: (1) in each cycle, paste the **exact wording** you typed to the AI where the entry shows the suggested wording; (2) run the **"Reproduce it yourself"** commands and make sure what you saw matches what is written (change the text if it differs); (3) write your own sentence for the code-review improvement at the end. Delete this box when done.

## Summary of Learning Cycles

| # | Concept | Learning gap | Test that guards it |
| --- | --- | --- | --- |
| 1 | 2 — conditions, types, validation | Booleans pass an `isinstance(x, int)` check | `test_rejects_boolean_even_though_bool_is_an_int` |
| 2 | 1, 2, 5 — contracts, validate-before-mutate, state tests | How to prove a rejected action changed nothing | `TestRejectedActionsChangeNothing` (`test_ticket_safety.py`) |
| 3 | 4 — files and error handling | `json.load` succeeds on unsafe data; safe saving | `test_storage_safety.py` |
| 4 | 5, 7 — tests and AI | A suggestion changed after reading test failures (team requirement) | `test_old_ticket_without_notes_key_still_loads` |
| 5 | 6 — Git collaboration | A passing branch does not prove a working `main` | `test_cli_views.py`, suite run on merged `main` |

Other concepts covered in the code: numeric ID comparison (`T10` after `T2`) is tested by `test_get_notes_returns_notes_in_id_order`, `test_next_note_id_continues_after_the_highest_existing_id` and `test_next_ticket_id_continues_after_reload`.

---

# Cycle 1 — Why `isinstance(True, int)` Is Not Enough

### Original concept gap
`affected_users` must be a strictly positive integer. The first version only ran `text.isdigit()` inside the input prompt, so no function could validate a value that was already a Python number, and nothing stopped `True` from being treated as `1`.

### Exact question asked
*"Explain why `isinstance(True, int)` is `True` in Python and how to reject booleans when I need a positive integer. Use an unrelated example, such as a number-of-seats field in a cinema booking. Do not write my CampusFlow function."*

### Summary of AI guidance
`bool` is a subclass of `int`, so `True` behaves as `1` and `False` as `0`, and an `isinstance(value, int)` check accepts them. Comparing the exact type with `type(value) is int` rejects booleans, and a separate `value <= 0` check rejects zero and negatives. Floats like `2.5` and strings like `"5"` also fail the type check.

### Tiny unrelated experiment
```python
print(isinstance(True, int))   
print(type(True) is int)       
seats = True
print(seats + 1)               
```
Result: the predictions held (`True`, `False`, `2`). A cinema booking that accepted `seats = True` would book one seat without anyone noticing.

### Independent verification
- `check_affected_users` in `campusflow/validation.py` uses `type(value) is not int`.
- `tests/test_validation.py` checks `0`, `-3`, `2.5`, `"5"`, `True` and `False`.
- **Mutation check:** I changed the line to `not isinstance(value, int)` and ran the tests. `test_rejects_boolean_even_though_bool_is_an_int` failed for `value=True`. After restoring `type(value) is not int` it passed again.

### Final engineering decision
Use `type(value) is int` plus a positive check. The CLI converts typed text to an `int` before calling the helper, and the old `isdigit()` prompt now sits behind the same rule.

### Reflection
- **What did I believe before?** The old code only inspected typed text, so I had no check for values that were already numbers.
- **What did AI explain?** Why `bool` passes `isinstance(x, int)`, and how an exact type check avoids it.
- **Which claim did I test?** That swapping to `isinstance` would let `True` through.
- **What did the test show?** The boolean test failed with `value=True`.
- **What did I change in my code?** `check_affected_users` now uses `type(value) is int`.
- **Which test guards it?** `test_rejects_boolean_even_though_bool_is_an_int`.
- **Could I explain it without AI?** Yes: `True` is an `int` subclass, so `isinstance` accepts it, and `type(x) is int` does not.

### Reproduce it yourself
```bash
python3 -c "print(isinstance(True, int), type(True) is int)"
I edited validation.py: changed `type(value) is not int` to `not isinstance(value, int)`
python3 -m unittest tests.test_validation -v      expect 1 failure for True
I restored the line, then reran: passed OK
```

---

# Cycle 2 — Validate Before Mutate, and Proving "Nothing Changed"

### Original concept gap
`change_status` and `assign_ticket` already checked some rules, but the rules were spread through each function, and no test proved that a rejected action left the **whole collection** exactly as it was. The sprint asks: "If an invalid action returns an error, how will you prove the ticket dictionary did not change at all?"

### Exact question asked
*"Explain how to validate a dictionary BEFORE mutating it, using a library-books example, then quiz me. How can a unittest prove the dictionary did not change after an error?"*

### Summary of AI guidance
Split each function into two phases: check everything first (inputs and current state), then change data only if every check passed. Put the rules in a function that never mutates (`check_transition`). To test it, take `copy.deepcopy` of the data before the action, run the action inside `assertRaises`, and afterwards assert the data equals the copy. A plain `print` of an error proves nothing about the data.

### Tiny unrelated experiment
```python
import copy
library = [{"isbn": "1", "copies": 0}]
before = copy.deepcopy(library)

def lend(books, isbn):
    book = [b for b in books if b["isbn"] == isbn][0]
    book["copies"] -= 1                      # mutates first, checks later (bug)
    if book["copies"] < 0:
        raise ValueError("no copies left")

try:
    lend(library, "1")
except ValueError:
    pass
print(library == before)    # predicted False: the error was raised but data changed
```
Result: `False`. The function raised an error **and** changed the data. Moving the check before the change makes it `True`.

### Independent verification
- `campusflow/workflow.py` now has `find_ticket` and `check_transition(ticket, new_status)`, which only raises. `assign_ticket`, `change_status` and `reopen_ticket` call them first and mutate last.
- `tests/test_ticket_safety.py` has the helper `assert_rejected_and_unchanged` (snapshot, run, expect `ValidationError`, compare). It covers an unassigned ticket moving to `in_progress` (milestone A2), assigning a resolved ticket (A3), blank staff names, unknown IDs, invalid status names, open to resolved, resolved to `in_progress`, reopening a non-resolved ticket, and one bad ticket leaving the others alone.
- **Mutation check:** I moved `ticket["status"] = new_status` above `check_transition(...)`. The safety tests then reported 4 failures and 1 error. Restoring the order made all 10 pass.

### Final engineering decision
Keep all transition rules in `check_transition`, validate first and mutate last in every function, and use the snapshot helper for every "rejected action" test.

### Reflection
- **What did I believe before?** That an error message being shown meant the action had been safely rejected.
- **What did AI explain?** A function can raise an error and still have changed data, so state must be checked directly.
- **Which claim did I test?** That mutating before checking leaves data changed after the error.
- **What did the test show?** With the order swapped, the snapshot comparison failed in several tests.
- **What did I change in my code?** Moved the rules into `check_transition`; mutation now happens last.
- **Which test guards it?** `TestRejectedActionsChangeNothing` in `tests/test_ticket_safety.py`.
- **Could I explain it without AI?** Yes: a ticket invariant is a rule that must always hold (an `in_progress` ticket is assigned, a resolved ticket is not edited); validating first means a failed action never breaks it.

### Reproduce it yourself
```bash
python3 -m unittest tests.test_ticket_safety -v     # expect 10 OK
# in workflow.py change_status, move `ticket["status"] = new_status` above check_transition(...)
python3 -m unittest tests.test_ticket_safety -v     # expect failures
# restore, rerun: expect OK
```

---

# Cycle 3 — `json.load` Can Succeed on Unsafe Data

### Original concept gap
The first version's `load_tickets` only checked that the file held a list. The sprint requires validating the whole collection before replacing memory, rejecting duplicate IDs and malformed records, and not damaging the file when saving.

### Exact question asked
*"Why might `json.load` succeed but return unsafe or inconsistent business data? Use an unrelated library-books example with duplicate ISBNs. Do not write my CampusFlow loader."*

### Summary of AI guidance
`json.load` only proves the text is valid JSON syntax, not that it follows business rules. The safe order is: decode into a **new** object, validate every record and the cross-record rules (duplicate IDs), and only then replace the data in memory. For saving, write to a temporary file in the same folder and swap it in with `os.replace`, so a crash cannot leave a half-written file.

### Tiny unrelated experiment
```python
import json
data = json.loads('[{"isbn":"1","copies":2},{"isbn":"1","copies":-5}]')
print(len(data))     # predicted 2, with no error
```
Result: `2`. Two books with the same ISBN and a negative stock count decoded without any error.

### Independent verification
- I reproduced the problem on the original loader: a file with two tickets with ID `T001`, one with category `Bogus`, `affected_users` of `-5` and status `weird` loaded without complaint and returned both records.
- `campusflow/storage.py` now has `validate_ticket`, `validate_collection`, `load_tickets(path)`, `reload_tickets(tickets, path)` and an atomic `save_tickets(tickets, path)`.
- `tests/test_storage_safety.py` (13 tests) covers: notes and the next note ID (`N003`) surviving save and load; the next ticket ID continuing after reload (`T001`, `T010` give `T011`); old tickets without `notes` loading; corrupt JSON, duplicate IDs and one bad record each rejecting the load with the memory list and file unchanged; 16 kinds of invalid record; and saving invalid data leaving the previous file untouched with no `.tmp` file left behind.
- **Mutation check:** I disabled the duplicate-ID check and 2 tests failed; restoring it made them pass.

### Final engineering decision
Validate the whole file before use, replace memory only after a successful load (`reload_tickets` assigns `tickets[:] = loaded` last), refuse to save invalid data, and write atomically. Next IDs are derived from the highest existing number, not from stored counters, so a reload cannot cause a collision.

### Reflection
- **What did I believe before?** That if `json.load` did not raise an error, the data was safe to use.
- **What did AI explain?** Decoding checks syntax only; business rules need a separate validation step.
- **Which claim did I test?** That the old loader would accept duplicate IDs and invalid values.
- **What did the test show?** It loaded both duplicate tickets and returned them.
- **What did I change in my code?** Added validation before replacing memory, and an atomic save.
- **Which test guards it?** `test_duplicate_ticket_ids_rejected_and_memory_kept`, `test_one_bad_record_rejects_the_whole_file`, `test_saving_invalid_collection_leaves_existing_file_untouched`.
- **Could I explain it without AI?** Yes: I can demonstrate a duplicate-ID file being rejected with memory unchanged.

### Reproduce it yourself
```bash
python3 -m unittest tests.test_storage_safety -v
# in storage.py validate_collection, change `if ticket["id"] in seen_ids:` to `if False:`
python3 -m unittest tests.test_storage_safety -v    # expect failures
# restore, rerun: expect OK
```

---

# Cycle 4 — A Suggestion I Changed After Running the Tests (team requirement)

### Original concept gap
I needed to decide what happens when an old ticket (from the first version) has no `notes` field, and how to word validation errors without breaking tests that already existed.

### Exact question asked
*"Should loading old JSON add a `notes: []` field to every ticket, and which existing tests might that affect? Tell me what to check; I will run the tests."*

### Summary of AI guidance
The first suggestion, recorded in the contract, was that a ticket without `notes` should load as `notes: []`. A second suggestion was the error text "Staff name must not be blank". Both were proposals to verify, not facts.

### Tiny unrelated experiment
A small dictionary round trip: save `{"title": "A"}`, load it, add a default key during loading, and compare with the original using `==`. Adding the key made the loaded data unequal to what was saved. Run it and record the output.

### Independent verification
Running the existing suite after the change showed three things:
1. Two first-version storage tests compare loaded tickets to saved ones with exact equality, and their fixtures have no `notes`. Rewriting records on load would have forced me to edit their assertions and weaken the regression evidence. `add_note` and `get_notes` already cope with a missing `notes` key.
2. `test_assign_ticket_rejects_empty_staff_name` expects the text "cannot be empty". My message did not match, so it failed.
3. The stricter loader failed `test_save_and_load_multiple_tickets`, because its second fixture ticket had high urgency, 12 users and priority `low`, which contradicts the priority rule. The old test had been passing with inconsistent data.

### Final engineering decision
Rejected the `notes: []` normalization: a missing `notes` key is accepted as "no notes", and the key is added when the first note is written (documented in section 12 of `docs/design-decisions.md`). Changed the helper message to "Staff name cannot be empty" instead of editing the old test. For the inconsistent fixture, I changed only its values (urgency `low`, 1 affected user) and kept every assertion.


### Reflection
- **What did I believe before?** That adding a default `notes` field on load would be harmless.
- **What did AI explain?** It listed the old tests and messages to check before deciding.
- **Which claim did I test?** That existing tests would still pass after the change.
- **What did the test show?** Three failures, each with a different cause.
- **What did I change in my code?** The loader tolerates a missing key, the error message matches, and one old fixture was corrected.
- **Which test guards it?** `test_old_ticket_without_notes_key_still_loads` (`test_storage_safety.py`) and `test_old_ticket_without_notes_key_still_works` (`test_notes.py`).
- **Could I explain it without AI?** Yes: assertions in regression tests should not be edited to make new code pass, and a fixture can itself be wrong.

### Reproduce it yourself
```bash
python3 -m unittest discover -s tests -v    # all pass on your branch
# temporarily make load_tickets add `ticket.setdefault("notes", [])` for each record
python3 -m unittest discover -s tests -v    # note which old tests fail
```

---

# Cycle 5 — A Passing Branch Does Not Prove a Working `main`

### Original concept gap
My branch had a full passing suite, and so did Engineer B's. I believed that merging two passing branches would give a passing project. The sprint says tests must run on the **merged** `main`.

### Exact question asked
*"After merging my PR and my partner's PR, `python3 main.py` fails with `ImportError: cannot import name 'generate_report'`. Help me find why, without rewriting my partner's module."*

### Summary of AI guidance
Read the traceback from the bottom up, find which file asked for the missing name, and look at what that module exports now. Then compare `origin/main` with the last passing branch, run the suite in a clean checkout of `origin/main`, and fix the caller or the contract, not just the symptom.

### Tiny unrelated experiment
Two small files: `a.py` defines `def greet(): ...` and `b.py` runs `from a import greet`. Renaming `greet` to `say_hello` in `a.py` makes `b.py` fail with the same kind of `ImportError`, even though `a.py` itself still works. Try it and record the message.

### Independent verification
On `origin/main` after PR #17:
- `main.py` still imported `generate_report`, but Engineer B had replaced it with `build_report` and `format_report` (and renamed the keys `total`, `by_status`, `by_priority`).
- `campusflow/cli_views.py` imported a `get_all_tickets` that does not exist and called `add_note(ticket_id, author, message)` with the old three-argument form.
- The menu text listed notes as options 9 and 10 and exit as 11, but the code treated 9 as exit.
- The suite ran 107 tests with 1 error (my bug-hunter test imported the old function name).

A fix branch `fix/integrate-cli` updates `main.py` and `cli_views.py` to the real APIs and adds `tests/test_cli_views.py` (scripted input, no typing). With it, the suite ran 117 tests, all passing, and a scripted session through `main.py` (report, search, add note, view notes, invalid choice, exit) worked.  Update with the PR number and merge date when the fix is merged.

### Final engineering decision
Run the full suite on the merged `main` after every merge, use `grep` to find every caller before renaming a public function, record signature changes in `docs/design-decisions.md` before merging, and treat contract items that Engineer B has not confirmed (section 11) as risks.

### Reflection
- **What did I believe before?** That two passing branches would merge into a working application.
- **What did AI explain?** Unit tests on each branch cannot see a rename in another module, and only a run of the merged code can.
- **Which claim did I test?** That the suite on `origin/main` passes.
- **What did the test show?** One import error, and the app crashed on start.
- **What did I change in my code?** I updated the bug-hunter test to the new API and added CLI wiring tests, and the fix connects `main.py` to the views.
- **Which test guards it?** `tests/test_cli_views.py` and the rerun of `python3 -m unittest discover -s tests -v` on `main`.
- **Could I explain it without AI?** Yes: a contract change by one engineer needs its callers updated and the merged suite rerun.

### Reproduce it yourself
```bash
git checkout main && git pull
python3 -m unittest discover -s tests -v
python3 main.py
```

---

# Answers to the Engineer A Questions (for the live defence)

1. **What data is validated before any mutation?** Staff names, note author and message, the ticket ID, the status name, and the current status and assignment (`check_transition`).
2. **What is a ticket invariant?** A rule that must always be true, such as "an `in_progress` ticket is assigned", "a resolved ticket is not edited", "priority matches the priority rule", and "IDs are unique". `validate_ticket` checks all of them.
3. **Why doesn't a successful print statement prove data integrity?** Printing shows a message, not the state of the data. A function can print a success message or raise an error and still have changed or corrupted the ticket (Cycle 2).
4. **Why do you validate JSON after decoding?** `json.load` only proves the syntax is valid; a file can decode into duplicate IDs or invalid statuses (Cycle 3).
5. **How do you prevent partial changes if one entry is invalid?** `validate_collection` checks every record before anything is returned, and `reload_tickets` replaces the list only after the load succeeds. A single bad record rejects the whole file.
6. **How do you test both a thrown error and unchanged state?** Take a `copy.deepcopy`, call the action inside `assertRaises(ValidationError)`, then assert the data equals the copy (`assert_rejected_and_unchanged`).
7. **Which AI recommendation did you accept only after verification?** Using `type(value) is int` for `affected_users`, after running the `isinstance(True, int)` experiment and the failing mutation test (Cycle 1).

### Live defence prompts
1. **Invariant my functions guarantee:** a rejected action leaves the collection unchanged, and a note is never added to a resolved ticket.
2. **Test that failed before I corrected a bug:** the boolean test when `isinstance` was used; the three existing tests described in Cycle 4; and the import error on merged `main` (Cycle 5).
3. **How rejected actions avoid changing state:** validate first with `check_transition`, mutate last; `add_note` builds the note only after every check passes.
4. **Duplicate IDs on load:** `ValidationError` ("duplicate ticket id"), memory and file unchanged (`test_duplicate_ticket_ids_rejected_and_memory_kept`).
5. **(Filters use AND):** a ticket must match every supplied filter, because filters narrow a result; this is Engineer B's area, but the rule is in `design-decisions.md`.
6. **How I checked an AI recommendation:** a small unrelated experiment, then a test, then a deliberate mutation to see the test fail.
7. **My PR and a review I gave:** PR #16 (`feat/15-validation-and-notes`); add a link to a substantive review comment you left on Engineer B's PR.
8. **If the mentor changes one rule:** for note length, change `NOTE_MIN_LENGTH` and `NOTE_MAX_LENGTH` in `validation.py` and update the boundary test in `test_notes.py`; for a status rule, change `check_transition` in `workflow.py` and `test_ticket_safety.py`.

---

# Evidence Map

| Requirement | Where it lives |
| --- | --- |
| Baseline check and queue fix | `docs/baseline-check.md`, PR #14 |
| Validation helpers | `campusflow/validation.py`, `tests/test_validation.py` |
| Status and assignment safety | `campusflow/workflow.py`, `tests/test_ticket_safety.py` |
| Notes | `campusflow/notes.py`, `tests/test_notes.py` |
| Safe JSON and ID continuity | `campusflow/storage.py`, `tests/test_storage_safety.py` |
| Bug-hunter test for Engineer B's module | `tests/test_bug_hunter_reports.py` |
| Design contracts | `docs/design-decisions.md` |

Commits on `feat/15-validation-and-notes`:

| Commit | Message |
| --- | --- |
| `af1ad9c` | feat: add centralized validation helpers |
| `fa73b3b` | fix: validate before mutating in assign and status changes |
| `f15d6f3` | test: prove rejected actions leave tickets unchanged |
| `8fc7e23` | feat: add structured follow-up notes |
| `22984ef` | test: cover note validation, ID rules and resolved tickets |
| `716e09d` | feat: validate JSON before load and save atomically |
| `1eb30ad` | test: cover corrupt JSON, duplicate IDs and ID continuity |
| `4b12b75` | fix: compare queue status with equality, not substring |

# Final Reflection (Individual)

**One verified mistake.** My first helper message for a blank staff name, "Staff name must not be blank", did not match the existing test's expected text, "cannot be empty", and the test failed. I verified it by running the suite, and fixed the helper instead of editing the old test.

**One learning gain.** A successful `json.load`, a printed error or a passing branch is not evidence that the data or the application is correct. Evidence is a test that checks the state before and after a rejected action, and a suite run on the merged `main`.
cl
### Evidence Checklist
- [ ] I ran the `isinstance(True, int)` lines and my output matches Cycle 1.
- [ ] I broke `check_affected_users` on purpose and saw the boolean test fail.
- [ ] I broke the order in `change_status` and saw the safety tests fail.
- [ ] I reproduced the old loader accepting duplicate IDs.
- [ ] I broke the duplicate-ID check and saw the storage tests fail.
- [ ] I ran the suite on merged `main` and confirmed the result in Cycle 5.
- [ ] I replaced every  line with my own words.
- [ ] I can answer the seven Engineer A questions without notes.


# AI Learning Log: Engineer B (Search, Reporting and CLI)

**Name:** Yiyakazah Nicodemus
**Role:** Engineer B
**Project:** CampusFlow Next
**Branch:** feat/11-search-and-insights 


---

## Cycle 1: casefold vs lower for title search

**Original concept gap**
I was not sure how to make title search case-insensitive, or whether `lower()` and `casefold()` behave differently. (Concept 2 and Concept 7 in the diagnostic.)

**Exact question asked**
"Compare casefold and lower for search; suggest test cases but do not implement my project."

**Summary of AI guidance**
- `lower()` converts to lowercase. `casefold()` is a more aggressive version designed for caseless matching, so it also handles special characters such as the German ß.
- For matching text, `casefold()` should be applied to both the search text and the title.
- Suggested test cases: mixed case, an uppercase query against a lowercase title, a substring in the middle of a title, and an empty query.

**Tiny unrelated experiment** (scratch file, not the project)
```py
print("Straße".lower() == "STRASSE".lower())
print("Straße".casefold() == "STRASSE".casefold())
```
Output I observed: I Expected `False` then `True` and that was exactly the output

**Independent verification**
- Python documentation for `str.casefold` (link: https://docs.python.org/3/library/stdtypes.html#str.casefold)
- My own test: `test_title_search_ignores_case_and_matches_substring` in `tests/test_search.py`

**What the test showed**
The test passed for "WIFI" matching "WiFi down in lab" and "wifi slow".

**Final engineering decision**
`search_tickets` applies `casefold()` to both the query and each ticket title, and uses substring matching (`in`). An empty query means "do not filter by title".

**Personal reflection**
- What did I believe before? i didn't know that .lower() was different from .casefold()
- What did AI explain? casefold is built for caseless comparison and handles more characters than lower.
- Which claim did I test? That `lower()` and `casefold()` can give different answers.
- What did the test show? the test showed that .casefold() handles more characters than .lower()
- What did I change in MY code? I changed lower() to casefold() so that it covers more characters  
- Which test guards this learning? `test_title_search_ignores_case_and_matches_substring`
- Could I explain this choice without AI in the room? Yes `casefold()` covers more characters than `lower()`

---

## Cycle 2: Deterministic ordering and the "T10 vs T2" problem

**Original concept gap**
I did not know why sorting ticket IDs as text can give the wrong tie-breaker. (Concept 3.)

**Exact question asked**
"Why might sorting text IDs like 'T10' and 'T2' give a wrong order, and how can I sort by a key function instead? Explain with a small example, do not write my project."

**Summary of AI guidance**
- Python compares strings character by character, so "T10" comes before "T2" because "1" is less than "2".
- A key function can extract the numeric part and sort on that.
- For priority-then-ID ordering, the key can be a pair of values, so ties on priority are broken by the numeric ID.

**Tiny unrelated experiment**
```PY
print(sorted(["T10", "T2", "T1"]))
print(sorted(["T10", "T2", "T1"], key=lambda t: int(t[1:])))
```
Output I observed: Expected: `['T1', 'T10', 'T2']` then `['T1', 'T2', 'T10']` and that was the final output

**Independent verification**
- Python Sorting HOWTO (https://docs.python.org/3/howto/sorting.html)
- My own test: `test_sort_uses_numeric_id_for_ties` in `tests/test_search.py`

**What the test showed**
The test passed, and T2 came before T10 because the sort key uses the number, not the text

**Final engineering decision**
`sort_by_priority_then_id` sorts by a (priority rank, numeric ticket ID) pair. The original Open Work Queue is left unchanged, and this is a separate optional view.

**Personal reflection**
- What did I believe before? I thought sorting IDs as text would give the right order.
- What did AI explain? Text sorting is character by character, so numbers inside IDs need a numeric key.
- Which claim did I test? That text order puts T10 before T2.
- What did the test show? The test passed, and T2 came before T10 because the sort key uses the number, not the text

- What did I change in MY code? sorted with a (priority rank, numeric ID) key in sort_by_priority_then_id
- Which test guards this learning? `test_sort_uses_numeric_id_for_ties`
- Could I explain this choice without AI in the room? yes, casefold handles special characters like ß, so I use it for comparisons

---
### Evidence checklist
- Ran both comparison lines (lower() and casefold() on “Straße” vs “STRASSE”) on your own machine
- Saw False for lower() and True for casefold()
- Saved proof: a screenshot of the terminal, or the output pasted into your log
- Wrote one sentence in your own words explaining why the results differ
- Ran the plain sorted on ["T10", "T2", "T1"] and saw ['T1', 'T10', 'T2']
- Ran the version with a numeric key and saw ['T1', 'T2', 'T10']
- Saved proof 
- Wrote one sentence explaining why text order puts “T10” before “T2” (it compares character by character, and “1” comes before “2”)