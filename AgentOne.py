from Graph import *
from BFS import *
from Prey import *
from Predator import *

class AgentOne:
    
    def __init__(self,n_nodes,G : nx.Graph,prey:Prey, predator:Predator):
        self.n_nodes=n_nodes

        ag_not_decided=True
        while ag_not_decided:
            self.position=random.randint(1, n_nodes)
            if self.position!=prey.position and self.position != predator.position:
                ag_not_decided=False

        self.G=G

    def simulate_step(self,prey : Prey,predator:Predator):
        
        d_prey=len(get_bfs_path(self.G, self.position, prey.position)[1])     #Distance from prey
        d_predator=len(get_bfs_path(self.G, self.position, predator.position)[1])  #Distance from predator

        neighbor_list=list(self.G.neighbors(self.position))
        
        # print("Distance From Prey = ",d_prey)
        # print("Distance from Pred =",d_predator)
        # print("Current Position = ",self.position)
        # print("Neighbor List = ",neighbor_list)

        cost_matrix={}
        for neighbor in neighbor_list:
            c_prey=len(get_bfs_path(self.G, neighbor, prey.position)[1])
            c_predator=len(get_bfs_path(self.G, neighbor, predator.position)[1])
            cost_matrix[neighbor]=[c_prey,c_predator]
        l1=[]
        for neighbor in neighbor_list:
            if cost_matrix[neighbor][0]<d_prey and cost_matrix[neighbor][1]>d_predator:
                l1.append(neighbor)

        if not l1:
            
            l2=[]
            for neighbor in neighbor_list:
                if cost_matrix[neighbor][0]<d_prey and cost_matrix[neighbor][1]==d_predator:
                    l2.append(neighbor)

            if not l2:
                l3=[]
                for neighbor in neighbor_list:
                    if cost_matrix[neighbor][0]==d_prey and cost_matrix[neighbor][1]>d_predator:
                        l3.append(neighbor)
                
                if not l3:
                    l4=[]
                    for neighbor in neighbor_list:
                        if cost_matrix[neighbor][0]==d_prey and cost_matrix[neighbor][1]==d_predator:
                            l4.append(neighbor)
                    
                    if not l4:
                        l5=[]
                        for neighbor in neighbor_list:
                            if cost_matrix[neighbor][1]>d_predator:
                                l5.append(neighbor)
                        
                        if not l5:
                            l6=[]
                            for neighbor in neighbor_list:
                                if cost_matrix[neighbor][1]==d_predator:
                                    l6.append(neighbor)

                            if not l6:
                                #sit still and pray
                                next_position=self.position
                            else:
                                next_position=random.choice(l6)
                                #print(l6)

                        else:
                            next_position=random.choice(l5)
                            #print(l5)


                    else:
                        next_position=random.choice(l4)
                        #print(l4)

                else:
                    next_position=random.choice(l3)
                    #print(l3)

            else:
                next_position=random.choice(l2)
                #print(l2)

        else:
            next_position=random.choice(l1)
            #print(l1)

        
        self.position=next_position