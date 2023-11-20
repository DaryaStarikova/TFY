priority = {'+': 1, '-': 1, '*': 2, '/': 2, '(': 3, ')': 4}
str = []
stack = []

inp = input("Введите выражение: ")

for i in inp.split():
    if i.isdigit():
        str.append(i)
    elif i == '(':
        stack.append(i)
    elif i == ')':
        while stack[-1] != '(':
            str.append(stack[-1])
            stack.pop()
        stack.pop()
    elif i == '+' or i == '-' or i == '/' or i == '*':
        if len(stack) == 0:
            stack.append(i)
        elif stack:
            if priority[stack[-1]] >= priority[i] and stack[-1] != '(':
                while priority[stack[-1]] >= priority[i] and stack[-1] != '(':
                    str.append(stack[-1])
                    stack.pop()
                    if len(stack) == 0:
                        break
                stack.append(i)
            elif stack[-1] == '(':
                stack.append(i)
            else:
                stack.append(i)

while stack:
    str.append(stack[-1])
    stack.pop()

print("Выражение в обратной польской записи", str)


