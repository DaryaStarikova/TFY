class Token:
    def __init__(self, token_type, lexeme):
        self.token_type = token_type
        self.lexeme = lexeme

    def __str__(self):
        return f"Token({self.token_type}, '{self.lexeme}')"


from enum import Enum, auto


# Типы токенов
class TokenType(Enum):
    IDENTIFIER = auto()
    NUMBER = auto()
    FLOAT_NUMBER = auto()
    LOGICAL_CONST = auto()
    #LETTER = auto()
    WORD = auto()
    RELATION_OP = auto()  # операция сравнения
    LEFT_PAREN = auto()  # (
    RIGHT_PAREN = auto()  # )
    SEMICOLON = auto()  # ;
    KEYWORD = auto()
    LEFT_BRACE = auto()  # {
    RIGHT_BRACE = auto()  # }
    LEFT_BRACKET = auto()  # [
    RIGHT_BRACKET = auto()  # ]
    COMMENT = auto()
    HEXADECIMAL = auto()
    BINARY = auto()
    OCTAL = auto()
    COMMA = auto()  # ,
    PERIOD = auto()  # .
    COLON = auto()  # :


# Состояния лексического  анализатора
class State(Enum):
    H = 1
    DECIMAL_NUMBER = 2
    IDENTIFIER = 3
    DATA_TYPE = 4  # ключевые слова
    HEXADECIMAL = 5
    BINARY = 6
    OCTAL = 7
    ERROR = 8


# Присвоение каждому токену двухбуквенного значения
lexeme_table = {
    TokenType.IDENTIFIER: 'TI',
    TokenType.NUMBER: 'TN',
    TokenType.FLOAT_NUMBER: 'TN',
    TokenType.LOGICAL_CONST: 'TL',
    #TokenType.LETTER: 'TW',
    TokenType.WORD: 'TW',
    TokenType.RELATION_OP: 'TO',
    TokenType.LEFT_PAREN: 'TP',
    TokenType.RIGHT_PAREN: 'TP',
    TokenType.SEMICOLON: 'TS',
    TokenType.KEYWORD: 'TK',
    TokenType.LEFT_BRACE: 'TB',
    TokenType.RIGHT_BRACE: 'TB',
    TokenType.LEFT_BRACKET: 'TB',
    TokenType.RIGHT_BRACKET: 'TB',
    TokenType.COMMA: 'TC',
    TokenType.PERIOD: 'TP',
    TokenType.COLON: 'TC'
}

# Списки
number_tables = {
    'DECIMAL': [],
    'FLOAT_NUMBER': [],
    'HEXADECIMAL': [],
    'BINARY': [],
    'OCTAL': []
}

# Операции языка и описание типов данных
keyword_table = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'read': 'READ',
    'write': 'WRITE',
    'int': 'INT',
    'float': 'FLOAT',
    'bool': 'BOOL',
    'and': 'AND',
    'or': 'OR',
    '~': 'NOT',
    'true': 'TRUE',
    'false': 'FALSE'
}

# пункт 1 +
operator_table = {
    'plus': 'ADD_OP',  # сложение
    'min': 'ADD_OP',  # вычитание
    'or': 'ADD_OP',  # дизъюнкция
    'mult': 'MUL_OP',  # умножение
    'div': 'MUL_OP',  # деление
    'and': 'MUL_OP',  # конъюнкция
    '~': 'UNARY_OP',  # не
    'NE': 'RELATION_OP',  # неравно
    'EQ': 'RELATION_OP',  # равно
    'LT': 'RELATION_OP',  # меньше
    'LE': 'RELATION_OP',  # меньше или равно
    'GT': 'RELATION_OP',  # больше
    'GE': 'RELATION_OP'  # больше или равно
    # ... другие операторы, если есть ...
}

identifier_table = {}

