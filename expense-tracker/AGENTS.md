# AGENTS.md

Instructions for AI coding agents working in this repository.

## Purpose
Small Python CLI that records expenses and computes the amount the company
reimburses. Educational project (Software Engineering, Assignment #05).
Contains no real personal or financial data.

## Architecture
- `expense_tracker/calculator.py`: business logic (reimbursement rules, totals, report text). No I/O.
- `expense_tracker/storage.py`: JSON file load/save; raises `StorageError` on corrupt data. Path from `EXPENSE_FILE` (default `expenses.json`).
- `expense_tracker/validation.py`: validates and normalizes amount, date, category from CLI input.
- `expense_tracker/cli.py`, `__main__.py`: command-line entry point (`add`, `report`).
- `tests/`: `unittest` tests for calculator, validation, storage and CLI (24 tests).

Rule: business logic stays in `calculator.py`; the CLI and storage must not contain reimbursement rules.

## Setup
- Python 3.8+ (version in use must be recorded in the baseline report).
- No third-party runtime dependencies. Do not add any without approval.

## Safe commands (allowed without asking)
- `python -m unittest -v`
- `python -m compileall expense_tracker tests`
- `python -m expense_tracker report` (always with `EXPENSE_FILE` pointing to a temp file)
- `git status`, `git diff`, `git log`, `git checkout -b <new-branch>`

## Forbidden actions
- Never read, create or commit secrets, tokens, `.env` files or real personal data.
- No deployment or publishing of any kind (no `pip upload`, no release tags).
- No destructive commands: `rm -rf`, `git push --force`, `git reset --hard`, deleting branches or history.
- No adding, removing or upgrading dependencies without explicit human approval.
- No network downloads or `curl | sh`.
- Do not edit `expenses.json` of a user or commit it (it is git-ignored).
- Do not modify tests to make them pass; fix the code or explain the failure.

## Coding conventions
- PEP 8, type hints for new functions, docstrings for public functions.
- Keep functions small; one change = one purpose.
- Money values must not be silently changed in precision or rounding behavior.

## Test expectations
- Run `python -m unittest -v` before and after every change; report exact totals.
- Every bug fix or new rule needs at least one test.
- If a check was not run, say so explicitly. Never fabricate test output.

## Review gates
- Work on a separate branch; never commit directly to `main`.
- A human reviews the full diff before merge.
- Agent must summarize: files changed, commands run, results, open risks.

## Acceptance criteria (must stay true after any change)
1. `travel` expenses reimburse 90%, `meals` 50%, `office` 100%, any other category 0.
2. `total()` and `total_reimbursable()` return correct sums for a list of expenses.
3. `build_report()` output contains `TOTAL:` and `REIMBURSABLE:` lines with 2 decimals.
4. `python -m expense_tracker add ...` followed by `report` works end to end.
5. All tests pass with `python -m unittest`.
