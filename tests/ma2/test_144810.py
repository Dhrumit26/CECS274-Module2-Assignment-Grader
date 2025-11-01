
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
    
    def TestCase():
      # TestCase must return a TestOutput Object
      # TestObject is initialized
      operators = ['*', '+', '-', '/']
      x = ["(" + chr(random.randint(65,90))+ operators[random.randint(0, len(operators)-1)] + chr(random.randint(65,90))+ ")" for i in range(len(operators) + 1)]
      parens = ['(', ')', '(', ')']
      expr = ''
      
      
      while len(parens) > 0:
        r = random.randint(1, 2)
        if r == 1:
          expr += parens[0]
          del parens[0]
          i = random.randint(0, len(x)-1)
          expr += x[i]
    
        else:
          i = random.randint(0, len(x)-1)
          expr += x[i]
          
      msg = f"Testing Calculator balanced_parens(expr)..."
      
      try:
        calculator = Calculator.Calculator()
        is_balanced = calculator.balanced_parens(expr)
    
    
        msg += f"\n\nExpression: {expr}"
        msg += "\nExpected: True"
        msg += f"\nReturned: {is_balanced}"
    
        if (is_balanced):
          msg += "\nTest passed."
          return TestOutput(passed=True, logs=msg)
        else:
          msg += "\nTest failed."
          return TestOutput(passed=False, logs=msg)
      except Exception as e:
        msg += f"The following unexpected error occurred:\n{e}"
        return TestOutput(passed=False, logs=msg)

    output = TestCase()
    assert(isinstance(output, TestOutput))
except Exception as e:
    errorLogs = traceback.format_exc()
    output = TestOutput(False, str(errorLogs))
f = open("/outputs/144810.json", "w")
json.dump({"id": "144810", "passed": output.passed, "log": output.logs}, f)
f.close()
