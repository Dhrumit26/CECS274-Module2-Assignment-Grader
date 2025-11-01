
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
    import random
    from expression_builder import build_math_expr
    
    def TestCase():
      n = random.randint(2, 4)
      
      expr = build_math_expr(n, True, ')')
      msg = f"Testing Calculator balanced_parens(expr)..." 
      try:
        calculator = Calculator.Calculator()
        is_balanced = calculator.balanced_parens(expr)
    
    
        msg += f"\n\nExpression: {expr}"
        msg += "\nExpected: False"
        msg += f"\nReturned: {is_balanced}"
    
        if (not is_balanced):
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
f = open("/outputs/144806.json", "w")
json.dump({"id": "144806", "passed": output.passed, "log": output.logs}, f)
f.close()
