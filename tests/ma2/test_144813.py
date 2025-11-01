#!/usr/bin/env python3
"""
Python port of the shell test (original: test_144812.sh).

Behavior:
- Run tests/ma2/input_generator.py to produce input_2.txt (created in the CWD: student work dir).
- Feed input_2.txt to the reference (tests/ma2/mainCP.py) and the student (main.py).
- From both outputs:
    * Capture the 4 lines AFTER "Removed the following book from catalog:".
    * Capture the lines BETWEEN "Accessed the following book from catalog:" and the next "Action".
- Compare the "Accessed..." windows for equality; also report the removed-book blocks.
- Write Gradescope-style JSON to ${OUTPUTS_DIR}/144812.json.

Notes:
- PYTHONPATH is set so both reference and student code can import helpers from tests/ma2 if needed.
- Any stderr from ref/student is tailed into the JSON log for easier debugging.
"""

import json
import os
import sys
import subprocess
from pathlib import Path
from typing import Tuple

TEST_ID = "144812"
DEFAULT_TESTS_DIR = Path(__file__).parent  # tests/ma2
OUTPUTS_DIR = Path(os.environ.get("OUTPUTS_DIR", "__outputs__"))
PYTHON_BIN = os.environ.get("PYTHON_BIN", sys.executable)

OUT_JSON = OUTPUTS_DIR / f"{TEST_ID}.json"
# The shell version looked for the input in the current working directory (student work dir),
# and the runner chdirs there. We'll do the same.
INPUT_TXT = Path("input_2.txt")

# Optional stderr tails for debugging
REF_STDERR = OUTPUTS_DIR / f"{TEST_ID}_ref.stderr.txt"
STU_STDERR = OUTPUTS_DIR / f"{TEST_ID}_stu.stderr.txt"


def write_json(passed: bool, logs: str = "") -> None:
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    data = {"id": TEST_ID, "passed": bool(passed), "log": str(logs)}
    OUT_JSON.write_text(json.dumps(data), encoding="utf-8")


def run(cmd, *, env=None, stdin_text: str | None = None,
        capture_stderr_to: Path | None = None) -> Tuple[int, str, str]:
    proc = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE if stdin_text is not None else None,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env,
    )
    out, err = proc.communicate(stdin_text)
    if capture_stderr_to is not None:
        try:
            capture_stderr_to.write_text(err or "", encoding="utf-8")
        except Exception:
            pass
    return proc.returncode, out or "", err or ""


def extract_between_access_and_action(s: str) -> str:
    """
    Extract lines strictly between
      'Accessed the following book from catalog:' and the next 'Action'
    (exclusive). Mirrors the sed block logic from the shell script.
    """
    lines = s.splitlines()
    want = False
    out_lines: list[str] = []
    for ln in lines:
        if "Accessed the following book from catalog:" in ln:
            want = True
            continue
        if want and "Action" in ln:
            break
        if want:
            out_lines.append(ln)
    return "\n".join(out_lines)


def extract_removed_block(s: str, lines_after: int = 4) -> str:
    """
    Find the line with 'Removed the following book from catalog:' and return the
    next `lines_after` lines joined by newline. Error if not found.
    """
    lines = s.splitlines()
    for i, ln in enumerate(lines):
        if "Removed the following book from catalog:" in ln:
            start = i + 1
            end = min(start + lines_after, len(lines))
            return "\n".join(lines[start:end])
    raise ValueError("Remove confirmation not found in output.")


def parse_catalog_and_idx_from_input(input_text: str) -> tuple[str, str]:
    """
    Shell used:
      catalog_num=$(sed -n '3 s/[^0-9]//gp' input_2.txt)
      idx=$(sed -n '5p' input_1.txt)   <-- likely a typo in the shell; use input_2 here.
    We read the file and replicate intent: line 3 digits for catalog, full line 5 for idx.
    """
    lines = input_text.splitlines()
    catalog = ""
    idx = ""
    if len(lines) >= 3:
        catalog = "".join(ch for ch in lines[2] if ch.isdigit())
    if len(lines) >= 5:
        idx = lines[4].strip()
    return catalog, idx


