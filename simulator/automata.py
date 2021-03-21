import matplotlib.pyplot as plt
import numpy as np


    # rules=[
    #     [0,0,0]
    #     [0,0,1]
    #     [0,1,0]
    #     [0,1,1]
    #     [1,0,0]
    #     [1,0,1]
    #     [1,1,0]
    #     [1,1,1]
    # ]

def decode_rules(n_rule):
    rules=[
        [0,0,0],
        [0,0,1],
        [0,1,0],
        [0,1,1],
        [1,0,0],
        [1,0,1],
        [1,1,0],
        [1,1,1],
    ]
    binary_rule=str(bin(n_rule)).lstrip("0b")[::-1]
    for i in range(0,len(rules)):
        if i<len(binary_rule):
            rules[i].insert(3,binary_rule[i])
        else:
            rules[i].insert(3,0)
    return rules

def next_state(rules,last_state):
    new_state=[]
    for center_cell in range(0,len(last_state)):
        left_cell=center_cell-1
        right_cell=center_cell+1
        if left_cell < 0:
            left_cell=len(last_state)-1
        if right_cell == len(last_state):
            right_cell=0
        current_state=[last_state[left_cell],last_state[center_cell],last_state[right_cell]]
        for pattern in range(0,len(rules)):
            if current_state == rules[pattern][0:3:]:
                new_state.append(rules[pattern][3])
                break
    return new_state

def create_automata(initial_state,rules,time):
    ac_grid=np.zeros((time,len(initial_state)),dtype=int)
    ac_grid[0]=initial_state
    for t_state in range(1,time):
        ac_grid[t_state]=next_state(rules, initial_state)
        initial_state=ac_grid[t_state]
    return ac_grid

def draw_user_automata(automata):
    img=plt.imshow(automata, cmap="binary", aspect="equal")
    plt.title("RANDOM")
    return img


probe_state=[1,0,0,1,1,1,0,0,1,1,0,1,0,1,0,0,0,1,1,0,0,1,0,0,0]
probe_state_1=[0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0]
rule_array=decode_rules(30)
t=50
automata=create_automata(probe_state,rule_array,t)
automata1=create_automata(probe_state_1,rule_array,t)
plt.figure(figsize=(8,6))

#plot 1:

plt.subplot(1, 2, 1)
plt.imshow(automata, cmap="binary", aspect="equal")
plt.title("RANDOM")

#plot 2:

plt.subplot(1, 2, 2)
plt.imshow(automata1, cmap="binary", aspect="equal")
plt.title("CADENA 1 EN MEDIO")
plt.suptitle("AUTOMATAS CELULARES")
plt.show()





