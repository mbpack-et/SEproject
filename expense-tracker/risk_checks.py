#!/usr/bin/env python3
"""Cross-platform, reproducible risk checks for the expense tracker.

Run from the repository root:
    python risk_checks.py                 # observe and print behaviour
    python risk_checks.py --expect-fixed  # exit code 1 if a mitigated risk still reproduces

Uses a temporary directory (removed automatically) and never touches real data.
"""
import importlib.util
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXPECT_FIXED = "--expect-fixed" in sys.argv
fixed_results = []


def cli(tmp, *args):
    env = {"EXPENSE_FILE": str(Path(tmp) / "e.json")}
    import os
    env = dict(os.environ, **env)
    p = subprocess.run(
        [sys.executable, "-m", "expense_tracker", *args],
        cwd=ROOT, env=env, capture_output=True,
        encoding="utf-8", errors="replace", timeout=30,
    )
    return p.returncode, p.stdout.strip(), p.stderr.strip()


def show(cmd, rc, out, err):
    print("$ python -m expense_tracker " + " ".join(cmd))
    print("  exit code:", rc)
    for label, text in (("stdout", out), ("stderr", err)):
        if text:
            lines = text.splitlines()
            print("  %s: %s" % (label, " | ".join(lines[-3:])))


def no_traceback(err):
    return "Traceback" not in err


def record(hid, title, ok):
    fixed_results.append((hid, title, ok))
    print("  -> %s %s" % (hid, "NOT REPRODUCED (fixed)" if ok else "REPRODUCED (open)"))
    print()


def run_case(hid, title, args, ok_fn, setup=None, then=None):
    print("=== %s %s" % (hid, title))
    with tempfile.TemporaryDirectory() as tmp:
        if setup:
            setup(Path(tmp) / "e.json")
        rc, out, err = cli(tmp, *args)
        show(args, rc, out, err)
        if then:
            rc2, out2, err2 = cli(tmp, *then)
            show(then, rc2, out2, err2)
            record(hid, title, ok_fn(rc, out, err, rc2, out2, err2))
        else:
            record(hid, title, ok_fn(rc, out, err, None, None, None))


run_case("H1", "negative amount accepted", ["add", "2026-11-01", "travel", "-100"],
         lambda rc, o, e, *_: rc != 0 and no_traceback(e))
run_case("H2", "non-numeric amount", ["add", "2026-11-01", "travel", "abc"],
         lambda rc, o, e, *_: rc != 0 and no_traceback(e))
run_case("H3", "category case-sensitivity (Travel)", ["add", "2026-11-01", "Travel", "100"],
         lambda rc, o, e, rc2, o2, e2: "90.00" in (o2 or ""), then=["report"])
run_case("H4", "corrupt JSON storage", ["report"],
         lambda rc, o, e, *_: rc != 0 and no_traceback(e),
         setup=lambda p: p.write_text("{broken", encoding="utf-8"))
run_case("H5", "no arguments", [],
         lambda rc, o, e, *_: rc != 0 and no_traceback(e))
run_case("H6", "README command 'export --csv' (not implemented)", ["export", "--csv"],
         lambda rc, o, e, *_: rc != 0)
run_case("H7", "invalid date accepted", ["add", "not-a-date", "office", "5"],
         lambda rc, o, e, *_: rc != 0)

print("=== H8 float money (informational, not mitigated)")
sys.path.insert(0, str(ROOT))
from expense_tracker import calculator  # noqa: E402
items = [{"date": "d", "category": "office", "amount": 0.1},
         {"date": "d", "category": "office", "amount": 0.2}]
print("  total(0.1 + 0.2) =", repr(calculator.total(items)), "| == 0.3:", calculator.total(items) == 0.3)
with tempfile.TemporaryDirectory() as tmp:
    cli(tmp, "add", "2026-11-01", "office", "2.675")
    rc, out, err = cli(tmp, "report")
    show(["report"], rc, out, err)
print("  half-up money rounding of 2.675 would be 2.68")
print()

print("=== H9 lint/type tools installed (informational)")
for tool in ("ruff", "mypy", "flake8"):
    print("  %-7s %s" % (tool, "installed" if importlib.util.find_spec(tool) else "NOT installed"))
print()

print("=== H10 reproducibility/CI files (informational)")
names = ["pyproject.toml", "requirements.txt", "setup.py", "tox.ini", "Makefile", ".github"]
found = [n for n in names if (ROOT / n).exists()]
print("  found:", ", ".join(found) if found else "none")
print()

print("=== H11 tests touching storage/cli (informational)")
hits = [p.name for p in sorted((ROOT / "tests").glob("test_*.py"))
        if any(w in p.read_text(encoding="utf-8") for w in ("storage", "cli"))]
print("  test files:", ", ".join(hits) if hits else "none")
print()

passed = sum(1 for _, _, ok in fixed_results if ok)
print("SUMMARY: %d/%d mitigated-risk checks not reproduced" % (passed, len(fixed_results)))
for hid, title, ok in fixed_results:
    print("  %-3s %-8s %s" % (hid, "fixed" if ok else "OPEN", title))
if EXPECT_FIXED and passed != len(fixed_results):
    sys.exit(1)
