import re

keywords = ["for", "do"]


class Token:
    def __init__(self, token_name, token_value):
        self.token_name = token_name
        self.token_value = token_value


class LexemeTable:
    def __init__(self, tok, next=None):
        self.tok = tok
        self.next = next


lt = None  # переменная, представляющая текущий узел в связном списке
lt_head = None  # переменная, представляющая начало связного списка


def lexer(code):
    CS = 'H'  # начальное состояние
    i = 0
    code_length = len(code)  # длина строки входного кода

    while i < code_length:
        c = code[i]  # текущий символ

        if CS == 'H':
            while i < code_length and c.isspace():
                i += 1
                if i < code_length:
                    c = code[i]
            if re.match(r'[A-Za-z_]', c):  # если текущий символ является буквой
                CS = 'ID'
            elif re.match(r'[0-9.]|[+-]', c):
                CS = 'NM'
            elif c == ':':
                CS = 'ASGN'
            else:
                CS = 'DLM'

        if CS == 'ASGN':
            colon = c
            i += 1
            if i < code_length and code[i] == '=':
                tok = Token('OPER', ':=')  # создаем новый токен объект с типом OPER
                add_token(tok)  # добавляем токен в таблицу лексем
                i += 1
                CS = 'H'
            else:
                err_symbol = colon
                CS = 'ERR'

        if CS == 'DLM':
            if c in '();':
                tok = Token('DELIM', c)  # создаем новый токен объект с типом DELIM
                add_token(tok)
                i += 1
                CS = 'H'
            elif c in '<>=':
                tok = Token('OPER', c)  # создаем новый токен объект с типом OPER
                add_token(tok)
                i += 1
                CS = 'H'
            else:
                err_symbol = c
                i += 1
                CS = 'ERR'

        if CS == 'ERR':
            print(f"Unknown character: {err_symbol}")
            CS = 'H'

        if CS == 'ID':
            buf = c
            i += 1
            while i < code_length and re.match(r'[A-Za-z0-9_]', code[i]):
                buf += code[i]
                i += 1
            if is_kword(buf):  # если в буфере ключевое слово
                tok = Token('KWORD', buf)  # создаем новый токен объект с типом KWORD
            else:
                tok = Token('IDENT', buf)   # создаем новый токен объект с типом IDENT
            add_token(tok)
            CS = 'H'

        if CS == 'NM':
            buf = c
            i += 1
            while i < code_length and re.match(r'[0-9.FflL]', code[i]):
                buf += code[i]
                i += 1
            if is_num(buf):
                tok = Token('NUM', buf)
            else:
                tok = Token('ERR', buf)
            add_token(tok)
            CS = 'H'


def is_kword(id):
    return id in keywords


def is_num(num):
    num_pattern = r'^[+-]?\d+(\.\d*)?[FfLl]?$|^[+-]?\d*\.\d+[FfLl]?$'

    if re.match(num_pattern, num):
        return True
    return False


def add_token(tok):
    global lt, lt_head
    new_lexeme = LexemeTable(tok)
    if lt is None:
        lt = new_lexeme
        lt_head = new_lexeme
    else:
        lt.next = new_lexeme
        lt = new_lexeme


if __name__ == "__main__":
    code_input = "for i := 10F to 15.6 do print(i);"
    lexer(code_input)

    current = lt_head
    while current:
        token_name = ""
        if current.tok.token_name == 'KWORD':
            token_name = "Keyword"
        elif current.tok.token_name == 'IDENT':
            token_name = "Identifier"
        elif current.tok.token_name == 'NUM':
            token_name = "Number"
        elif current.tok.token_name == 'OPER':
            token_name = "Operator"
        elif current.tok.token_name == 'DELIM':
            token_name = "Delimiter"
        else:
            token_name = "Unknown"
        print(f"{token_name}: {current.tok.token_value}")
        current = current.next
