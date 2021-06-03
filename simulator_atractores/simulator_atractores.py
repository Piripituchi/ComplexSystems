import itertools as it
import networkx as nx

import matplotlib.pyplot as plt
#import pygraphviz as pgv


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

dicc=[0,1]
long=8
lista=[list(elem) for elem in list(it.product(dicc,repeat=long))]
print(lista)

rule=decode_rules(54)

nodos=[]
aristas=[]

for vertice in lista:
    while True:
        next=[int(elem) for elem in next_state(rule,vertice)]
        verticeStr=int(''.join(map(str,vertice)),2)
        nextStr=int(''.join(map(str,next)),2)
        if (verticeStr,nextStr) in aristas:
            break
        nodos.append(verticeStr)
        aristas.append((verticeStr,nextStr))
        vertice=next

G=nx.DiGraph()
G.add_nodes_from(nodos)
G.add_edges_from(aristas)
pos=nx.spring_layout(G)

# A=nx.nx_agraph.to_agraph(G)
# A.layout('dot')
# pgv.Source(A.to_string())

nx.draw_networkx(G,pos,node_size=150,font_size=8, arrows=True, arrowsize=8)
plt.show()

print(nodos)
print('\n'*3)
print(aristas)
