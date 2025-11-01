
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
      # TestCase must return a TestOutput Object
      # TestObject is initialized
      msg = "Testing ArrayList add(i, x)..."
      try:
        answer = ArrayListCP.ArrayList()
        student = ArrayList.ArrayList()
    
        msg += "\n\nCreated ArrayList object lst."
        
        for i in range(random.randint(3, 5)):
          letter = chr(random.randint(65, 85))
          answer.append(letter)
          student.append(letter)
          msg += "\n\n"+"-"*30 + f"\nCalled lst.append({letter})\nExpected list: {answer}\t\tSize: {answer.size()}\nReceived list: {student}\t\tSize: {student.size()}\n\nExpected backing array: {answer.a}\nReceived backing array: {student.a}"
          arr_bool = np.array_equal(answer.a, student.a)
          boolean = arr_bool and (answer.size() == student.size()) and str(answer) == str(student)
          if not boolean:
            msg += "\n\nTest FAILED."
            return TestOutput(passed=False, logs=msg)
        
        for i in range(random.randint(5, 7)):
          idx = random.randint(0, answer.size()-1)
          letter = chr(random.randint(65, 85))
          answer.add(idx, letter)
          student.add(idx, letter)
          msg += "\n\n"+"-"*30 + f"\nCalled lst.add({idx}, {letter})\nExpected list: {answer}\t\tSize: {answer.size()}\nReceived list: {student}\t\tSize: {student.size()}\n\nExpected backing array: {answer.a}\nReceived backing array: {student.a}"
          arr_bool = answer.a == student.a
          print("arrays are equal:", arr_bool)
          print("sizes agree:", answer.size() == student.size())
          print("strings are the same:", str(answer) == str(student))
          boolean = arr_bool.all() and (answer.size() == student.size()) and str(answer) == str(student)
          if not boolean:
            msg += "\n\nTest FAILED."
            return TestOutput(passed=False, logs=msg)
      
        msg += "\n\nAll tests PASSED."
        return TestOutput(passed=True, logs=msg)
      except Exception as e:
        print(e)
        msg += f"\nThe following unexpected error occurred:\n {e}"
        return TestOutput(passed=False, logs=msg)
    

    output = TestCase()
    assert(isinstance(output, TestOutput))
except Exception as e:
    errorLogs = traceback.format_exc()
    output = TestOutput(False, str(errorLogs))
f = open("/outputs/144798.json", "w")
json.dump({"id": "144798", "passed": output.passed, "log": output.logs}, f)
f.close()
