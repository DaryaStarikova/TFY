def powerset(s):
    """
    Вспомогательная функция для построения всех подмножеств множества s.
    """
    result = [[]]
    for elem in s:
        result += [curr + [elem] for curr in result]
    return result[1:]

def nfa_to_dfa(states, alphabet, transitions, initial_states, final_states):
    dfa_states = []
    dfa_transitions = {}
    dfa_initial_states = []
    dfa_final_states = []

    # Построение всех подмножеств состояний НКА
    power_states = powerset(states)

    # Создание новых состояний ДКА
    for state_set in power_states:
        dfa_states.append("{" + ",".join(map(str, state_set)) + "}")

    # Построение функции переходов для ДКА
    for state_set in power_states:
        for symbol in alphabet:
            next_state_set = set()
            for state in state_set:
                for transition in transitions:
                    if transition[0] == state and transition[1] == symbol:
                        next_state_set.update(map(int, transition[2].strip('{}').split(',')))
            dfa_transitions[(str(state_set), symbol)] = "{" + ",".join(map(str, next_state_set)) + "}"

    # Определение начальных и конечных состояний ДКА
    for state_set in power_states:
        for state in state_set:
            if state in map(int, initial_states.split()):
                dfa_initial_states.append("{" + ",".join(map(str, state_set)) + "}")
                break
        if any(state in map(int, final_states.split()) for state in state_set):
            dfa_final_states.append("{" + ",".join(map(str, state_set)) + "}")

    # Вывод результата
    print("DFA:")
    print("Set of states:", ", ".join(dfa_states))
    print("Input alphabet:", ", ".join(alphabet))
    print("State-transitions function:")
    for key, value in dfa_transitions.items():
        print(f"D({key[0]}, {key[1]}) = {value}")
    print("Initial states:", ", ".join(dfa_initial_states))
    print("Final states:", ", ".join(dfa_final_states))


# Ввод данных
states = input("Enter set of states: ").split()
alphabet = input("Enter the input alphabet: ").split()
transitions = [tuple(input("Enter state-transitions function: ").split()) for _ in range(int(input("Enter the number of state-transitions: ")))]
initial_states = input("Enter a set of initial states: ")
final_states = input("Enter a set of final states: ")

# Преобразование НКА в ДКА
nfa_to_dfa(states, alphabet, transitions, initial_states, final_states)