# Установили соответствие между строковыми лексемами и типами токенов 
new_lexeme_table = {
    'IDENTIFIER': TokenType.IDENTIFIER,
    'NUMBER': TokenType.NUMBER,
    'LOGICAL_CONST': TokenType.LOGICAL_CONST,
    'if': TokenType.KEYWORD,
    'else': TokenType.KEYWORD,
    'while': TokenType.KEYWORD,
    'for': TokenType.KEYWORD,
    'read': TokenType.KEYWORD,
    'write': TokenType.KEYWORD,
    'int': TokenType.KEYWORD,
    'float': TokenType.KEYWORD,
    'bool': TokenType.KEYWORD,
    'and': TokenType.KEYWORD,
    'or': TokenType.KEYWORD,
    '~': TokenType.KEYWORD,
    'true': TokenType.KEYWORD,
    'false': TokenType.KEYWORD,
    '(': TokenType.LEFT_PAREN,
    ')': TokenType.RIGHT_PAREN,
    '[': TokenType.LEFT_BRACKET,
    ']': TokenType.RIGHT_BRACKET,
    '{': TokenType.LEFT_BRACE,
    '}': TokenType.RIGHT_BRACE,
    ',': TokenType.COMMA,
    ';': TokenType.SEMICOLON,
    '.': TokenType.PERIOD,
    ':': TokenType.COLON,
    '0b': TokenType.BINARY,
    '0o': TokenType.OCTAL,
    '0x': TokenType.HEXADECIMAL
}

# +
tokens = ['IDENTIFIER', 'plus', 'NUMBER', 'LT', 'NUMBER', 'or', 'LOGICAL_CONST']
current_token_index = 0


# Получить текущую лексему из списка токенов
def lexeme():
    global current_token_index
    if current_token_index < len(tokens):
        return tokens[current_token_index]
    else:
        return None  # Возвращает None, если достигнут конец списка лексем


# Получить следующий токен
def get_next_token():
    global current_token_index
    if current_token_index < len(tokens):
        current_token = tokens[current_token_index]
        current_token_index += 1
        return current_token
    else:
        return None  # Возвращает None, если достигнут конец списка лексем


# Проверка на одиночную букву
'''def is_letter(char):

    #return 'A' <= char <= 'Z' or 'a' <= char <= 'z'
    return len(char) == 1 and char.isalpha()
'''

# Проверка на цифру
def is_digit(char):
    return '0' <= char <= '9'


def error(message):
    print(f"Error: {message}")
    exit(1)  # Завершение выполнения программы с кодом ошибки 1


# Проверка на идентификатор
def identifier():
    lex = lexeme()
    if lex in keyword_table:
        print(Token(keyword_table[lex], lex))
    elif lex.isalpha():
        print(Token(TokenType.IDENTIFIER, lex))
    else:
        error("Invalid identifier")
    get_next_token()


# Определение типа числа (hex/bin/oct/dec)
def number():
    lex = lexeme()
    if lex.startswith(('0x', '0X')):
        hexadecimal()
    elif lex.startswith(('0b', '0B')):
        binary()
    elif lex.startswith(('0o', '0O')):
        octal()
    else:
        decimal()
    get_next_token()  # Переход к следующей лексеме


# Обработка двоичного числа
def binary():
    lex = lexeme()[:-1]  # Убираем символ обозначения двоичного числа (B/b)
    if all(bit in ('0', '1') for bit in lex):
        number = int(lex, 2)
        number_tables['BINARY'].append(number)  # Добавляем число в таблицу двоичных чисел
        lexeme_table[TokenType.BINARY] = 'TN'  # Обновляем таблицу лексем
    else:
        error("Invalid binary number format")  # Если есть символы, отличные от 0 и 1, вызываем ошибку
    get_next_token()  # Переход к следующей лексеме


# Обработка восьмеричного числа
def octal():
    lex = lexeme()  # получаем текущую лексему
    if lex.startswith('0o') or lex.startswith('0O'):
        if all(digit in '01234567' for digit in lex[2:]):
            number = int(lex, 8)
            number_tables['OCTAL'].append(number)  # Добавляем в таблицу восьмеричных чисел
            lexeme_table[TokenType.OCTAL] = 'TN'  # Обновляем таблицу лексем
        else:
            error("Incorrect octal number format")  # В противном случае, ошибка формата числа
    else:
        error("Incorrect octal number format")
    get_next_token()  # Переход к следующей лексеме


# Обработка десятичного числа
def decimal():
    lex = lexeme()
    if lex.isdigit():
        number = int(lex)
        number_tables['DECIMAL'].append(number)
        lexeme_table[TokenType.DECIMAL] = 'TN'
    else:
        error("Incorrect decimal format")
    get_next_token()


