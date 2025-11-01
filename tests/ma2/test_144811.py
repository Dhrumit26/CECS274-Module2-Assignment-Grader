#!/usr/bin/env python3
"""
Robust Python port of test_144811.sh.

- Runs tests/ma2/input_generator.py
- Ensures INPUT_TXT ends up at OUTPUTS_DIR/input_1.txt (copy from CWD/tests dir if needed)
- Runs reference mainCP.py and student main.py
- Extracts lines between:
    'Accessed the following book from catalog:'  ... up to next line starting with 'Action'
- Writes Gradescope-style JSON to OUTPUTS_DIR/144811.json
"""

import json
import os
import re
import sys
import shutil
import subprocess
from pathlib import Path
from typing import Optional, Tuple

TEST_ID = "144811"
DEFAULT_TESTS_DIR = Path(__file__).parent  # tests/ma2
OUTPUTS_DIR = Path(os.environ.get("OUTPUTS_DIR", "__outputs__"))
PYTHON_BIN = os.environ.get("PYTHON_BIN", sys.executable)

OUT_JSON   = OUTPUTS_DIR / f"{TEST_ID}.json"
INPUT_TXT  = OUTPUTS_DIR / "input_1.txt"
REF_STDERR = OUTPUTS_DIR / f"{TEST_ID}_ref.stderr.txt"
STU_STDERR = OUTPUTS_DIR / f"{TEST_ID}_stu.stderr.txt"

def write_json(passed: bool, logs: str = "") -> None:
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps({"id": TEST_ID, "passed": bool(passed), "log": str(logs)}), encoding="utf-8")

def run(cmd, *, env=None, stdin_text: Optional[str]=None, cwd: Optional[Path]=None,
        capture_stderr_to: Optional[Path]=None) -> Tuple[int, str, str]:
    proc = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE if stdin_text is not None else None,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env,
        cwd=str(cwd) if cwd else None,
    )
    out, err = proc.communicate(stdin_text)
    if capture_stderr_to is not None:
        try:
            capture_stderr_to.write_text(err or "", encoding="utf-8")
        except Exception:
            pass
    return proc.returncode, (out or ""), (err or "")

def extract_between_block(s: str) -> str:
    """
    Extract lines strictly between the first occurrence of the anchor:
        'Accessed the following book from catalog:'
    and the next line that starts with 'Action' (e.g., 'Action', 'Action:', etc.)
    """
    lines = s.splitlines()
    start_idx = None
    end_idx = None
    for i, ln in enumerate(lines):
        if start_idx is None and "Accessed the following book from catalog:" in ln:
            start_idx = i + 1
            continue
        if start_idx is not None and re.match(r'^\s*Action\b', ln):
            end_idx = i
            break
    if start_idx is None:
        return ""  # anchor not found
    if end_idx is None:
        end_idx = len(lines)
    block = lines[start_idx:end_idx]
    # Trim leading/trailing blank lines
    while block and not block[0].strip():
        block.pop(0)
    while block and not block[-1].strip():
        block.pop()
    return "\n".join(block)

def ensure_input_in_outputs() -> Tuple[bool, str]:
    """
    Ensure OUTPUTS_DIR/input_1.txt exists.
    Search in likely places and copy into OUTPUTS_DIR if necessary.
    Returns (ok, debug_message).
    """
    searched = []
    # likely spots: current working dir (student sandbox), tests dir, outputs dir itself
    candidates = [
        Path.cwd() / "input_1.txt",
        DEFAULT_TESTS_DIR / "input_1.txt",
        INPUT_TXT,
    ]
    for c in candidates:
        searched.append(str(c))
        if c.exists() and c.stat().st_size > 0:
            if c != INPUT_TXT:
                OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
                try:
                    shutil.copy2(c, INPUT_TXT)
                except Exception:
                    return (False, f"Found {c} but failed to copy to {INPUT_TXT}")
            return (True, f"Using {INPUT_TXT}")
    # final fallback: any input_*.txt in CWD, pick the one with suffix 1 if present
    any_inputs = sorted(Path.cwd().glob("input_*.txt"))
    if any_inputs:
        # prefer input_1.txt if present; else first one
        prefer = [p for p in any_inputs if p.name == "input_1.txt"]
        src = prefer[0] if prefer else any_inputs[0]
        searched.append(str(src))
        OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
        try:
            shutil.copy2(src, INPUT_TXT)
            return (True, f"Copied {src} to {INPUT_TXT}")
        except Exception as e:
            return (False, f"Found {src} but failed to copy: {e}")

    return (False, "Searched:\n  " + "\n  ".join(searched))

