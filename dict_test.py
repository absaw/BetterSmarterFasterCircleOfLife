import pickle
import numpy as np
import math
import networkx as nx
import matplotlib.pyplot as plt

# with open('StoredWeights/param_dict_2.pkl', 'rb') as handle:
#     data = handle.read()
# state_dict = pickle.loads(data)
# print(weight_dict["BW1"].shape)
# print(weight_dict["dBW1"].shape)
# print(weight_dict["BW2"].shape)
# print(weight_dict["dBW2"].shape)
# for value in weight_dict["X_train"]:
#     print(value) 
# for key,value in weight_dict.items():
#     print(key ," -- ", value)
#     print("\n\n")

# a=np.zeros([5,5])
# file = open("StoredData/test", "wb")
# # pickle.dump(a, file)
# a=pickle.loads(file)
# file.close()

# with open('StoredData/upartial_dataset5', 'rb') as handle:
#     data = handle.read()
# a = pickle.loads(data)
# # print(type(a))
# print(a.shape)
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
# def visualize_graph(self):
        # plt.figure(figsize=(2,2))
# pos=nx.circular_layout(G)
# nx.draw_networkx_nodes(G,pos=pos)
# nx.draw_networkx_edges(G, pos,connectionstyle="arc2,rad=0.5")
# nx.draw_networkx(G,pos=pos,with_labels=True,edge_color="Green")
# nx.draw_circular(G,with_labels=True)
nx.draw(G,with_labels=True)

plt.show()