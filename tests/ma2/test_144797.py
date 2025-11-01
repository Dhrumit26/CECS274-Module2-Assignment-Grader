
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
      msg = "Testing ArrayStack remove(i)..."
      try:
        answer = ArrayStackCP.ArrayStack()
        student = ArrayStack.ArrayStack()
    
        msg += "\n\nCreated ArrayStack object s."
        for i in range(random.randint(7, 10)):
          letter = chr(random.randint(97, 120))
          answer.push(letter)
          student.push(letter)
          msg += f"\nCalled s.push({letter})"
        msg += f"\n\nExpected stack: {answer}\t\tSize: {student.size()}\nReceived stack: {student}\t\tSize: {student.size()}"
        while answer.size() > 0:
          idx = random.randint(0, answer.size()-1)
          expected = answer.remove(idx)
          received = student.remove(idx)
          msg += "\n\n"+"-"*30 + f"\nCalled s.remove({idx})\nExpected element: {expected}\nReceived element: {received}\nExpected stack: {answer}\t\tSize: {answer.size()}\nReceived stack: {student}\t\tSize: {student.size()}\n\nExpected backing array: {answer.a}\nReceived backing array: {student.a}"
          arr_bool = answer.a == student.a
          boolean = arr_bool.all() and (answer.size() == student.size()) and str(answer) == str(student) and expected == received
          if not boolean:
            msg += "\n\nTest FAILED."
            return TestOutput(passed=False, logs=msg)
      
        msg += "\n\nAll tests PASSED."
        return TestOutput(passed=True, logs=msg)
      except Exception as e:
        msg += f"\nThe following unexpected error occurred:\n{e}\n\nTest FAILED."
        return TestOutput(passed=False, logs=msg)
    

    output = TestCase()
    assert(isinstance(output, TestOutput))
except Exception as e:
    errorLogs = traceback.format_exc()
    output = TestOutput(False, str(errorLogs))
f = open("/outputs/144797.json", "w")
json.dump({"id": "144797", "passed": output.passed, "log": output.logs}, f)
f.close()
