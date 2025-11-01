
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
    import ArrayStack
    
    def TestCase():
      # TestCase must return a TestOutput Object
      # TestObject is initialized
      student = ArrayStack.ArrayStack()
      
      try:
        student.pop()
        msg = "Created empty ArrayStack and attempted to remove an element.\nIndexError was not raised.\nTest FAILED."
        return TestOutput(passed=False, logs=msg)
      except IndexError:
        msg = "Created empty ArrayStack and attempted to remove an element.\nIndexError is correctly raised. \nTest PASSED."
        return TestOutput(passed=True, logs=msg)
      except Exception as e:
        msg = f"The following unexpected error occurred:\n{e}\n\nTest FAILED."
        return TestOutput(passed=False, logs=msg)
    

    output = TestCase()
    assert(isinstance(output, TestOutput))
except Exception as e:
    errorLogs = traceback.format_exc()
    output = TestOutput(False, str(errorLogs))
f = open("/outputs/144793.json", "w")
json.dump({"id": "144793", "passed": output.passed, "log": output.logs}, f)
f.close()
