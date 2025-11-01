
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
        idx = random.randint(0, answer.size()-1)
        letter = chr(random.randint(65, 90))
        answer.set(idx, letter)
        student.set(idx, letter)
        msg += f"\n\nCalled lst.set({idx}, {letter})\nExpected list: {answer}\t\tSize: {answer.size()}\nReceived list: {student}\t\tSize: {student.size()}\n\nExpected backing array: {answer.a}\nReceived backing array: {student.a}"
        boolean = str(answer) == str(student) and (answer.a == student.a).all()
        if not boolean:
          msg += "\n\nTest FAILED."
          return TestOutput(passed=False, logs=msg)
        else:
          msg += "\n\nTest PASSED."
          return TestOutput(passed=True, logs=msg)
      except Exception as e:
        msg += f"\n\nThe following unexpected error occurred:\n{e}\n\nTest FAILED."
        return TestOutput(passed=False, logs=msg)
    

    output = TestCase()
    assert(isinstance(output, TestOutput))
except Exception as e:
    errorLogs = traceback.format_exc()
    output = TestOutput(False, str(errorLogs))
f = open("/outputs/144802.json", "w")
json.dump({"id": "144802", "passed": output.passed, "log": output.logs}, f)
f.close()
