#!/usr/bin/env python3
"""
Python port of test_144815.sh

Flow:
- Run tests/ma2/input_generator.py to create input_5.txt in the CWD.
- Parse catalog number from line 3 (digits only).
- Run reference (tests/ma2/mainCP.py) and student (main.py) with input_5.txt via stdin.
- From both outputs, extract lines between:
      'Removed from shopping cart the following book:'
  and the next line containing 'Action'
  (excluding the boundary lines themselves), preserving order.
- PASS iff:
    * extracted blocks (expected vs. returned) are exactly equal,
    * and expected block is non-empty / non-whitespace.
- Write JSON to ${OUTPUTS_DIR}/144815.json.
"""

import json
import os
import re
import sys
import subprocess
from pathlib import Path
from typing import Tuple

TEST_ID = "144815"
OUTPUTS_DIR = Path(os.environ.get("OUTPUTS_DIR", "__outputs__"))
PYTHON_BIN = os.environ.get("PYTHON_BIN", sys.executable)
TESTS_DIR = Path(__file__).parent  # tests/ma2

OUT_JSON = OUTPUTS_DIR / f"{TEST_ID}.json"
INPUT_TXT = Path("input_5.txt")

# Optional stderr captures (helpful for debugging failures)
GEN_STDERR = OUTPUTS_DIR / f"{TEST_ID}_gen.stderr.txt"
REF_STDERR = OUTPUTS_DIR / f"{TEST_ID}_ref.stderr.txt"
STU_STDERR = OUTPUTS_DIR / f"{TEST_ID}_stu.stderr.txt"


def write_json(passed: bool, logs: str = "") -> None:
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(
        json.dumps({"id": TEST_ID, "passed": bool(passed), "log": str(logs)}),
        encoding="utf-8",
    )


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


def parse_catalog_number(line3: str) -> str:
    # Shell used: sed -n '3 s/[^0-9]//gp'
    return "".join(ch for ch in line3 if ch.isdigit())


def extract_removed_block(stdout_text: str) -> str:
    """
    Emulates:
      sed -n '/Removed from shopping cart the following book:/,/Action/ {
        /Removed from shopping cart the following book:/d; /Action/d; p;
      }'
    """
    lines = stdout_text.splitlines()
    start_idx, end_idx = None, None
    for i, ln in enumerate(lines):
        if "Removed from shopping cart the following book:" in ln:
            start_idx = i
            break
    if start_idx is None:
        return ""

    for j in range(start_idx + 1, len(lines)):
        if "Action" in lines[j]:
            end_idx = j
            break
    if end_idx is None:
        # If no 'Action' sentinel, take until end
        end_idx = len(lines)

    # Exclude the boundary lines themselves
    body = lines[start_idx + 1:end_idx]
    return "\n".join(body).strip("\n")


def main():
    try:
        OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

        # 1) Generate inputs (creates input_5.txt in CWD)
        rc, gen_out, gen_err = run([PYTHON_BIN, str(TESTS_DIR / "input_generator.py")],
                                   capture_stderr_to=GEN_STDERR)
        if rc != 0:
            tail = (gen_err.splitlines()[-60:] if gen_err else [])
            write_json(False, "ERROR: input_generator.py failed to execute properly.\n\nSTDERR (last lines):\n" + "\n".join(tail))
            return

        # 2) Ensure input_5.txt exists
        if not INPUT_TXT.exists():
            write_json(False, "ERROR: input_5.txt not found.")
            return

        input_text = INPUT_TXT.read_text(encoding="utf-8", errors="ignore")
        lines = input_text.splitlines()
        line3 = lines[2] if len(lines) >= 3 else ""
        catalog_num = parse_catalog_number(line3)

        # 3) Run reference and student with input_5 on stdin
        env = os.environ.copy()
        env["PYTHONPATH"] = f".:{TESTS_DIR}:{env.get('PYTHONPATH','')}"

        rc, ref_out, ref_err = run([PYTHON_BIN, str(TESTS_DIR / "mainCP.py")],
                                   env=env, stdin_text=input_text, capture_stderr_to=REF_STDERR)
        if rc != 0:
            tail = (ref_err.splitlines()[-60:] if ref_err else [])
            write_json(False, "ERROR: Reference solution (mainCP.py) failed.\n\nSTDERR (last lines):\n" + "\n".join(tail))
            return

        rc, stu_out, stu_err = run([PYTHON_BIN, "main.py"],
                                   env=env, stdin_text=input_text, capture_stderr_to=STU_STDERR)
        if rc != 0:
            tail = (stu_err.splitlines()[-60:] if stu_err else [])
            write_json(False, "ERROR: Student program (main.py) failed.\n\nSTDERR (last lines):\n" + "\n".join(tail))
            return

        # 4) Extract removed-book blocks
        expected_block = extract_removed_block(ref_out)
        returned_block = extract_removed_block(stu_out)

        # 5) Build message like the shell
        msg = (
            f"Testing addBookByIndex(i) on catalog {catalog_num}...\n\n"
            f"STUDENT OUTPUT:\n{stu_out}\n"
            "-------------------------------------------\n"
            "FEEDBACK:\n\n"
            "* What this tester did:\n"
            f"      1. Loaded the catalog {catalog_num}\n"
            "      2. Added books to the cart by index\n"
            "      3. Removed all books from the cart\n\n"
            "* Expected to remove from the cart the following books:\n"
            f"{expected_block}"
        )

        # 6) Pass/Fail
        non_empty_expected = bool(expected_block.strip())
        if (expected_block == returned_block) and non_empty_expected:
            write_json(True, msg + "\n\nRESULT: Books were CORRECTLY ADDED/REMOVED from shopping cart.\n\nTest PASSED.")
        else:
            write_json(False, msg + "\n\nRESULT: INCORRECT book(s) was added/removed or an UNEXPECTED ERROR occurred.\n\nTest FAILED.")

    except Exception as e:
        write_json(False, f"Harness error: {e}")


if __name__ == "__main__":
    main()
