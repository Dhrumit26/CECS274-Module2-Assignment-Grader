
import json
import traceback
import os

class TestOutput:
    def __init__(self, passed, logs):
        assert (isinstance(passed, bool))
        assert (isinstance(logs, str))
        self.passed = passed
        self.logs = logs

try:
    import Calculator
    
    def TestCase():
      msg = "Testing Calculator balanced_parens(\"\") ..."
      try:
        expr = ""
        calculator = Calculator.Calculator()
        is_balanced = calculator.balanced_parens(expr)
    
        msg += "\nExpected: True"
        msg += f"\nReturned: {is_balanced}"
    
        if (is_balanced):
          msg += "\nTest PASSED."
          return TestOutput(passed=True, logs=msg)
        else:
          msg += "\nTest FAILED."
          return TestOutput(passed=False, logs=msg)
      except Exception as e:
        msg += f"\nThe following unexpected error occurred:\n{e}"
        return TestOutput(passed=False, logs=msg)

    output = TestCase()
    assert(isinstance(output, TestOutput))
except Exception as e:
    errorLogs = traceback.format_exc()
    output = TestOutput(False, str(errorLogs))
f = open("/outputs/144805.json", "w")
json.dump({"id": "144805", "passed": output.passed, "log": output.logs}, f)
f.close()
