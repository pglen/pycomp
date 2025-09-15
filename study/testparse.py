import re

def tokenize(expr):
    """
    Convert a string expression into tokens.
    Example: " (2 + 3) * 4 " -> ["(", "2", "+", "3", ")", "*", "4"]
    """
    token_pattern = r"\d+|[()+\-*/]"
    return re.findall(token_pattern, expr)


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consume(self):
        token = self.peek()
        self.pos += 1
        return token

    # Grammar:
    # expr   → term (("+" | "-") term)*
    # term   → factor (("*" | "/") factor)*
    # factor → NUMBER | "(" expr ")"

    def parse(self):
        return self.expr()

    def expr(self):
        node = self.term()
        while self.peek() in ("+", "-"):
            op = self.consume()
            right = self.term()
            node = (op, node, right)
        return node

    def term(self):
        node = self.factor()
        while self.peek() in ("*", "/"):
            op = self.consume()
            right = self.factor()
            node = (op, node, right)
        return node

    def factor(self):
        token = self.peek()
        if token is None:
            raise SyntaxError("Unexpected end of input")

        if token.isdigit():  # number
            self.consume()
            return ("num", int(token))

        if token == "(":
            self.consume()  # consume "("
            node = self.expr()
            if self.peek() != ")":
                raise SyntaxError("Expected ')'")
            self.consume()  # consume ")"
            return node

        raise SyntaxError(f"Unexpected token: {token}")


def evaluate(ast):
    """Evaluate the AST recursively."""
    if ast[0] == "num":
        return ast[1]

    op, left, right = ast
    lval = evaluate(left)
    rval = evaluate(right)

    if op == "+":
        return lval + rval
    elif op == "-":
        return lval - rval


