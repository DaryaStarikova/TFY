from typing import NamedTuple
import re

class Token:
    def __init__(self, token_name, token_value):
        self.token_name = token_name
        self.token_value = token_value
    def __repr__(self):
        return f"{self.token_name} ::= {self.token_value}"


class States(NamedTuple):
    H: str
    COMM: str
    ID: str
    ERR: str
    NM: str
    DLM: str


class Tokens(NamedTuple):
    KWORD: str
    IDENT: str
    NUM: str
    OPER: str
    DELIM: str
    NUM2: str
    NUM8: str
    NUM10: str
    NUM16: str
    REAL: str
    TYPE: str
    ARITH: str


class Current:
    def __init__(self, symbol: str = "", eof_state: bool = False, line_number: int = 0, pos_number: int = 0, state: str = ""):
        self.symbol = symbol
        self.eof_state = eof_state
        self.line_number = line_number
        self.pos_number = pos_number
        self.state = state

    def re_assign(self, symbol: str, eof_state: bool, line_number: int, pos_number: int):
        self.symbol = symbol
        self.eof_state = eof_state
        self.line_number = line_number
        self.pos_number = pos_number


class Error:
    def __init__(self, filename: str, symbol: str = "", line: int = 0, pos_in_line: int = 0):
        self.filename = filename
        self.symbol = symbol
        self.line = line
        self.pos_in_line = pos_in_line

def fgetc_generator(filename: str):
    with open(filename) as fin:
        s = list(fin.read())
        s.append('\n')
        counter_pos, counter_line = 1, 1
        for i in range(len(s)):
            yield s[i], s[i] == "@", counter_line, counter_pos
            if s[i] == "\n":
                counter_pos = 0
                counter_line += 1
            else:
                counter_pos += 1

