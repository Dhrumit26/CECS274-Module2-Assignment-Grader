
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
    import ArrayListCP
    import ArrayList
    import random
    import numpy as np
    
    def TestCase():
      msg = "Testing ArrayList remove(i)..."
      try:
        answer = ArrayListCP.ArrayList()
        student = ArrayList.ArrayList()
    
        msg += "\n\nCreated ArrayList object lst."
        for i in range(random.randint(8, 13)):
          letter = chr(random.randint(97, 120))
          answer.append(letter)
          student.append(letter)
          msg += f"\nCalled lst.append({letter})"
        msg += f"\n\nExpected list: {answer}\t\tSize: {student.size()}\nReceived list: {student}\t\tSize: {student.size()}"
        while answer.size() > 0:
          idx = random.randint(0, answer.size()-1)
          expected = answer.remove(idx)
          received = student.remove(idx)
          msg += "\n\n"+"-"*30 + f"\nCalled lst.remove({idx})\nExpected element: {expected}\nReceived element: {received}\nExpected list: {answer}\t\tSize: {answer.size()}\nReceived list: {student}\t\tSize: {student.size()}\n\nExpected backing array: {answer.a}\nReceived backing array: {student.a}"
          print(f"Expected backing array {answer.a}")
          print(f"Received backing array {student.a}")
          print(f"Arrays are equal: {np.array_equal(answer.a, student.a)}")
          boolean = np.array_equal(answer.a, student.a) and (answer.size() == student.size()) and str(answer) == str(student) and expected == received
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
f = open("/outputs/144799.json", "w")
json.dump({"id": "144799", "passed": output.passed, "log": output.logs}, f)
f.close()
