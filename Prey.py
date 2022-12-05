from Graph import *
from BFS import *
import random

class Prey:
    
    def __init__(self,n_nodes,G : nx.Graph):
        self.n_nodes=n_nodes
        self.position=random.randint(1,n_nodes)
        self.G=G
    
    def simulate_step(self):
        neighbor_list=list(self.G.neighbors(self.position))
        next_pos=random.choice(neighbor_list+[self.position])
        self.position=next_pos
        return next_pos
            
#Testing prey
if __name__=="__main__":
    self.G=generate_graph(50)
    p=Prey(50, self.G)
    print("Init Pos ->",p.position)
    print("Neighbors -> ",*list(self.G.neighbors(p.position)))
    print()
    for i in range(1,101):
        p.simulate_step()
        print("i = ",i," - Prey = ",p.position)
        print("Neighbors -> ",*list(self.G.neighbors(p.position)))
        print()