class LexicalAnalyzer:
    def __init__(self, filename: str, identifiersTable):
        self.identifiersTable = identifiersTable
        self.states = States("H", "COMM", "ID", "ERR", "NM", "DLM")
        self.token_names = Tokens("KWORD", "IDENT", "NUM", "OPER", "DELIM", "NUM2", "NUM8", "NUM10", "NUM16", "REAL",
                                  "TYPE", "ARITH")
        self.keywords = {"or": 1, "and": 2, "~": 3, "program": 4, "var": 5, "begin": 6, "end": 7, "as": 8, "if": 9,
                         "then": 10, "else": 11, "for": 12, "to": 13, "do": 14, "while": 15, "read": 16, "write": 17,
                         "true": 18, "false": 19}
        self.types = {"int", "float", "bool"}  # +
        self.arith = {"plus", 'min', 'mult', 'div'}  # +
        self.operators = {"NE", "EQ", "LT", "LE", "GT", "GE"}  # +
        self.delimiters = {";", ",", ":", "[", "]", "(", ")"}
        self.fgetc = fgetc_generator(filename)
        self.current = Current(state=self.states.H)
        self.error = Error(filename)
        self.lexeme_table = []

    def analysis(self):
        self.current.state = self.states.H
        self.current.re_assign(*next(self.fgetc))
        while not self.current.eof_state:
            if self.current.state == self.states.H:
                self.h_state_processing()
            elif self.current.state == self.states.COMM:
                self.comm_state_processing()
            elif self.current.state == self.states.ID:
                self.id_state_processing()
            elif self.current.state == self.states.ERR:
                self.err_state_processing()
            elif self.current.state == self.states.NM:
                self.nm_state_processing()
            elif self.current.state == self.states.DLM:
                self.dlm_state_processing()

    def h_state_processing(self):
        while not self.current.eof_state and self.current.symbol in {" ", "\n", "\t"}:
            self.current.re_assign(*next(self.fgetc))
        if self.current.symbol.isalpha():  # переход в состояние идентификаторов
            self.current.state = self.states.ID
        elif self.current.symbol == "~":  # переход в состояние идентификаторов для обработки "~"
            self.current.state = self.states.ID
        elif self.current.symbol in set(list("0123456789.")):  # переход в состояние чисел
            self.current.state = self.states.NM
        elif self.current.symbol in (self.delimiters | self.operators | self.types | self.arith):
            self.current.state = self.states.DLM
        elif self.current.symbol == "{":
            self.current.state = self.states.COMM
        else:
            self.current.state = self.states.ERR

    def comm_state_processing(self):
        while not self.current.eof_state and self.current.symbol != "}":
            self.current.re_assign(*next(self.fgetc))
        if self.current.symbol == "}":
            self.current.state = self.states.H
            if not self.current.eof_state:
                self.current.re_assign(*next(self.fgetc))
        else:
            self.error.symbol = self.current.symbol
            self.current.state = self.states.ERR

    def dlm_state_processing(self):
        if self.current.symbol in ["p", "m"]:
            buf = [self.current.symbol]
            if not self.current.eof_state:
                self.current.re_assign(*next(self.fgetc))

            while not self.current.eof_state and self.current.symbol.isalpha():
                buf.append(self.current.symbol)
                self.current.re_assign(*next(self.fgetc))

            buf = ''.join(buf)
            if buf in self.arith:
                self.add_token(self.token_names.ARITH, buf)
                self.current.state = self.states.H
            else:
                self.current.state = self.states.ERR
        if self.current.symbol in self.delimiters | self.arith | self.types:
            if self.current.symbol in self.delimiters:
                self.add_token(self.token_names.DELIM, self.current.symbol)
            elif self.current.symbol in self.types:
                self.add_token(self.token_names.TYPE, self.current.symbol)
            else:
                self.add_token(self.token_names.ARITH, self.current.symbol)
            if not self.current.eof_state:
                self.current.re_assign(*next(self.fgetc))
        else:
            temp_symbol = self.current.symbol
            if not self.current.eof_state:
                self.current.re_assign(*next(self.fgetc))
                if temp_symbol + self.current.symbol in self.operators:
                    self.add_token(self.token_names.OPER, temp_symbol + self.current.symbol)
                    if not self.current.eof_state:
                        self.current.re_assign(*next(self.fgetc))
                else:
                    self.add_token(self.token_names.OPER, temp_symbol)
            else:
                self.add_token(self.token_names.OPER, self.current.symbol)
        self.current.state = self.states.H

    def err_state_processing(self):
        raise Exception(
            f"\nUnknown: '{self.error.symbol}' in file {self.error.filename} \nline: {self.current.line_number} and pos: {self.current.pos_number}")

    def id_state_processing(self):
        buf = [self.current.symbol]
        if not self.current.eof_state:
            self.current.re_assign(*next(self.fgetc))

        while not self.current.eof_state and (self.current.symbol.isalpha() or self.current.symbol.isdigit()):
            buf.append(self.current.symbol)
            self.current.re_assign(*next(self.fgetc))

        buf = ''.join(buf)
        if buf in self.keywords:  # Проверка на ключевое слово
            self.add_token(self.token_names.KWORD, buf)
        elif buf in self.types:  # Проверка на тип данных
            self.add_token(self.token_names.TYPE, buf)
        elif buf in self.arith:  # Проверка на арифметическую операцию
            self.add_token(self.token_names.ARITH, buf)
        elif buf in self.operators:  # Проверка на оператор
            self.add_token(self.token_names.OPER, buf)
        else:
            self.add_token(self.token_names.IDENT, buf)
            if buf not in self.keywords:
                self.identifiersTable.put(buf)

        self.current.state = self.states.H

    def nm_state_processing(self):
        buf = []
        buf.append(self.current.symbol)
        if not self.current.eof_state:
            self.current.re_assign(*next(self.fgetc))
        while not self.current.eof_state and (self.current.symbol in set(list("ABCDEFabcdefoOdDhH0123456789.eE+-"))):
            buf.append(self.current.symbol)
            self.current.re_assign(*next(self.fgetc))

        buf = ''.join(buf)
        is_n, token_num = self.is_num(buf)
        if is_n:
            self.add_token(token_num, buf)
            self.current.state = self.states.H
        else:
            self.error.symbol = buf

            self.current.state = self.states.ERR

    def is_num(self, digit):
        if re.match(r"^\d+(\.\d*)?(eplus[+-]?\d+)?$|^\d*\.\d+(eplus[+-]?\d+)?$", digit):
            digit = re.sub(r'eplus', 'e+', digit)
            return True, self.token_names.REAL
        elif re.match(r"^[01]+[Bb]$", digit):
            return True, self.token_names.NUM2
        elif re.match(r"^[01234567]+[Oo]$", digit):
            return True, self.token_names.NUM8
        elif re.match(r"^\d+[dD]?$", digit):
            return True, self.token_names.NUM10
        elif re.match(r"^\d[0-9ABCDEFabcdef]*[Hh]$", digit):
            return True, self.token_names.NUM16

        return False, False

    def is_keyword(self, word):
        if word in self.keywords:
            return True
        return False

    def add_token(self, token_name, token_value):
        self.lexeme_table.append(Token(token_name, token_value))

