import numpy as np 
import pandas as pd
import math
import pickle
import networkx as nx
from collections import defaultdict
from BFS import *
import random 
class NeuralNetwork:

    def __init__(self,X,Y,layer_list=[2,3,2,1]):
        self.n_layers=4
        self.layer_list=layer_list
        self.X=X
        self.Y=Y
        self.train_size=0.8
        
    def split_dataset(self):
        train_limit=int(125000*self.train_size)
        self.X_train=self.X[:train_limit,:]
        self.X_test=self.X[train_limit:,:]
        self.Y_train=self.Y[:train_limit,:]
        self.Y_test=self.Y[train_limit:,:]

    def initialize_weights(self):
        np.random.seed(1) # Seed the random number generator
        self.W1=np.random.randn(self.layer_list[0],self.layer_list[1])
        self.B1=np.random.randn(self.layer_list[1],)
        
        self.W2=np.random.randn(self.layer_list[1],self.layer_list[2])
        self.B2=np.random.randn(self.layer_list[2],)

        self.W3=np.random.randn(self.layer_list[2],self.layer_list[3])
    #Activation Functions

    def sigmoid(self,z):
        return 1/(1+np.exp(-z))

    def sigmoid_prime(self,z):
        return (np.exp(-z)/(1+np.exp(-z))**2)

    def reLu(self,z):
        return np.maximum(0,z)
    def reLuPrime(self,z):
        y=(z>0)*1
        return y

    
    def leakyReLu(self,z):
        return np.maximum(0.1*z,z)
    def mean_squared_error(self,y,y_hat):
        loss_vector=np.subtract(y,y_hat)
        mse=0
        for value in loss_vector:
            mse+=value**2
        mse=mse/len(y)
        return mse
    def forward_propogation(self):

        self.Z1=np.dot(self.X_train,self.W1)+self.B1
        #self.print_state(self.Z1)
        self.A1=self.reLu(self.Z1)
        #self.print_state(self.A1)

        # print("\n2nd")
        self.Z2=np.dot(self.A1,self.W2)+self.B2
        #self.print_state(self.Z2)
        self.A2=self.reLu(self.Z2)
        #self.print_state(self.A2)

        # print("\n3rd")
        self.Z3=np.dot(self.A2,self.W3)
        #self.print_state(self.Z3)
        # self.Y_hat=self.reLu(self.Z3)
        self.Y_hat=self.Z3
        #self.print_state(self.Y_hat)

        self.loss=self.mean_squared_error(self.Y_train, self.Y_hat)
        print(np.sqrt(self.loss))
        return self.Y_hat

    def back_propogation(self):
        a=-2/len(self.Y_hat)
        self.delta_3=np.multiply(-(self.Y_train-self.Y_hat),self.reLuPrime(self.Z3))
        self.dJ_dW3=np.dot(self.A2.T,self.delta_3)

        self.delta_2=np.dot(self.delta_3,self.W3.T)
        self.delta_2=np.multiply(self.delta_2,self.reLuPrime(self.Z2))
        self.dJ_dW2=np.dot(self.A1.T,self.delta_2)
        

        self.delta_1=np.dot(self.delta_2,self.W2.T)
        self.delta_1=np.multiply(self.delta_1,self.reLuPrime(self.Z1))
        self.dJ_dW1=np.dot(self.X_train.T,self.delta_1)

        alpha=2
        # print(self.dJ_dW3.shape)
        # print(self.dJ_dW2.shape)
        # print(self.dJ_dW1.shape)
        print("\n ===========")
        print(self.W1)
        print(self.W2)
        print(self.W3)
        print()
        print(self.dJ_dW1)
        print(self.dJ_dW2)
        print(self.dJ_dW3)
        self.W3=self.W3+alpha*self.dJ_dW3
        self.W2=self.W2+alpha*self.dJ_dW2
        self.W1=self.W1+alpha*self.dJ_dW1
        

    def print_state(self,x):
        x_df=pd.DataFrame(x)
        print("\nDescription ->")
        print(x_df.describe())
        print(x_df.head(5))

if __name__=="__main__":

    #Preparing dataset
    n_nodes=50
    with open('/Users/abhishek.sawalkar/Library/Mobile Documents/com~apple~CloudDocs/AI Project/BetterSmarterFasterCircleOfLife/StoredUtilities/Graph1_Utility6.pkl', 'rb') as handle:
        data = handle.read()
    utility_dict = pickle.loads(data)
    
    with open('/Users/abhishek.sawalkar/Library/Mobile Documents/com~apple~CloudDocs/AI Project/BetterSmarterFasterCircleOfLife/StoredDistances/dist_dict1.pkl', 'rb') as handle:
        data = handle.read()
    dist_dict = pickle.loads(data)

    G = nx.read_gpickle("/Users/abhishek.sawalkar/Library/Mobile Documents/com~apple~CloudDocs/AI Project/BetterSmarterFasterCircleOfLife/StoredGraph/Graph1.gpickle")

    #Prepare dataset
    #X = vector of dim 125000x2. 2 features are distance to prey and distance to predator
    # dist_dict=defaultdict()
    # for start_node in range(1,n_nodes+1):
    #     for end_node in range(1,n_nodes+1):
    #         dist_dict[(start_node,end_node)]=len(get_bfs_path(G, start_node, end_node))-1
    
    X = np.zeros([125000,2])
    Y=np.zeros([125000,1])
    i=0
    for state in utility_dict:
        agent=state[0]
        prey=state[1]
        predator=state[2]
        utility=utility_dict[state]

        d_prey=dist_dict[(agent,prey)]
        d_pred=dist_dict[(agent,predator)]

        # print(d_prey,d_pred)
        X[i][0]=d_prey
        X[i][1]=d_pred
        # print(X[i])

        if math.isinf(utility):
            Y[i]=10000 #Some high value
        else:
            Y[i]=utility
        i+=1
        if i>10000:
            break
    # train=int(len(utility_dict)*0.8)

    NN=NeuralNetwork(X, Y)
    NN.split_dataset()
    NN.initialize_weights()
    NN.forward_propogation()
    n_iterations=10
    for i in range(n_iterations):

        NN.back_propogation()
        NN.forward_propogation()
    
    # print(NN.Y_hat)
    # Y_hat_df=pd.DataFrame(NN.Y_hat)
    # print(Y_hat_df.describe())



















    # X_train=X[:train,:]
    # X_test=X[train:,:]
    # Y_train=Y[:train,:]
    # Y_test=Y[train:,:]

    # print("X train= \n",X_train.shape)
    # print("X test = \n",X_test.shape)
    # print("Y train= \n",Y_train.shape)
    # print("Y test= \n",Y_test.shape)

    # df_x=pd.DataFrame(X)
    # df_y=pd.DataFrame(Y)
    # print(df_x.describe())
    # print(df_y.describe())



