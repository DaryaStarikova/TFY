# вычисляет эпсилон-замыкание набора состояний в NFA (добавляет состояния, достижимые посредством эпсилон-переходов)
def epsilon_closure(states, transitions, epsilon='eps'):
    closure = set(states)  # начальный набор состояний
    stack = list(states)  # стек инициализируется начальным набором
    while stack:
        state = stack.pop()  # извлекаем состояние из стека
        # перебор всех переходов NFA
        for transition in transitions:
            # если есть эпсилон-переход из текущего состояния
            if transition[0] == state and transition[1] == epsilon:
                # если состояние после эпсилон-перехода не в замыкании
                if transition[2] not in closure:
                    closure.add(transition[2])
                    stack.append(transition[2])
    return closure


# вычисляет множество состояний, в которые можно перейти из заданного множества states по заданному символу symbol
def move(states, transitions, symbol):
    result = set()  # пустое множество, в которое будут добавляться состояния после переходов
    for state in states:
        for transition in transitions:
            if transition[0] == state and transition[1] == symbol:
                result.add(transition[2])
    return result


# выполняет преобразование NFA в DFA с использованием метода построения подмножества
def nfa_to_dfa(states, alphabet, transitions, initial_states, final_states):
    dfa_states = []  # список состояний DFA
    dfa_transitions = []  # список переходов DFA
    dfa_initial_state = frozenset(epsilon_closure(initial_states, transitions))  # начальное состояние DFA
    dfa_states.append(dfa_initial_state)
    stack = [dfa_initial_state]

    while stack:
        current_dfa_state = stack.pop()
        # перебор символов в алфавите
        for symbol in alphabet:
            # переход к новому состоянию с учетом эпсилон-замыкания
            next_nfa_state = epsilon_closure(move(current_dfa_state, transitions, symbol), transitions)
            # если новое состояние не встречается во множестве состояний DFA
            if next_nfa_state not in dfa_states:
                dfa_states.append(next_nfa_state)
                stack.append(next_nfa_state)
            # добавляем переход во множество переходов DFA
            dfa_transitions.append((current_dfa_state, symbol, next_nfa_state))
    # рассчитываем множество конечных результатов DFA
    dfa_final_states = [state for state in dfa_states if any(s in state for s in final_states)]

    return dfa_states, alphabet, dfa_transitions, dfa_initial_state, dfa_final_states


def main():
    states = input("Enter set of states: ").split()
    alphabet = input("Enter the input alphabet: ").split()
    transitions_input = input("Enter state-transitions function (current state, input character, next state): ").split()
    transitions = [tuple(t.strip()[1:-1].split(',')) for t in transitions_input]
    initial_states = input("Enter a set of initial states: ").split()
    final_states = input("Enter a set of final states: ").split()

    dfa_states, dfa_alphabet, dfa_transitions, dfa_initial_state, dfa_final_states = nfa_to_dfa(
        states, alphabet, transitions, initial_states, final_states)

    # Преобразование набороров состояний в строковый вид
    dfa_states_str = [''.join(sorted(state)) for state in dfa_states]
    dfa_final_states_str = [''.join(sorted(state)) for state in dfa_final_states]

    print("DFA:")
    print("Set of states: " + ', '.join(dfa_states_str))
    print("Input alphabet: " + ', '.join(dfa_alphabet))
    print("State-transitions function:")
    for transition in dfa_transitions:
        current_state = ''.join(sorted(transition[0]))
        next_state = ''.join(sorted(transition[2]))
        print(f'D({current_state}, {transition[1]}) = {next_state}')
    initial_state_str = ''.join(sorted(dfa_initial_state))
    print("Initial states: " + initial_state_str)
    print("Final states: " + ', '.join(dfa_final_states_str))


if __name__ == "__main__":
    main()
