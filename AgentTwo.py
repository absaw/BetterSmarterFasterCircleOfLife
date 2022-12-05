from Graph import *
from BFS import *
from Prey import *
from Predator import *

class AgentTwo:
    
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
        len_list=[]
        cost_matrix={}
        for neighbor in neighbor_list:
            c_prey=len(get_bfs_path(self.G, neighbor, prey.position)[1])
            c_predator=len(get_bfs_path(self.G, neighbor, predator.position)[1])
            cost_matrix[neighbor]=[c_prey,c_predator]
        
        run_from_pred_threshold=3

        # cycles=list(nx.cycle_basis(self.G.to_undirected()))
        # # print("Cycle list ->",*cycles)
        # small_cycles=[]
        # print("Cycles with length less than 5")
        # for i in cycles:
        #     if len(i)<5:
        #         small_cycles.append(i)
        #         print(*i)
        # nodes_to_avoid=[]
        # for node in range(1,51):
        #     if 2<=node<=49:
        #         if self.G.has_edge(node-1, node+1):
        #             nodes_to_avoid.append(node)
        #     elif node==1 or node == 50:
        #         if self.G.has_edge(u, v)

        if d_predator<run_from_pred_threshold:

            #default behaviour
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
                                    #select randomly from all neighbors or current position
                                    next_position=random.choice([self.position]+neighbor_list)

                                else:
                                    len_list.append(len(l6))
                                    # next_position=random.choice(l6)
                                    if len(l6)>1:
                                        if self.G.degree(l6[0])>self.G.degree(l6[1]):
                                            next_position=l6[0]
                                        else:
                                            next_position=l6[1]
                                    else:
                                        next_position=l6[0]

                            else:
                                len_list.append(len(l5))
                                # next_position=random.choice(l5)
                                if len(l5)>1:
                                    if self.G.degree(l5[0])>self.G.degree(l5[1]):
                                        next_position=l5[0]
                                    else:
                                        next_position=l5[1]
                                else:
                                    next_position=l5[0]

                        else:
                            len_list.append(len(l4))
                            # next_position=random.choice(l4)
                            if len(l4)>1:
                                if self.G.degree(l4[0])>self.G.degree(l4[1]):
                                    next_position=l4[0]
                                else:
                                    next_position=l4[1]
                            else:
                                next_position=l4[0]

                    else:
                        len_list.append(len(l3))
                        if len(l3)>1:
                            if self.G.degree(l3[0])>self.G.degree(l3[1]):
                                next_position=l3[0]
                            else:
                                next_position=l3[1]
                        else:
                            next_position=l3[0]
                        # next_position=random.choice(l3)

                else:
                    len_list.append(len(l2))
                    if len(l2)>1:
                        if self.G.degree(l2[0])>self.G.degree(l2[1]):
                            next_position=l2[0]
                        else:
                            next_position=l2[1]
                    else:
                        next_position=l2[0]
                    # next_position=random.choice(l2)


            else:
                len_list.append(len(l1))
                if len(l1)>1:
                    if self.G.degree(l1[0])>self.G.degree(l1[1]):
                        next_position=l1[0]
                    else:
                        next_position=l1[1]
                else:
                    next_position=l1[0]
        else:
            #run towards prey
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
                            #select randomly from all neighbors or current position
                            next_position=random.choice(neighbor_list)

                        else:
                            len_list.append(len(l6))
                            # next_position=random.choice(l6)
                            if len(l6)>1:
                                if self.G.degree(l6[0])>self.G.degree(l6[1]):
                                    next_position=l6[0]
                                else:
                                    next_position=l6[1]
                            else:
                                next_position=l6[0]

                    else:
                        len_list.append(len(l5))
                        # next_position=random.choice(l5)
                        if len(l5)>1:
                            if self.G.degree(l5[0])>self.G.degree(l5[1]):
                                next_position=l5[0]
                            else:
                                next_position=l5[1]
                        else:
                            next_position=l5[0]

                else:
                    len_list.append(len(l2))
                    if len(l2)>1:
                        if self.G.degree(l2[0])>self.G.degree(l2[1]):
                            next_position=l2[0]
                        else:
                            next_position=l2[1]
                    else:
                        next_position=l2[0]
                    # next_position=random.choice(l2)


            else:
                len_list.append(len(l1))
                if len(l1)>1:
                    if self.G.degree(l1[0])>self.G.degree(l1[1]):
                        next_position=l1[0]
                    else:
                        next_position=l1[1]
                else:
                    next_position=l1[0]
        # if len_list:
            # print(max(len_list))
        self.position=next_position