
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
    
    import ArrayQueue
    
    def TestCase():
      # TestCase must return a TestOutput Object
      # TestObject is initialized
      student_queue = ArrayQueue.ArrayQueue()
      
      try:
        student_queue.remove()
        msg = "Created empty ArrayQueue and attempted to remove an element.\nIndexError was not raised.\nTest failed."
        return TestOutput(passed=False, logs=msg)
      except IndexError:
        return TestOutput(passed=True, logs="Created empty ArrayQueue and attempted to remove an element.\nIndexError is correctly raised. \nTest passed.")
      except Exception as e:
        print("The following unexpected error occurred:\n", e)
    

    output = TestCase()
    assert(isinstance(output, TestOutput))
except Exception as e:
    errorLogs = traceback.format_exc()
    output = TestOutput(False, str(errorLogs))
f = open("/outputs/144790.json", "w")
json.dump({"id": "144790", "passed": output.passed, "log": output.logs}, f)
f.close()
