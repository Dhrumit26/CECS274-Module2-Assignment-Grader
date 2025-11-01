
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
    
    def TestCase():
      msg = "Testing ArrayList set(i, x)..."
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
        n = answer.size()
        invalid = [i for i in range(-1*n, -1)] + [j for j in range(n, n+10)]
        idx = invalid[random.randint(0, len(invalid)-1)]
        letter = chr(random.randint(65, 90))
        student.set(idx, letter)
        msg += f"\n\nCalled lst.set({idx}, {letter})\nExpected: IndexError\nIndexError was NOT RAISED.\n\nTest FAILED."
        return TestOutput(passed=False, logs=msg)
    
      except IndexError:
        msg += f"\n\nCalled lst.set({idx}, {letter})\nExpected: IndexError\nRaised: IndexError.\n\nTest PASSED."
        return TestOutput(passed=True, logs=msg)
      except Exception as e:
        msg += f"\nThe following unexpected error occurred:\n{e}\n\nTest FAILED."
        return TestOutput(passed=False, logs=msg)
    

    output = TestCase()
    assert(isinstance(output, TestOutput))
except Exception as e:
    errorLogs = traceback.format_exc()
    output = TestOutput(False, str(errorLogs))
f = open("/outputs/144804.json", "w")
json.dump({"id": "144804", "passed": output.passed, "log": output.logs}, f)
f.close()
