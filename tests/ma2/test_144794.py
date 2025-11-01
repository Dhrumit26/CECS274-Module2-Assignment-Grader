
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
    import ArrayStackCP
    import ArrayStack
    import random
    
    def TestCase():
      # TestCase must return a TestOutput Object
      # TestObject is initialized
      msg = "Testing ArrayStack push(x)..."
      try:
        answer = ArrayStackCP.ArrayStack()
        student = ArrayStack.ArrayStack()
    
        msg += "\n\nCreated ArrayStack object s."
        for i in range(random.randint(10, 17)):
          letter = chr(random.randint(97, 120))
          answer.push(letter)
          student.push(letter)
          msg += "\n\n"+"-"*30 + f"\nCalled s.push({letter}):\nExpected stack: {answer}\t\tSize: {answer.size()}\nReceived stack: {student}\t\tSize: {student.size()}\n\nExpected backing array: {answer.a}\nReceived backing array: {student.a}"
          arr_bool = answer.a == student.a
          boolean = arr_bool.all() and (answer.size() == student.size()) and str(answer) == str(student)
          if not boolean:
            msg += "\n\nTest FAILED."
            return TestOutput(passed=False, logs=msg)
      
        msg += "\n\nAll tests PASSED."
        return TestOutput(passed=True, logs=msg)
      except Exception as e:
        msg += f"\nThe following unexpected error occurred:\n {e}"
        return TestOutput(passed=False, logs=msg)
    

    output = TestCase()
    assert(isinstance(output, TestOutput))
except Exception as e:
    errorLogs = traceback.format_exc()
    output = TestOutput(False, str(errorLogs))
f = open("/outputs/144794.json", "w")
json.dump({"id": "144794", "passed": output.passed, "log": output.logs}, f)
f.close()
