#!/usr/bin/env python3
"""
Python port of test_144813.sh

Flow:
- Run tests/ma2/input_generator.py to create input_3.txt in the student work dir (CWD).
- Run reference (tests/ma2/mainCP.py) and student (main.py) with input_3.txt on stdin.
- Extract lines strictly between "Accessed the following book from catalog:" and the next "Action"
  from both outputs (exclusive).
- Require exactly 4 lines in expected (to match the shell's wc -l check).
- Compare expected vs returned; write Gradescope-style JSON to ${OUTPUTS_DIR}/144813.json.

Notes:
- PYTHONPATH includes "." and tests/ma2 so helpers import cleanly.
- Any stderr is tailed into side files for debugging.
"""

import json
import os
import sys
import subprocess
from pathlib import Path
from typing import Tuple

TEST_ID = "144813"
DEFAULT_TESTS_DIR = Path(__file__).parent  # tests/ma2
OUTPUTS_DIR = Path(os.environ.get("OUTPUTS_DIR", "__outputs__"))
PYTHON_BIN = os.environ.get("PYTHON_BIN", sys.executable)

OUT_JSON = OUTPUTS_DIR / f"{TEST_ID}.json"
INPUT_TXT = Path("input_3.txt")

# Optional stderr tails for debugging
REF_STDERR = OUTPUTS_DIR / f"{TEST_ID}_ref.stderr.txt"
STU_STDERR = OUTPUTS_DIR / f"{TEST_ID}_stu.stderr.txt"


def write_json(passed: bool, logs: str = "") -> None:
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps({"id": TEST_ID, "passed": bool(passed), "log": str(logs)}), encoding="utf-8")


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
    Extract lines strictly between:
      'Accessed the following book from catalog:' and the next 'Action'
    (excluding both markers). Mirrors the sed logic from the shell script.
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


def parse_catalog_and_idx_from_input(input_text: str) -> tuple[str, str]:
    """
    Shell did:
      catalog_num: digits from line 3
      idx: full line 5
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

        # 1) Generate inputs (creates input_3.txt in CWD).
        rc, gen_out, gen_err = run([PYTHON_BIN, str(tests_dir / "input_generator.py")], capture_stderr_to=REF_STDERR)
        if rc != 0:
            tail = (gen_err.splitlines()[-60:] if gen_err else [])
            write_json(False, "ERROR: input_generator.py failed to execute properly.\n\nSTDERR (last lines):\n" + "\n".join(tail))
            return

        # 2) Validate presence of input_3.txt
        if not INPUT_TXT.exists():
            write_json(False, "ERROR: input_3.txt not found.")
            return

        input_text = INPUT_TXT.read_text(encoding="utf-8", errors="ignore")
        catalog_num, idx = parse_catalog_and_idx_from_input(input_text)

        # 3) Run reference and student programs
        env = os.environ.copy()
        env["PYTHONPATH"] = f".:{tests_dir}:{env.get('PYTHONPATH','')}"

        rc, ref_out, ref_err = run([PYTHON_BIN, str(tests_dir / "mainCP.py")],
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

        # 4) Extract the Accessed-window blocks
        expected = extract_between_access_and_action(ref_out)
        returned = extract_between_access_and_action(stu_out)

        # 5) Enforce "exactly 4 lines" for expected
        expected_lines_count = 0 if not expected else expected.count("\n") + 1
        if expected_lines_count != 4:
            write_json(False, f"ERROR: Unexpected error occurred while attempting to access book at index {idx} of catalog {catalog_num}.")
            return

        # 6) Compose feedback message (like the shell)
        msg = (
            f"Testing getBookAtIndex({idx}) on catalog {catalog_num}...\n\n"
            f"STUDENT OUTPUT:\n{stu_out}\n"
            "-------------------------------------------\n"
            "FEEDBACK:\n\n"
            "* What this tester did:\n"
            f"      1. Loaded the catalog {catalog_num}\n"
            f"      2. Accessed book at index {idx}\n\n"
            "* Expected to access the following book:\n"
            f"{expected}"
        )

        # 7) Pass/fail
        if expected and (expected.strip() == returned.strip()):
            write_json(True, msg + "\n\nRESULT: Book was CORRECTLY ACCESSED.\n\nTest PASSED.")
        else:
            write_json(False, msg + "\n\nRESULT: INCORRECT BOOK was returned or an UNEXPECTED ERROR occurred.\n\nTest FAILED.")

    except Exception as e:
        write_json(False, f"Harness error: {e}")


if __name__ == "__main__":
    main()
