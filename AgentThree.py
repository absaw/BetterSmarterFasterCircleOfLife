from Graph import *
from BFS import *
from Prey import *
from Predator import *
from AgentOne import *
import copy

class AgentThree:
    
    def __init__(self,n_nodes,G : nx.Graph,prey:Prey, predator:Predator):
        self.n_nodes=n_nodes
        self.G=G
        self.prey=prey
        self.predator=predator
        ag_not_decided=True
        while ag_not_decided:
            self.position=random.randint(1, n_nodes)
            if self.position!=prey.position and self.position != predator.position:
                ag_not_decided=False
        self.p_now=[0]*n_nodes
        self.p_next=[0]*n_nodes
        # Initialize the probablities of all the nodes in the graph
        self.initialize_probabilities()
        self.p_now[self.position-1]=0
        self.sure_of_prey=0

    def simulate_step(self,survey_node,prey : Prey,predator:Predator):
        # Simulate step will perform following actions:-
        # 1. Update belief system for finding/not finding prey at current survey node
        # 2. Move agent to next highest prob value neighbor by rules of Agent 1
        # 3. Update belief system for finding/not finding prey at new position

        #Prey's position here is only used to check if the surveyed node is the prey's node or not
       
        # 1. Belief update based on surveyed node
        self.update_belief(survey_node, prey.position)
        G_copy=copy.deepcopy(self.G)
        
        m=max(self.p_now)
        max_prob_list=[node+1 for node in range(len(self.p_now)) if self.p_now[node]==m]
        prey_virtual_location=random.choice(max_prob_list)
        
        virtual_prey=Prey(self.n_nodes,self.G)
        virtual_prey.position=prey_virtual_location
        
        #2. Agent moves towards the highest prob_now node of prey with rules of agent One
        ag_one=AgentOne(self.n_nodes, self.G, virtual_prey, self.predator)
        ag_one.position=self.position
        ag_one.simulate_step(virtual_prey, self.predator)
        self.position=ag_one.position
        
        #Agent has now moved to the new position, according to agent 1's behaviour
        # 3. Update belief system again
        self.update_belief(self.position, prey.position)
    

    def update_belief(self,survey_node,prey_positon):
        # Update belief changes the probability of the nodes based on the belief system 
        # 1. If prey was found at survey node--set P_now(survey_node)=1
        # 2. If prey was not found at survey node--set P_now(survey_node)=0, for each X out of nodes, P(X)=P(prey in the node X)*P(prey not in survey node|prey in the node X)/P(prey not in survey node)
        
        if survey_node==prey_positon:
            #1. Prey found scenario
            self.p_now[survey_node-1]=1
            #set prob of all other nodes to 0
            for node in range(1,51):
                if node!=survey_node:
                    self.p_now[node-1]=0
            self.sure_of_prey+=1
        else:
            #2. Prey not found scenario
            p_new=[0]*50
            p_prey_not_in_survey_node=1-self.p_now[survey_node-1]
            for node in range(1,51):
                if node!=survey_node:
                    p_prey_in_current_node=self.p_now[node-1]
                    p_new[node-1]=p_prey_in_current_node/p_prey_not_in_survey_node
            
            self.p_now=p_new.copy()
    #Used- Simplified version
    def transition_update(self):
        # This updates the prob of all nodes, for when the prey moves in the graph
        for update_node in range(1,self.n_nodes+1): # C
            neighbors_of_update_node=list(self.G.neighbors(update_node))+[update_node] # [A,B,D,E]

            p_update_node=0

            for neighbor_of_update_node in neighbors_of_update_node:# node=A,B,D,E
                degree_of_neighbor_of_update_node=self.G.degree(neighbor_of_update_node)
                p_update_node+=self.p_now[neighbor_of_update_node-1]/(degree_of_neighbor_of_update_node+1)
        
            self.p_next[update_node-1]=p_update_node

    def initialize_probabilities(self):
        #Initialize all prob to 1/49
        for node in range(self.n_nodes):
            self.p_now[node]=1/49

    def print_state(self):
        #Print current values
        print("\nCurrent State ->")
        print("Agent Position : ",self.position)
        print("Neighbors : ",*list(self.G.neighbors(self.position)))
        print("Prey Position : ",self.prey.position)
        print("Neighbors : ",*list(self.G.neighbors(self.prey.position)))
        print("Predator Position : ",self.predator.position)
        print("Neighbors : ",*list(self.G.neighbors(self.predator.position)))
        d_prey=len(get_bfs_path(self.G, self.position, self.prey.position)[1])  #Distance from prey
        d_predator=len(get_bfs_path(self.G, self.position, self.predator.position)[1])  #Distance from predator
        print("Distance to Prey : ",d_prey)
        print("Distance to Predator : ",d_predator)
        print("Sum of P_now : ",sum(self.p_now))
        # print()
        # print("P_now -> ",*self.p_now)
        # print()
        print("Sum of P_next : ",sum(self.p_next))
        # print()
        # print("P_next -> ",self.p_next)
        # print("\n")

    def print_sum(self):
        print("Sum of P_now : ",sum(self.p_now))
        print("Sum of P_next : ",sum(self.p_next))


#Used for testing. Not part of the main flow. AgentThree simulator will call AgentThree
if __name__=="__main__":

    n_nodes=50
    G=Graph(n_nodes).G
    prey=Prey(n_nodes,G)
    # prey.position=6
    predator=Predator(n_nodes, G)
    agent_three=AgentThree(n_nodes, G, prey, predator)
    survey_list=list(range(1,51))
    survey_list.remove(agent_three.position)
    survey_node=random.choice(survey_list)
    # print("Initial Condtion -> ")
    # agent_three.print_state()
    # agent_three.simulate_step(prey, predator)
    # for i in range(1,101):
    # # while(True):
    #     print("i = ",i)
    #     if agent_three.position==prey.position:
    #         print("Prey found main")
    #         break
        
    #     agent_three.simulate_step(survey_node,prey, predator)
    #     agent_three.print_state()
    #     m=max(agent_three.p_now)
    #     survey_list=[node+1 for node in range(len(agent_three.p_now)) if agent_three.p_now[node]==m]
    #     survey_node=random.choice(survey_list)


    # agent_three.print_state()
    for i in range(0,10):
        agent_three.transition_update()
        agent_three.print_state()


# def transition_update(self,survey_node):
#         set_next_prob_list=list(self.G.neighbors(survey_node))+[survey_node]

#         for node in set_next_prob_list:
#             # if self.G.degree(node)==3:
#             set_next_prob_list_neighbor=list(self.G.neighbors(node))+[node]
#             p_node_2=0
#             for node_2 in set_next_prob_list_neighbor:
#                 if self.G.degree(node_2)==3:
#                     multiplier=1/4
#                 else:
#                     multiplier=1/3
#                 # P_next_calc+=self.G.nodes[node_2]["P_now"]*multiplier
#                 p_node_2+=self.p_now[node_2-1]*multiplier
            
#             # self.G.nodes[node]["P_next"]=P_next
#             # self.p_next[node-1]=p_node_2
#             self.p_now[node-1]=p_node_2