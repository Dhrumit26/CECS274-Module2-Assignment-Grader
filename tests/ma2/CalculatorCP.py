import ArrayStackCP as ArrayStack


class Calculator:
    def __init__(self):
        self.dict = None

    def balanced_parens(self, s: str) -> bool:
        parens = ArrayStack.ArrayStack()
        for c in s:
            if c == "(":
                parens.push(c)
            if c == ")":
                if parens.size() > 0:
                    parens.pop()
                else:
                    return False
        return parens.size() == 0
