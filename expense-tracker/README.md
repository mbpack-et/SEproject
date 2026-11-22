# Expense Tracker

Small CLI tool to record expenses and compute the reimbursable amount.

## Requirements
Python 3.8+ (verified on 3.13.2)

## Usage
    python -m expense_tracker add 2026-11-01 travel 120.50
    python -m expense_tracker report

## Tests
    python -m unittest

## Exit codes
- `0` success, `1` invalid input or unreadable data file, `2` wrong usage.