# Обработка шестнадцатеричного числа
def hexadecimal():
    lex = lexeme()[:-1]  # Убираем символ обозначения шестнадцатеричного числа (H/h)
    valid_hex_chars = '0123456789ABCDEFabcdef'
    if lex.startswith(('0x', '0X')):
        if all(char in valid_hex_chars for char in lex[2:]):
            number = int(lex, 16)
            number_tables['HEXADECIMAL'].append(number)  # Добавляем число в таблицу шестнадцатеричных чисел
            lexeme_table[TokenType.HEXADECIMAL] = 'TN'  # Обновляем таблицу лексем
        else:
            error("Invalid hexadecimal format")  # Если есть недопустимые символы, вызываем ошибку
    else:
        error("Invalid hexadecimal format")
    get_next_token()  # Переход к следующей лексеме


# Обработка логических констант (True/False)
def logical_constant():
    lex = lexeme()
    if lex == 'True' or lex == 'False':
        lexeme_table[lex] = TokenType.LOGICAL_CONST  # Добавляем логическую константу в таблицу лексем
    else:
        error("Expected boolean constant True or False")  # Если лексема не является логической константой, вызываем ошибку


class MultiLineCommentNode:
    def __init__(self, comment):
        self.comment = comment

    def __str__(self):
        return f"MultiLineCommentNode('{self.comment}')"



# Пункт 6 Многострочные комментарии
def multi_line_comment():
    if lexeme() == '{':
        get_next_token()
        comment = ''
        while lexeme() != '}':
            comment += lexeme() + " "
            get_next_token()
        get_next_token()  # Переходим к следующей лексеме после '}'
        return MultiLineCommentNode(comment)
    else:
        error("Syntax error: missing '{'")  # Ошибка в синтаксисе

def real():
    numerical_string()
    if lexeme() in {'E', 'e'}:
        get_next_token()
        if lexeme() in {'+', '-'}:
            get_next_token()
        numerical_string()


# Обработка числовой строки включая целую и десятичную часть (если она присутствует)
def numerical_string():
    if lexeme().isdigit():
        while lexeme().isdigit():
            get_next_token()
        if lexeme() == '.':
            get_next_token()
            while lexeme().isdigit():
                get_next_token()


