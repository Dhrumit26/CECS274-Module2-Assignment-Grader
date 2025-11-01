from ArrayList import ArrayList
from ArrayQueue import ArrayQueue
from ArrayStack import ArrayStack
import random

def test():
    """write your own tester in this function"""
    print("YOUR TESTS:")
    stack = ArrayStack()
    print("Created empty stack.")
    while stack.size() < 5:
        ele = random.randint(1, 10)
        if ele not in stack:
            stack.push(ele)
            print(f"Added: {ele}\nStack after addition: {stack}\nBacking array: {stack.a}\n")
    while stack.size() > 0:
        r = stack.pop()
        print(f"Popped: {r}\nStack after removal: {stack}\nBacking array: {stack.a}\n")

    print(stack)
    while stack.size() < 4:
        ele = random.randint(1, 10)
        if ele not in stack:
            stack.push(ele)
            print(f"Added: {ele}\nStack after addition: {stack}\nBacking array: {stack.a}\n")
    stack.add(1, 'A')
    print(f"Inserted 'A' at index 1\nStack after insertion: {stack}\nBacking array: {stack.a}\n")
    stack.add(3, 'B')
    print(f"Inserted 'B' at index 3\nStack after insertion: {stack}\nBacking array: {stack.a}\n")

    while stack.size() > 0:
        r = stack.pop()
        print(f"Popped: {r}\nStack after removal: {stack}\nBacking array: {stack.a}\n")


