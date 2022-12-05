from Graph import *
from BFS import *
import random

class Predator:

    def __init__(self,n_nodes,G:nx.Graph):
        self.n_nodes=n_nodes
        self.position=random.randint(1,n_nodes)
        self.G=G
    #For normal predator which always moves towards agent
    def simulate_step(self,agent_pos):
    
        neighbor_list=list(self.G.neighbors(self.position))
        degree=self.G.degree(self.position)
        shortest_path_list=[]
        shortest_path_len_list=[]
        for neighbor in neighbor_list:
            bfs_result=get_bfs_path(self.G, neighbor, agent_pos)
            if bfs_result[0]:
                shortest_path_list.append(bfs_result[1])
                shortest_path_len_list.append(len(bfs_result[1]))
            else:
                continue
        
        min_path_len=min(shortest_path_len_list)
        min_path_list=[node for node in shortest_path_list if len(node)==min_path_len]
        shortest_path=random.choice(min_path_list)
        next_pos=shortest_path[0]#neighbor with the shortest path length
        self.position=next_pos
    
    #For distracted predator which moves towards agent with probability 0.6 and randomly with a probability 0.4
    def simulate_step_distracted(self,agent_pos):

        prob=random.random()
        if prob<=0.6:
            neighbor_list=list(self.G.neighbors(self.position))
            shortest_path_list=[]
            shortest_path_len_list=[]
            for neighbor in neighbor_list:
                bfs_result=get_bfs_path(self.G, neighbor, agent_pos)
                if bfs_result[0]:
                    shortest_path_list.append(bfs_result[1])
                    shortest_path_len_list.append(len(bfs_result[1]))
                else:
                    continue
            
            min_path_len=min(shortest_path_len_list)
            min_path_list=[node for node in shortest_path_list if len(node)==min_path_len]
            shortest_path=random.choice(min_path_list)
            next_pos=shortest_path[0]#neighbor with the shortest path length
        else:
            neighbor_list=list(self.G.neighbors(self.position))
            next_pos=random.choice(neighbor_list)
            
        self.position=next_pos
        # return next_pos

#Test predator

if __name__=="__main__":
    G=generate_graph(20)
    p=Predator(20, G)
    print("Init Pos ->",p.position)
    print("Neighbors -> ",*list(G.neighbors(p.position)))
    print("SPP - > ",get_bfs_path(G, p.position, 10)[1])
    print()
    for i in range(1,101):
        p.simulate_step(10)
        print("i = ",i," - Predator = ",p.position)
        print("Neighbors -> ",*list(G.neighbors(p.position)))

        if p.position==10:
            print("Agent Caught!")
            break
        print()
    visualize_graph(G)
    