# методы для ситаксического анализатора
# пункт 3
'''def program():
    if lexeme() == '{':
        get_next_token()
        while lexeme() != '}':
            if lexeme() == ';':
                get_next_token()
            elif lexeme() == 'IDENTIFIER' or lexeme() == 'NUMBER':
                # Оператор или описание
                description()  # Обработка описания или оператора
            else:
                error("Expected ';' or description/operator")  # Если не ';' и не описание/оператор, вызываем ошибку
        if lexeme() == '}':
            get_next_token()
        else:
            error("Missing closing curly brace '}'")  # Если нет закрывающей фигурной скобки, вызываем ошибку
    else:
        error("Missing opening curly brace '{'")  # Если нет открывающей фигурной скобки, вызываем ошибку


class Node:
    def __init__(self):
        pass

class DescriptionNode:
    def __init__(self, data_type, identifiers):
        self.data_type = data_type
        self.identifiers = identifiers


def data_description():
    data_type = lexeme()
    get_next_token()
    identifiers = []

    # Проверка наличия идентификаторов после типа данных
    while lexeme() == ',':
        get_next_token()
        if lexeme() == TokenType.IDENTIFIER:
            identifiers.append(lexeme())
            get_next_token()
        else:
            error("Expected IDENTIFIER after ',' in identifiers_list")

    # Создание узла синтаксического дерева
    description_node = DescriptionNode(data_type, identifiers)
    return description_node

def description():
    data_description()

class AssignmentNode:
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

def assignment():
    identifier = lexeme()
    identifier_node = Token(TokenType.IDENTIFIER, identifier)
    get_next_token()
    if lexeme() == 'as':
        get_next_token()
        expression_node = expression()  # Необходимо реализовать функцию expression
        return AssignmentNode(identifier_node, expression_node)
    else:
        error("Missing keyword 'as'")

class ConditionalNode:
    def __init__(self, condition, true_branch, false_branch=None):
        self.condition = condition  # выражение условия
        self.true_branch = true_branch  # оператор блока if
        self.false_branch = false_branch  # оператор блока else (может быть None)

def conditional():
    if lexeme() == 'if':
        get_next_token()
        condition = expression()  # Обработка условия
        if lexeme() == 'then':
            get_next_token()
            true_branch = program_operator()  # Обработка блока кода
            if lexeme() == 'else':
                get_next_token()
                false_branch = program_operator()  # Обработка блока кода else
                return ConditionalNode(condition, true_branch, false_branch)
            else:
                return ConditionalNode(condition, true_branch)
        else:
            error("Missing 'then' after condition")
    else:
        error("Condition not met 'if'")

class FixedLoopNode:
    def __init__(self, initialization, condition, operator):
        self.initialization = initialization  # оператор инициализации
        self.condition = condition  # условие цикла
        self.operator = operator  # оператор цикла

def fixed_loop():
    if lexeme() == 'for':
        get_next_token()
        initialization = assignment()  # Необходимо реализовать функцию assignment
        if lexeme() == 'to':
            get_next_token()
            condition = expression()  # Необходимо реализовать функцию expression
            if lexeme() == 'do':
                get_next_token()
                operator = program_operator()  # Необходимо реализовать функцию program_operator
                return FixedLoopNode(initialization, condition, operator)
            else:
                error("Missing 'do' after loop condition")
        else:
            error("Missing 'to' after initialization")
    else:
        error("'for' condition not met")

class ConditionalLoopNode:
    def __init__(self, condition, operator):
        self.condition = condition  # условие цикла
        self.operator = operator  # оператор цикла

def conditional_loop():
    if lexeme() == 'while':
        get_next_token()
        condition = expression()  # Необходимо реализовать функцию expression
        if lexeme() == 'do':
            get_next_token()
            operator = program_operator()  # Необходимо реализовать функцию program_operator
            return ConditionalLoopNode(condition, operator)
        else:
            error("Missing 'do' after loop condition")
    else:
        error("'while' condition failed")

class InputOpNode:
    def __init__(self, identifiers):
        self.identifiers = identifiers  # список идентификаторов для операции ввода

def input_op():
    if lexeme() == 'read':
        get_next_token()
        if lexeme() == '(':
            get_next_token()
            identifiers = []
            while lexeme() != ')':
                if lexeme() == 'IDENTIFIER':
                    identifiers.append(lexeme())
                    identifier_table[lexeme()] = TokenType.IDENTIFIER
                    get_next_token()
                    if lexeme() == ',':
                        get_next_token()
                    elif lexeme() != ')':
                        error("Syntax error: missing ')'")  # Ошибка в синтаксисе
                else:
                    error("ID expected")  # Ожидается идентификатор
            get_next_token()  # Переходим к следующей лексеме после ')'
            return InputOpNode(identifiers)
        else:
            error("Syntax error: missing '('")  # Ошибка в синтаксисе
    else:
        error("Error: Read operation 'read' was expected")  # Ошибка: ожидалась операция чтения 'read'

class OutputOpNode:
    def __init__(self, expressions):
        self.expressions = expressions  # список выражений для операции вывода

def output_op():
    if lexeme() == 'write':
        get_next_token()
        if lexeme() == '(':
            get_next_token()
            expressions = []
            while lexeme() != ')':
                expr = expression()  # Необходимо реализовать функцию expression
                expressions.append(expr)
                if lexeme() == ',':
                    get_next_token()
                elif lexeme() != ')':
                    error("Syntax error: missing ')'")  # Ошибка в синтаксисе
            get_next_token()  # Переходим к следующей лексеме после ')'
            return OutputOpNode(expressions)
        else:
            error("Syntax error: missing '('")  # Ошибка в синтаксисе
    else:
        error("Error: 'write' operation expected")  # Ошибка: ожидалась операция записи 'write'

def variable_declaration():
    data_type()
    identifiers_list()

def data_type():
    if lexeme() in ['int', 'float', 'bool']:
        lexeme_table[lexeme()] = TokenType.DATA_TYPE
        get_next_token()
    else:
        error("Data type is not as expected")  # Если тип данных не соответствует ожидаемым, вызываем ошибку

def identifiers_list():
    identifier()
    while lexeme() == ',':
        get_next_token()
        if lexeme() == 'IDENTIFIER':
            get_next_token()
        else:
            error("Expected IDENTIFIER after ',' in identifiers_list")


def program_operator():
    if lexeme() == '{':
        return compound()
    elif lexeme() == 'IDENTIFIER':
        return assignment()
    elif lexeme() == 'if':
        return conditional()
    elif lexeme() == 'for_fixed':
        return fixed_loop()
    elif lexeme() == 'for':
        return conditional_loop()
    elif lexeme() == 'input':
        return input_op()
    elif lexeme() == 'output':
        return output_op()
    elif lexeme() == 'int' or lexeme() == 'float' or lexeme() == 'bool':
        return description()
    else:
        error("None of the conditions are met")  # Если ни одно из условий не выполнено, вызываем ошибку
'''