class TableRow(NamedTuple):
    was_described: bool
    identifier_type: str
    number: int
    address: int


class IdentifiersTable:
    def __init__(self):
        self.table = {}
        self.n = 0

    def throw_error(self, lex):
        raise Exception(
            f"\nIdentifier '{lex}' error")

    def put(self, identifier, was_described=False, identifier_type=None, address=0):
        if identifier not in self.table:
            self.table[identifier] = TableRow(was_described, identifier_type, self.n + 1, address)
            self.n += 1
        elif identifier in self.table and not self.table[identifier].was_described:
            self.table[identifier] = TableRow(was_described, identifier_type, self.table[identifier].number, address)
        elif identifier in self.table and self.table[identifier].was_described:
            self.throw_error(identifier)


    def __repr__(self):
        res = ["\nTable of Identifiers:"]
        for k, v in self.table.items():
            res.append(f'{k} {v}')
        return "\n".join(res)

    def check_if_all_described(self):
        for k, v in self.table.items():
            if not v.was_described:
                self.throw_error(k)

class SyntacticalAnalyzer:
    def __init__(self, lexeme_table, identifiersTable):
        self.identifiersTable = identifiersTable
        self.lex_get = self.lexeme_generator(lexeme_table)
        self.id_stack = []
        self.current_lex = next(self.lex_get)
        self.relation_operations = {"NE", "EQ", "LT", "LE", "GT", "GE"}
        self.term_operations = {"plus", "min", "or"}
        self.factor_operations = {"mult", "div", "and"}
        self.keywords = {"or": 1, "and": 2, "~": 3, "program": 4, "var": 5, "begin": 6, "end": 7, "as": 8, "if": 9,
                         "then": 10, "else": 11, "for": 12, "to": 13, "do": 14, "while": 15, "read": 16, "write": 17,
                         "true": 18, "false": 19}

    def equal_token_value(self, word):
        if self.current_lex.token_value != word:
            self.throw_error()
        self.current_lex = next(self.lex_get)

    def equal_token_name(self, word):
        if self.current_lex.token_name != word:
            self.throw_error()
        self.current_lex = next(self.lex_get)

    def throw_error(self):
        raise Exception(
            f"\nError in lexeme: '{self.current_lex.token_value}'")

    def lexeme_generator(self, lexeme_table):
        for i, token in enumerate(lexeme_table):
            yield token

    def PROGRAMM(self):  # <программа>::= program var <описание> begin <оператор> {; <оператор>} end
        self.equal_token_value("program")
        self.equal_token_value("var")
        self.DESCRIPTION()
        self.equal_token_value("begin")
        self.OPERATOR()

        while self.current_lex.token_value == ";":
            self.current_lex = next(self.lex_get)
            self.OPERATOR()

        if self.current_lex.token_value != "end":
            self.throw_error()

    def DESCRIPTION(self):  # <описание>::= {<идентификатор> {, <идентификатор> } : <тип> ;}
        while self.current_lex.token_value != "begin":
            self.IDENTIFIER(from_description=True)
            while self.current_lex.token_value == ",":
                self.current_lex = next(self.lex_get)
                self.IDENTIFIER(from_description=True)
            self.equal_token_value(":")

            self.TYPE(from_description=True)
            self.equal_token_value(";")

    def IDENTIFIER(self, from_description=False):
        if from_description:
            if self.current_lex.token_name != "IDENT":
                self.throw_error()
            self.id_stack.append(self.current_lex.token_value)
            self.current_lex = next(self.lex_get)
        else:
            self.equal_token_name("IDENT")

    def TYPE(self, from_description=False):
        if from_description:
            if self.current_lex.token_name != "TYPE":
                self.throw_error()
            for item in self.id_stack:
                if item not in self.keywords:
                    self.identifiersTable.put(item, True, self.current_lex.token_value)
            self.id_stack = []
            self.current_lex = next(self.lex_get)
        else:
            self.equal_token_name("TYPE")

    def OPERATOR(self):
        if self.current_lex.token_value == "[":
            self.COMPOSITE_OPERATOR()
        elif self.current_lex.token_value == "if":
            self.CONDITIONAL_OPERATOR()
        elif self.current_lex.token_value == "for":
            self.FIXED_CYCLE_OPERATOR()
        elif self.current_lex.token_value == "while":
            self.CONDITIONAL_CYCLE_OPERATOR()
        elif self.current_lex.token_value == "read":
            self.INPUT_OPERATOR()
        elif self.current_lex.token_value == "write":
            self.OUTPUT_OPERATOR()
        else:
            self.ASSIGNMENT_OPERATOR()

    def COMPOSITE_OPERATOR(self):
        self.equal_token_value("[")
        self.OPERATOR()

        while self.current_lex.token_value in {"\n", ":"}:
            self.current_lex = next(self.lex_get)
            self.OPERATOR()

        self.equal_token_value("]")

    def CONDITIONAL_OPERATOR(self):
        self.equal_token_value("if")
        self.EXPRESSION()
        self.equal_token_value("then")
        self.OPERATOR()

        if self.current_lex.token_value == "else":
            self.current_lex = next(self.lex_get)
            self.OPERATOR()

    def FIXED_CYCLE_OPERATOR(self):
        self.equal_token_value("for")
        self.ASSIGNMENT_OPERATOR()
        self.equal_token_value("to")
        self.EXPRESSION()
        self.equal_token_value("do")
        self.OPERATOR()

    def CONDITIONAL_CYCLE_OPERATOR(self):
        self.equal_token_value("while")
        self.EXPRESSION()
        self.equal_token_value("do")
        self.OPERATOR()

    def INPUT_OPERATOR(self):
        self.equal_token_value("read")
        self.equal_token_value("(")
        self.IDENTIFIER()
        while self.current_lex.token_value == ",":
            self.current_lex = next(self.lex_get)
            self.IDENTIFIER()
        self.equal_token_value(")")

    def OUTPUT_OPERATOR(self):
        self.equal_token_value("write")
        self.equal_token_value("(")
        self.EXPRESSION()
        while self.current_lex.token_value == ",":
            self.current_lex = next(self.lex_get)
            self.EXPRESSION()
        self.equal_token_value(")")

    def ASSIGNMENT_OPERATOR(self):
        self.IDENTIFIER()
        self.equal_token_value("as")
        self.EXPRESSION()

    def EXPRESSION(self):
        self.OPERAND()
        while self.current_lex.token_value in self.relation_operations:
            self.current_lex = next(self.lex_get)
            self.OPERAND()

    def OPERAND(self):
        self.TERM()
        while self.current_lex.token_value in self.term_operations:
            self.current_lex = next(self.lex_get)
            self.TERM()

    def TERM(self):
        self.FACTOR()
        while self.current_lex.token_value in self.factor_operations:
            self.current_lex = next(self.lex_get)
            self.FACTOR()

    def FACTOR(self):
        if self.current_lex.token_name in {"IDENT", "NUM", "NUM2", "NUM8", "NUM10", "NUM16",
                                           "REAL"}:  # <идентификатор> | <число>
            self.current_lex = next(self.lex_get)
        elif self.current_lex.token_value in {"true", "false"}:  # <логическая_константа>
            self.current_lex = next(self.lex_get)
        elif self.current_lex.token_value == "~":  # <унарная_операция> <множитель>
            self.equal_token_value("~")
            self.FACTOR()
        else:  # «(»<выражение>«)»
            self.equal_token_value("(")
            self.EXPRESSION()
            self.equal_token_value(")")

PRINT_INFO = True
PATH_TO_PROGRAM = "test.txt"


def main():
    identifiersTable = IdentifiersTable()
    lexer = LexicalAnalyzer(PATH_TO_PROGRAM, identifiersTable)
    lexer.analysis()
    if lexer.current.state != lexer.states.ERR:
        if PRINT_INFO:
            print("Result of Lexical Analyzer:")
            for i in lexer.lexeme_table:
                print(f"{i.token_name} {i.token_value}")


        syntaxAnalyzer = SyntacticalAnalyzer(lexer.lexeme_table, identifiersTable)
        syntaxAnalyzer.PROGRAMM()
        identifiersTable.check_if_all_described() # проверка что все Id описаны
        if PRINT_INFO:
            print(identifiersTable)
        print("+---------+")
        print("| SUCCESS |")
        print("+---------+")

if __name__ == "__main__":
    main()