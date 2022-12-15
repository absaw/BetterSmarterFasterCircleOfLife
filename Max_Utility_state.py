import pickle
import numpy as np
import math
import networkx as nx
import matplotlib.pyplot as plt
with open('/Users/abhishek.sawalkar/Library/Mobile Documents/com~apple~CloudDocs/AI Project/BetterSmarterFasterCircleOfLife/StoredUtilities/Graph1_Utility6.pkl', 'rb') as handle:
    data = handle.read()
state_dict = pickle.loads(data)
G = nx.read_gpickle("/Users/abhishek.sawalkar/Library/Mobile Documents/com~apple~CloudDocs/AI Project/BetterSmarterFasterCircleOfLife/StoredGraph/Graph1.gpickle")


m=-1

for key,value in state_dict.items():
    if m<value and not math.isinf(value):
        m=value
        state=key
print(m)
print(state)
agent=state[0]
prey=state[1]
predator=state[2]
print("Neighbors of Agent->",list(G.neighbors(agent)))
print("Neighbors of Prey->",list(G.neighbors(prey)))
print("Neighbors of Predator->",list(G.neighbors(predator)))

nx.draw(G,with_labels=True)

plt.show()