class CompoundNode:
    def __init__(self, operators):
        self.operators = operators


# Обработка операторов внутри []
def compound():
    operators = []
    if lexeme() == '[':
        get_next_token()
        while lexeme() not in [']', 'EOF']:
            #operator = program_operator()
            #operators.append(operator)
            if lexeme() in [':', 'NEWLINE']:
                get_next_token()
            else:
                error("Missing ':' or newline")
        if lexeme() == ']':
            get_next_token()
            if lexeme() not in [':', 'NEWLINE']:
                error("Missing ':' or newline after last operator in compound")
        else:
            error("Missing closing square bracket ']'")
    else:
        error("Missing opening square bracket '['")

    return CompoundNode(operators)


# Константы и функции для обработки выражений
ADD_OPERATORS = {'plus', 'min', 'or'}
MUL_OPERATORS = {'mult', 'div', 'and'}
RELATIONAL_OPERATORS = {'NE', 'EQ', 'LT', 'LE', 'GT', 'GE'}


# Функции обработки математических выражений
# Умножение/деление
def term():
    factor()
    while lexeme() in MUL_OPERATORS:
        get_next_token()
        factor()


# Сложение/вычитание
def operand():
    term()
    while lexeme() in ADD_OPERATORS:
        get_next_token()
        term()


# Операторы отношения
def expression():
    operand()
    while lexeme() in RELATIONAL_OPERATORS:
        get_next_token()
        operand()


# Базовые элементы выражения (идентификаторы, числа, логические константы, скобки)
def factor():
    if lexeme() == 'IDENTIFIER':
        identifier()
    elif lexeme() == 'NUMBER':
        number()
    elif lexeme() == 'LOGICAL_CONST':
        logical_constant()
    elif lexeme() == 'UNARY_OP':
        get_next_token()
        factor()
    elif lexeme() == '(':
        get_next_token()
        expression()
        if lexeme() == ')':
            get_next_token()
        else:
            error("Missing closing bracket ')'")  # Если нет закрывающей скобки ')', вызываем ошибку
    else:
        error("Unidentified token")  # Если неопознанная лексема, вызываем ошибку


# Преобразование входной строки в токены
def tokenize_input(input_string):
    tokens = []
    current_token = ""
    i = 0
    while i < len(input_string):
        if input_string[i].isspace():
            if current_token:
                tokens.append(current_token)
                current_token = ""
        elif input_string[i:i + 2] == '{ ':
            if current_token:
                tokens.append(current_token)
                current_token = ""
            end_of_line = input_string.find('\n', i + 2)
            if end_of_line == -1:
                end_of_line = len(input_string)
            i = end_of_line if end_of_line != -1 else len(input_string)
        elif input_string[i:i + 2] == '{':
            if current_token:
                tokens.append(current_token)
                current_token = ""
            end_comment = input_string.find('}', i + 2)
            if end_comment == -1:
                print("Error: Unclosed multiline comment")
                return
            i = end_comment + 2
        elif input_string[i] in {'{ ', ' }', ';', '(', ')'}:
            if current_token:
                tokens.append(current_token)
                current_token = ""
            tokens.append(input_string[i])
        else:
            current_token += input_string[i]
            if current_token.startswith(('0o', '0O')):
                octal_number = current_token[2:]
                if all(d in '01234567' for d in octal_number):
                    tokens.pop()
                    tokens.append("Token(TokenType.OCTAL, '" + current_token + "')")
                    current_token = ""
        i += 1

    if current_token:
        tokens.append(current_token)

    return tokens


# Обработка ключевых слов
def handle_keywords(tokens):
    i = 0
    while i < len(tokens) - 1:
        if tokens[i].startswith("Token(TokenType.KEYWORD"):
            next_token = tokens[i + 1]
        i += 1

    return tokens