def main():
    try:
        OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
        tests_dir = DEFAULT_TESTS_DIR

        # 1) Generate inputs (run from CWD = student sandbox; script path is tests_dir/input_generator.py)
        rc, gen_out, gen_err = run([PYTHON_BIN, str(tests_dir / "input_generator.py")],
                                   capture_stderr_to=REF_STDERR)
        if rc != 0:
            tail = "\n".join(gen_err.splitlines()[-60:])
            write_json(False, f"input_generator.py failed.\n\nSTDERR (last lines):\n{tail}")
            return

        # If generator printed the input to stdout, write it to OUTPUTS_DIR/input_1.txt
        if gen_out.strip():
            OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
            INPUT_TXT.write_text(gen_out, encoding="utf-8")

        ok, dbg = ensure_input_in_outputs()
        if not ok:
            write_json(False, "input_1.txt not created by input_generator.py.\n\n" + dbg)
            return

        input_text = INPUT_TXT.read_text(encoding="utf-8")

        # 2) Run reference solution with PYTHONPATH including tests dir
        env = os.environ.copy()
        env["PYTHONPATH"] = f".:{tests_dir}:{env.get('PYTHONPATH','')}"
        rc, ref_out, ref_err = run([PYTHON_BIN, str(tests_dir / "mainCP.py")],
                                   env=env, stdin_text=input_text, capture_stderr_to=REF_STDERR)
        if rc != 0:
            tail = "\n".join(ref_err.splitlines()[-60:])
            write_json(False, "Reference solution (mainCP.py) failed.\n\nSTDERR (last lines):\n" + tail)
            return

        # 3) Run student program
        rc, stu_out, stu_err = run([PYTHON_BIN, "main.py"],
                                   env=env, stdin_text=input_text, capture_stderr_to=STU_STDERR)
        if rc != 0:
            tail = "\n".join(stu_err.splitlines()[-60:])
            write_json(False, "Student program (main.py) failed.\n\nSTDERR (last lines):\n" + tail)
            return

        # 4) Extract and compare
        expected = extract_between_block(ref_out)
        returned = extract_between_block(stu_out)

        if not expected.strip():
            preview = "\n".join(ref_out.splitlines()[:120])
            write_json(False,
                "Could not locate expected block in reference output.\n\n"
                "Reference output (first 120 lines):\n" + preview
            )
            return

        snippet = stu_out[:1200]
        base_msg = (
            "Testing addToCatalog on generated input.\n\n"
            "Student output (truncated):\n" + snippet + "\n\n"
            "Verification:\n"
            f"- expected block lines: {len(expected.splitlines())}\n"
            f"- returned  block lines: {len(returned.splitlines())}\n"
        )

        if expected == returned and expected.strip():
            write_json(True, base_msg + "\nRESULT: Output matched reference. Test PASSED.")
        else:
            write_json(False, base_msg +
                "\nRESULT: Output did not match reference. Test FAILED.\n\n"
                "Expected block (first 40 lines):\n" + "\n".join(expected.splitlines()[:40]) +
                "\n\nReturned block (first 40 lines):\n" + "\n".join(returned.splitlines()[:40])
            )

    except Exception as e:
        write_json(False, f"Harness error: {e}")

if __name__ == "__main__":
    main()
