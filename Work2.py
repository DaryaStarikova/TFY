def calculate(expression):
    stack = []

    for token in expression.split():
        if token.isdigit() or (token[0] == '-' and token[1:].isdigit()):
            stack.append(int(token))
        elif token in ['+', '-', '*', '/']:
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            elif token == '/':
                if b == 0:
                    raise ZeroDivisionError("Деление на ноль")
                stack.append(a / b)
        else:
            raise ValueError("Недопустимый символ: {}".format(token))

    return stack[0]


input_expression = input("Введите алгебраическое выражение в обратной польской записи: ")
result = calculate(input_expression)
print("Результат вычислений:", result)
