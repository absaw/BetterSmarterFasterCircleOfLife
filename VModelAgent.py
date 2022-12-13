from Graph import *
from BFS import *
from Prey import *
from Predator import *
import random
from NeuralNetwork import *
class VModelAgent:
    
    def __init__(self,n_nodes,G : nx.Graph,prey:Prey, predator:Predator,utility_dict,param_dict,dist_dict):
        self.n_nodes=n_nodes
        self.G=G
        self.utility_dict=utility_dict
        self.param_dict=param_dict
        self.dist_dict=dist_dict

        ag_not_decided=True
        while ag_not_decided:
            self.position=random.randint(1, n_nodes)
            d_predator=len(get_bfs_path(self.G, self.position, predator.position))-1
            # if self.position!=prey.position and self.position != predator.position:
            if self.position!=prey.position and d_predator>1:
                ag_not_decided=False
        self.initialize_custom_weights()
        
    

    def simulate_step(self,prey : Prey,predator:Predator):
        agent=self.position
        # prey=prey.position
        # predator=predator.position
        
        agent_neighbors=list(self.G.neighbors(agent))
        # prey_neighbors=list(self.G.neighbors(prey))+[prey] #Prey itself is also added since it can stay in same place
        # predator_neighbors=list(self.G.neighbors(predator))
        # agent_action_space=defaultdict()
        
        agent_action_utility=defaultdict()

        for ag_neighbor in agent_neighbors:
            # for prey_neighbor in prey_neighbors:
            #     for predator_neighbor in predator_neighbors:
            state=(ag_neighbor,prey,predator)
            d_prey=self.dist_dict[(ag_neighbor,prey.position)]
            d_pred=self.dist_dict[(ag_neighbor,predator.position)]
            # NN.X_train=
            input=np.reshape([d_prey,d_pred],(1,2))
            utility=self.get_utility(input)[0][0]
            agent_action_utility[state]= utility#we will store the utility in here
            # print(utility)

        min_utility=min(agent_action_utility.values())
        min_state=[key for key in agent_action_utility if agent_action_utility[key]==min_utility]
        min_state=random.choice(min_state)
        next_position=min_state[0]

        self.position=next_position
    
    def reLu(self,z):
        # return np.maximum(0,z)
        # return (np.exp(z)-np.exp(-z))/(np.exp(z)+np.exp(-z))

        # return 1/(1+np.exp(-z))
        return(np.tanh(z))

        # return np.maximum(0.05*z,z)

    def reLuPrime(self,z):
        # z[z<=0] = 0
        # z[z>0] = 1
        # return z
        return (1-np.tanh(z)**2)
    # def reLu(self,z):
        # return np.maximum(0,z)
        # return (np.exp(z)-np.exp(-z))/(np.exp(z)+np.exp(-z))

        # return 1/(1+np.exp(-z))

        # return np.maximum(0.05*z,z)

    # def reLuPrime(self,z):
        # z[z<=0] = 0
        # z[z>0] = 1
        # return z
        # z[z<=0] = 0.05
        # z[z>0] = 1
        # return z

    def initialize_custom_weights(self):
        self.W1=self.param_dict["W1"]
        self.W2=self.param_dict["W2"]
        self.W3=self.param_dict["W3"]
        self.BW1=self.param_dict["BW1"]
        self.BW2=self.param_dict["BW2"]
        # self.BW3=self.param_dict["BW3"]
        self.bias1=self.param_dict["bias1"]
        self.bias2=self.param_dict["bias2"]

    def forward_propogation_pred(self,input):
        
        self.Z1=np.dot(input,self.W1)+self.BW1
        # self.print_state(self.Z1)
        self.A1=self.reLu(self.Z1)
        # self.print_state(self.A1)

        # print("\n2nd")
        self.Z2=np.dot(self.A1,self.W2)+self.BW2
        # self.print_state(self.Z2)
        self.A2=self.reLu(self.Z2)
        # self.print_state(self.A2)

        # print("\n3rd")
        self.Z3=np.dot(self.A2,self.W3)#+self.BW3
        # self.print_state(self.Z3)
        # self.Y_hat=self.reLu(self.Z3)
        self.Y_hat=self.Z3
        # self.print_state(self.Y_hat)
        return self.Y_hat
        # self.loss=self.mean_squared_error(self.Y_train, self.Y_hat)
        # print(np.sqrt(self.loss))
        # self.parameters["X_train"]=self.X_train
        # self.parameters["Z1"]=self.Z1
        # self.parameters["A1"]=self.A1
        # self.parameters["Z2"]=self.Z2
        # self.parameters["A2"]=self.A2
        # self.parameters["Z3"]=self.Z3
        # self.parameters["bias1"]=self.bias1
        # self.parameters["bias2"]=self.bias2
        # self.parameters["Y_hat"]=self.Y_hat
    
    def get_utility(self,input):
        utility=self.forward_propogation_pred(input)
        return utility