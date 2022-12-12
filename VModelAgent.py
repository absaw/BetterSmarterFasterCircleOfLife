from Graph import *
from BFS import *
from Prey import *
from Predator import *
import random
class VModelAgent:
    
    def __init__(self,n_nodes,G : nx.Graph,prey:Prey, predator:Predator,utility_dict,param_dict):
        self.n_nodes=n_nodes
        self.G=G
        self.utility_dict=utility_dict
        self.param_dict=param_dict

        ag_not_decided=True
        while ag_not_decided:
            self.position=random.randint(1, n_nodes)
            d_predator=len(get_bfs_path(self.G, self.position, predator.position))-1
            # if self.position!=prey.position and self.position != predator.position:
            if self.position!=prey.position and d_predator>1:
                ag_not_decided=False
    
    def compute_equation(self):

    def simulate_step(self,prey : Prey,predator:Predator):
        agent=self.position
        prey=prey.position
        predator=predator.position
        
        agent_neighbors=list(self.G.neighbors(agent))
        # prey_neighbors=list(self.G.neighbors(prey))+[prey] #Prey itself is also added since it can stay in same place
        # predator_neighbors=list(self.G.neighbors(predator))
        # agent_action_space=defaultdict()
        
        agent_action_utility=defaultdict()

        for ag_neighbor in agent_neighbors:
            # for prey_neighbor in prey_neighbors:
            #     for predator_neighbor in predator_neighbors:
            state=(ag_neighbor,prey,predator)
            agent_action_utility[state]=self.utility_dict[state] #we will store the utility in here

        min_utility=min(agent_action_utility.values())
        min_state=[key for key in agent_action_utility if agent_action_utility[key]==min_utility]
        min_state=random.choice(min_state)
        next_position=min_state[0]

        self.position=next_position
                   