
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
    import ArrayQueueCP
    import ArrayQueue
    import random
    
    def TestCase():
      # TestCase must return a TestOutput Object
      # TestObject is initialized
      msg = "Testing ArrayQueue remove()..."
      try:
        answer_queue = ArrayQueueCP.ArrayQueue()
        student_queue = ArrayQueue.ArrayQueue()
    
        msg += "\n\nCreated ArrayQueue object q."
        for i in range(random.randint(10, 17)):
          letter = chr(random.randint(97, 120))
          answer_queue.add(letter)
          student_queue.add(letter)
          msg += f"\nCalled q.add({letter})"
        while answer_queue.size() > 0:
          expected = answer_queue.remove()
          received = student_queue.remove()
          msg += "\n\n"+"-"*30 + f"\nCalled q.remove()\nExpected element: {expected}\nReceived element: {received}\nExpected queue: {answer_queue}\t\tSize: {answer_queue.size()}\nReceived queue: {student_queue}\t\tSize: {student_queue.size()}\n\nExpected backing array: {answer_queue.a}\nReceived backing array: {student_queue.a}"
          arr_bool = answer_queue.a == student_queue.a
          boolean = arr_bool.all() and (answer_queue.size() == student_queue.size()) and str(answer_queue) == str(student_queue) and expected == received
          if not boolean:
            msg += "\n\nTest FAILED."
            return TestOutput(passed=False, logs=msg)
      
        msg += "\n\nAll tests PASSED."
        return TestOutput(passed=True, logs=msg)
      except Exception as e:
        msg += f"The following unexpected error occurred:\n{e}\n\nTest FAILED."
        return TestOutput(passed=False, logs=msg)
    

    output = TestCase()
    assert(isinstance(output, TestOutput))
except Exception as e:
    errorLogs = traceback.format_exc()
    output = TestOutput(False, str(errorLogs))
f = open("/outputs/144792.json", "w")
json.dump({"id": "144792", "passed": output.passed, "log": output.logs}, f)
f.close()
