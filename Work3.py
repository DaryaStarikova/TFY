class Lexer:
    def __init__(self, input_string):
        self.input_string = input_string
        self.current_state = 'H'
        self.current_token = ''
        self.tokens = []

    def is_keyword(self, identifier):
        keywords = ['if', 'else', 'while', 'for']
        return identifier in keywords

    def is_number(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def add_token(self, token_type, value):
        self.tokens.append((token_type, value))
        self.current_token = ''

    def error(self):
        print(f"Error: Unrecognized symbol at state {self.current_state}")
        exit(1)

    def analyze(self):
        for char in self.input_string:
            if self.current_state != 'H':
                if self.current_state == 'ID':
                    if char.isalnum() or char == '_':
                        self.current_token += char
                    else:
                        if self.is_keyword(self.current_token):
                            self.add_token('KEYWORD', self.current_token)
                        else:
                            self.add_token('ID', self.current_token)
                        self.current_state = 'H'
                elif self.current_state == 'NM':
                    if char.isdigit() or char in '.eE+-':
                        self.current_token += char
                    else:
                        if self.is_number(self.current_token):
                            self.add_token('NUM', self.current_token)
                        else:
                            self.add_token('ERR', self.current_token)
                        self.current_state = 'H'
                elif self.current_state == 'ASGN':
                    if char == '=':
                        self.current_token += char
                        self.add_token('ASGN', self.current_token)
                        self.current_state = 'H'
                    else:
                        self.add_token('ERR', self.current_token)
                        self.current_state = 'H'

            if char.isspace():
                continue
            elif char == ':':
                self.current_state = 'ASGN'
                self.current_token = char
            elif char.isalpha() or char == '_':
                self.current_state = 'ID'
                self.current_token = char
            elif char == '+' or char == '-' or char.isdigit() or char == '.':
                self.current_state = 'NM'
                self.current_token = char
            elif char in '();=<>':
                self.add_token('DLM', char)
            else:
                self.error()

        if self.current_state == 'ID' and self.is_keyword(self.current_token):
            self.add_token('KEYWORD', self.current_token)
        elif self.current_state == 'NM' and self.is_number(self.current_token):
            self.add_token('NUM', self.current_token)
        elif self.current_state not in ['H', 'ASGN']:
            self.add_token('ERR', self.current_token)

        return self.tokens


# Пример использования:
input_string = "if x > 0: y := 3.14; else: z := 2"
lexer = Lexer(input_string)
tokens = lexer.analyze()

for token in tokens:
    print(token)
