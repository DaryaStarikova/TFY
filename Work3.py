import string
alphabetLC = list(string.ascii_lowercase)
alphabetUC = list(string.ascii_uppercase)
delims = ['>', '<', ':', '=', ',', ';']
class Lexer:
    def __init__(self, input_string):
        self.input_string = input_string
        self.current_state = 'H'
        self.current_token = ''
        self.tokens = []

    def is_number(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def add_token(self, token_type, value):
        self.tokens.append((token_type, value))
        self.current_token = ''

    def analyze(self):
        res = input_string.split()
        for i in res:
            if i in ('if', 'else', 'for', 'while', 'do'):
                self.current_token = i
                self.add_token('KEYWORD', self.current_token)
                # self.current_state = 'KEYWORD'
            elif i in (alphabetLC) or i in (alphabetUC):
                self.current_token = i
                self.add_token('ID', self.current_token)
                # self.current_state = 'ID'
            elif self.is_number(i):
                self.current_token = i
                self.add_token('NM', self.current_token)
                # self.current_state = 'NM'
            elif i == (':='):
                self.current_token = i
                self.add_token('ASGN', self.current_token)
                # self.current_state = 'ASGN'
            elif i in (delims):
                self.current_token = i
                self.add_token('DLM', self.current_token)
                # self.current_state = 'DLM'
            else:
                self.current_token = i
                self.add_token('ERR', self.current_token)
                # self.current_state = 'ERR'
        return self.tokens

# Пример использования:
input_string = "if x > 0 : y := 3.14 ; else : z := 2"
lexer = Lexer(input_string)
tokens = lexer.analyze()
for token in tokens:
    print(token)
