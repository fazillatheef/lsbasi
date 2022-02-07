INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF = (
    'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', '(', ')', 'EOF'
)

class Token():
    def __init__(self,type,value):
        self.value= value
        self.type = type

class Lexer():
    def __init__(self,text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception("Invalid Character")

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER,self.integer())
            
            if self.current_char == '+':
                self.advance()
                return Token(PLUS,'+')
            
            if self.current_char == '-':
                self.advance()
                return Token(MINUS,'-')
            
            if self.current_char == '*':
                self.advance()
                return Token(MUL,'*')
            
            if self.current_char == '/':
                self.advance()
                return Token(DIV,'/')

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN,'(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN,')')
            
            self.error()
        return Token(EOF,None)
                        

class BinOp:
    def __init__(self,left,op,right):
        self.operator = True
        self.left = left
        self.token = self.op = op
        self.right = right

class Num:
    def __init__(self,token):
        self.operator = False
        self.token = token
        self.value = token.value

class Parser:
    def __init__(self,lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception("Invalid syntax")
    
    def eat(self,token):
        if self.current_token.type == token:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node

    def term(self):
        node = self.factor()

        while self.current_token.type in (MUL,DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)
            node = BinOp(left=node,op=token,right=self.factor())
        
        return node

    def expr(self):
        node = self.term()
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        return node
    
    def parse(self):
        return self.expr()



class Interpreter():
    def __init__(self, parser):
        self.parser = parser
            
    def visit(self, node):
        if node.operator:
            if node.op.type == PLUS:
                return self.visit(node.left) + self.visit(node.right)
            elif node.op.type == MINUS:
                return self.visit(node.left) - self.visit(node.right)
            elif node.op.type == MUL:
                return self.visit(node.left) * self.visit(node.right)
            elif node.op.type == DIV:
                return self.visit(node.left) / self.visit(node.right)
        else:
          return node.value  

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)



print(">>Console (Ctrl+Z to exit)<<")
while True:
    try:
        try:
            text = input('spi> ')
        except NameError:  # Python3
            text = input('spi> ')
    except EOFError:
        break
    if not text:
        continue

    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    result = interpreter.interpret()
    print(result)


