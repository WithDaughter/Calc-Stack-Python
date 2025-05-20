from collections import deque


class Lexer:
    EOF = '?'
    def __init__(self, src):
        self.queue = deque(src)

    @staticmethod
    def is_operator(token):
        return token in '+-*/()'

    @staticmethod
    def is_space(token):
        return token in ' \t\n'

    def push_number(self):
        nums = ''
        while (self.queue and not Lexer.is_space(self.queue[0])
               and not self.is_operator(self.queue[0])):
            nums += self.queue.popleft()
        self.queue.appendleft(float(nums))

    def peek_token(self):
        try:
            while self.queue[0] in ' \t\n':
                self.queue.popleft()
        except IndexError:
            return Lexer.EOF
        token = self.queue[0]
        if Lexer.is_operator(token):
            return token
        elif isinstance(token, float):
            return token
        else:
            self.push_number()
            return self.queue[0]

    def get_token(self):
        if self.queue:
            return self.queue.popleft()
        else:
            return Lexer.EOF


def to_postfix(src):
    is_op = lambda t: t in '+-*/'
    is_lparen = lambda t: t == '('
    is_rparen = lambda t: t == ')'
    is_op_multi_divide = lambda t: t in '*/'

    lexer = Lexer(src)
    op_stack = []
    postfix_queue = []
    token = lexer.peek_token()
    while token != Lexer.EOF:
        if isinstance(token, float):
            postfix_queue.append(lexer.get_token())
        elif is_lparen(token):
            op_stack.append(lexer.get_token())
        elif is_rparen(token):
            while op_stack and not is_lparen(op_stack[-1]):
                postfix_queue.append(op_stack.pop())
            op_stack.pop()
            lexer.get_token()
        elif is_op(token):
            if is_op_multi_divide(token):
                while op_stack and is_op_multi_divide(op_stack[-1]):
                    postfix_queue.append(op_stack.pop())
            else:
                while op_stack and not is_lparen(op_stack[-1]):
                    postfix_queue.append(op_stack.pop())
            op_stack.append(lexer.get_token())
        token = lexer.peek_token()
    if op_stack:
        postfix_queue.append(op_stack.pop())
    return postfix_queue


def stack(src):
    postfix_queue = to_postfix(src)
    return postfix_queue


if __name__ == '__main__':
    src = '(1*2)+(2/3)'
    val = stack(src)
    print(val)