def main():
    try:
        OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
        tests_dir = DEFAULT_TESTS_DIR

        # 1) Run input generator (in tests/ma2). It should create input_2.txt in the CWD (student work dir).
        gen_cmd = [PYTHON_BIN, str(tests_dir / "input_generator.py")]
        rc, gen_out, gen_err = run(gen_cmd, capture_stderr_to=REF_STDERR)
        if rc != 0:
            tail = (gen_err.splitlines()[-60:] if gen_err else [])
            write_json(False, "ERROR: input_generator.py failed to execute properly.\n\nSTDERR (last lines):\n" + "\n".join(tail))
            return

        if not INPUT_TXT.exists() or INPUT_TXT.stat().st_size == 0:
            write_json(False, "ERROR: input_2.txt not found.")
            return

        input_text = INPUT_TXT.read_text(encoding="utf-8", errors="ignore")
        catalog_num, idx = parse_catalog_and_idx_from_input(input_text)

        # 2) Run reference solution
        env = os.environ.copy()
        env["PYTHONPATH"] = f".:{tests_dir}:{env.get('PYTHONPATH','')}"
        ref_cmd = [PYTHON_BIN, str(tests_dir / "mainCP.py")]
        rc, ref_out, ref_err = run(ref_cmd, env=env, stdin_text=input_text, capture_stderr_to=REF_STDERR)
        if rc != 0:
            tail = (ref_err.splitlines()[-60:] if ref_err else [])
            write_json(False, "ERROR: Reference solution (mainCP.py) failed.\n\nSTDERR (last lines):\n" + "\n".join(tail))
            return

        # 3) Run student solution
        stu_cmd = [PYTHON_BIN, "main.py"]
        rc, stu_out, stu_err = run(stu_cmd, env=env, stdin_text=input_text, capture_stderr_to=STU_STDERR)
        if rc != 0:
            tail = (stu_err.splitlines()[-60:] if stu_err else [])
            write_json(False, "ERROR: Student program (main.py) failed.\n\nSTDERR (last lines):\n" + "\n".join(tail))
            return

        # 4) Extract removed-book blocks (4 lines after the marker)
        try:
            removed_book_expected = extract_removed_block(ref_out, lines_after=4)
        except Exception as e:
            write_json(False, f"ERROR: Remove confirmation did not occur in Python solution script. ({e})")
            return

        try:
            removed_book_returned = extract_removed_block(stu_out, lines_after=4)
        except Exception as e:
            write_json(False, f"ERROR: Remove confirmation did not occur in student solution script. ({e})")
            return

        # 5) Extract Accessed-window blocks
        expected_access = extract_between_access_and_action(ref_out)
        returned_access = extract_between_access_and_action(stu_out)

        # 6) Build feedback message (match shell style)
        msg = (
            f"Testing removeFromCatalog({idx}) on catalog {catalog_num}...\n\n"
            f"STUDENT OUTPUT:\n{stu_out}\n"
            "-------------------------------------------\n"
            "FEEDBACK:\n\n"
            "* What this tester did:\n"
            f"      1. Loaded the catalog {catalog_num}\n"
            f"      2. Accessed book at index {idx}\n"
            f"      3. Removed book at index {idx}\n"
            "      4. Confirmed that the book has been removed by accessing the book at "
            f"{idx} again and verifying that the book at that index is different after the removal.\n\n"
            "* Expected to remove the following book:\n"
            f"{removed_book_expected}\n\n"
            "* Student code returned the book:\n"
            f"{removed_book_returned}\n"
        )

        # 7) Decide pass/fail by comparing the Accessed-window blocks
        if expected_access and (expected_access.strip() == returned_access.strip()):
            write_json(True, msg + "\nRESULT: Book was CORRECTLY REMOVED from the catalog.\n\nTest PASSED.")
        else:
            write_json(
                False,
                msg
                + "\nRESULT: Book was NOT CORRECTLY REMOVED from catalog or an UNEXPECTED ERROR occurred."
                + "\n\nExpected accessed books:\n" + expected_access
                + "\n\nAccessed books:\n" + returned_access
                + "\n\nTest FAILED."
            )

    except Exception as e:
        write_json(False, f"Harness error: {e}")


if __name__ == "__main__":
    main()