# Обработка лексем в соответствующие токены
def process_tokens(tokens):
    identifier_expected = False  # Флаг для ожидания идентификатора после ключевых слов
    for token in tokens:
        if not token.startswith("Token(TokenType.COMMENT"):
            if identifier_expected and token.isalpha():
                print(Token(TokenType.IDENTIFIER, token))
                identifier_expected = False
            elif token.isdigit():
                print(Token(TokenType.NUMBER, token))
                identifier_expected = False
            elif token.startswith(('0x', '0X')):
                print(Token(TokenType.HEXADECIMAL, token))
                identifier_expected = False
            elif token.startswith(('0b', '0B')):
                print(Token(TokenType.BINARY, token))
                identifier_expected = False
            elif token.startswith(('0o', '0O')) and all(d in '01234567' for d in token[2:]):
                print(Token(TokenType.OCTAL, token))
                identifier_expected = False
            elif token in operator_table:
                print(Token(operator_table[token], token))
                identifier_expected = False
                '''
            elif len(token) == 1 and token.isalpha():
                print(Token(TokenType.LETTER, token))
                identifier_expected = True
                '''
            elif token.isalpha():
                if token == 'true':
                    print(Token(TokenType.LOGICAL_CONST, token))
                    identifier_expected = False
                elif token == 'false':
                    print(Token(TokenType.LOGICAL_CONST, token))
                    identifier_expected = False
                elif token in keyword_table:
                    print(Token(TokenType.KEYWORD, token))
                    identifier_expected = True
                else:
                    print(Token(TokenType.IDENTIFIER, token))
                    identifier_expected = False
            elif '.' in token and token.replace('.', '').isdigit():
                print(Token(TokenType.FLOAT_NUMBER, token))
                identifier_expected = False
            else:
                if token.startswith("Token"):
                    print(token)
                elif token in new_lexeme_table:
                    print(Token(new_lexeme_table[token], token))
                    identifier_expected = False
                else:
                    print(Token(TokenType.IDENTIFIER, token))
                    identifier_expected = False

'''
def handle_identifiers(tokens):
    i = 0
    while i < len(tokens) - 1:
        if tokens[i].startswith("Token(TokenType.KEYWORD") and tokens[i + 1].isalnum():
            tokens[i + 1] = "Token(TokenType.IDENTIFIER, '" + tokens[i + 1] + "')"
        i += 1

    return tokens
'''

# Обработка входной строки 
def analyze_input(input_string):
    tokens = tokenize_input(input_string)
   # tokens = handle_identifiers(tokens)
    process_tokens(tokens)


# Пример использования
input_string = "x y" # синтаксис идент, идент, тип (x, y int)
analyze_input(input_string)

"int y { This is a multiline comment }"







"int x; int y; x = 123; y = 456; // Example"
"{ int x; int y; x = 5; y = 10; }"
"0 0xFF 0b1010 0765 true <= // Some comments"
"NE  EQ  LT  LE  GT  GE plus  min  or mult   //and not"
"true false"
"q a w s e d r f t g y h u j i k o l p z x c v b n m"
"Q A W S E D R F T G Y H U J I K O L P Z X C V B N M"
"0 1 2 3 4 5 6 7 8 9"
"( ) { } [ ] ; , ."
"int x;"
"float y;"
"x = 5;"
"y = 10.5;"

"""
int x;
int y;
x = 5;
y = 10.0;

if (x < y) {
x = x + 1;
} else {
y = y - 1;
}
"""

"""
int x;
x = 0;

for (x = 0; x < 5; x = x + 1) {
    x = x + 1;
}
"""

"input_string = "
"analyze_input(input_string)"

'''input_data = [
    "{ int x; int y; x = 5; y = 10; }",
    "0 0xFF 0b1010 0765 true <= // Some comments",
    "NE  EQ  LT  LE  GT  GE plus  min  or mult   //and not",
    "true false",
    "Q A W S E D R F T G Y H U J I K O L P Z X C V B N M",
    "q a w s e d r f t g y h u j i k o l p z x c v b n m",
    "0 1 2 3 4 5 6 7 8 9",
    "( ) { } [ ] ; , .",
    "{fbnjeafklwenklbgwkmjeowq",
     "fmjkewgjwomjwokhbowe}",
]
for statement in input_data:
    analyze_input(statement)'''