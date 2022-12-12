import numpy as np 
import pandas as pd
import math
import pickle
import networkx as nx
from collections import defaultdict
from BFS import *
import random
import matplotlib.pyplot as plt
from datetime import datetime 
class NeuralNetwork:

    def __init__(self,X,Y,alpha,seed,layer_list=[2,2,3,1]):
        self.layer_list=layer_list
        self.X=X
        self.Y=Y
        self.train_size=0.8
        self.parameters={}
        self.alpha=alpha
        self.seed=seed
        
        
    def split_dataset(self):
        train_limit=int(125000*self.train_size)
        self.X_train=self.X[:train_limit,:]
        self.X_test=self.X[train_limit:,:]
        self.Y_train=self.Y[:train_limit,:]
        self.Y_test=self.Y[train_limit:,:]
    def initialize__custom_weights(self,param_dict):
        self.W1=self.parameters["W1"]
        self.W2=self.parameters["W2"]
        self.W3=self.parameters["W3"]
        self.BW1=self.parameters["BW1"]
        self.BW2=self.parameters["BW2"]
        self.bias1=self.parameters["bias1"]
        self.bias2=self.parameters["bias2"]
        
    def initialize_weights(self):
        np.random.seed(self.seed) # Seed the random number generator
        self.W1=np.random.randn(self.layer_list[0],self.layer_list[1])
        self.BW1=np.random.randn(self.layer_list[1],)
        
        self.W2=np.random.randn(self.layer_list[1],self.layer_list[2])
        self.BW2=np.random.randn(self.layer_list[2],)

        self.W3=np.random.randn(self.layer_list[2],self.layer_list[3])

        self.parameters["W1"]=self.W1
        self.parameters["W2"]=self.W2
        self.parameters["W3"]=self.W3
        self.parameters["BW1"]=self.BW1
        self.parameters["BW2"]=self.BW2

        self.bias1=1
        self.bias2=1

    #Activation Functions

    def sigmoid(self,z):
        return 1/(1+np.exp(-z))

    def sigmoid_prime(self,z):
        return (np.exp(-z)/(1+np.exp(-z))**2)

    def reLu(self,z):
        return np.maximum(0,z)
        # return (np.exp(z)-np.exp(-z))/(np.exp(z)+np.exp(-z))

        # return 1/(1+np.exp(-z))

        # return np.maximum(0.1*z,z)

    def reLuPrime(self,z):
        z[z<=0] = 0
        z[z>0] = 1
        return z
        # return (1-z*z)

        # return (np.exp(-z)/(1+np.exp(-z))**2)

        # y=(z>0)*1
        # return y

    
    def leakyReLu(self,z):
        return np.maximum(0.1*z,z)
    def tanh(self,z):
        return (np.exp(z)-exp(-z))/(np.exp(z)+exp(-z))
    def tanh_prime(self,z):
        return (1-z*z)

    def mean_squared_error(self,y,y_hat):
        loss_vector=np.subtract(y,y_hat)
        mse=0
        for value in loss_vector:
            mse+=value**2
        mse=mse/len(y)
        return mse

    def forward_propogation(self):
        
        self.Z1=np.dot(self.X_train,self.W1)+self.bias1*self.BW1
        # self.print_state(self.Z1)
        self.A1=self.reLu(self.Z1)
        # self.print_state(self.A1)

        # print("\n2nd")
        self.Z2=np.dot(self.A1,self.W2)+self.bias2*self.BW2
        # self.print_state(self.Z2)
        self.A2=self.reLu(self.Z2)
        # self.print_state(self.A2)

        # print("\n3rd")
        self.Z3=np.dot(self.A2,self.W3)
        # self.print_state(self.Z3)
        # self.Y_hat=self.reLu(self.Z3)
        self.Y_hat=self.Z3
        # self.print_state(self.Y_hat)

        # self.loss=self.mean_squared_error(self.Y_train, self.Y_hat)
        # print(np.sqrt(self.loss))
        self.parameters["X_train"]=self.X_train
        self.parameters["Z1"]=self.Z1
        self.parameters["A1"]=self.A1
        self.parameters["Z2"]=self.Z2
        self.parameters["A2"]=self.A2
        self.parameters["Z3"]=self.Z3
        self.parameters["bias1"]=self.bias1
        self.parameters["bias2"]=self.bias2
        self.parameters["Y_hat"]=self.Y_hat

    def back_propogation(self):
        # a=2/len(self.Y_train)
        y_diff=np.subtract(self.Y_train,self.Y_hat)
        # self.delta_3=np.multiply(y_diff,self.reLuPrime(self.Z3))
        self.delta_3=2*y_diff/len(self.Y_train)
        self.dJ_dW3=np.dot(self.A2.T,self.delta_3)
        # self.dB3=np.sum(self.delta_3,axis=1,keepdims=True)

        self.delta_2=np.dot(self.delta_3,self.W3.T)
        self.delta_2=np.multiply(self.delta_2,self.reLuPrime(self.Z2))
        self.dJ_dW2=np.dot(self.A1.T,self.delta_2)
        self.dBW2=np.sum(self.delta_2,axis=1,keepdims=True)
        # print(self.dBW2.shape)
        # print(self.dBW2)

        self.delta_1=np.dot(self.delta_2,self.W2.T)
        self.delta_1=np.multiply(self.delta_1,self.reLuPrime(self.Z1))
        self.dJ_dW1=np.dot(self.X_train.T,self.delta_1)
        self.dBW1=np.sum(self.delta_1,keepdims=True)

        alpha=self.alpha
        # print(self.dJ_dW3.shape)
        # print(self.dJ_dW2.shape)
        # print(self.dJ_dW1.shape)
        # print("\n ===========")
        # print(self.W1)
        # print(self.W2)
        # print(self.W3)
        # print("DJs")
        # print(self.dJ_dW1)
        # print(self.dJ_dW2)
        # print(self.dJ_dW3)
        self.W1=self.W1+alpha*self.dJ_dW1
        self.W2=self.W2+alpha*self.dJ_dW2 
        self.W3=self.W3+alpha*self.dJ_dW3 

        self.BW1=self.BW1+alpha*self.dBW1
        self.BW2=self.BW2+alpha*self.dBW2
        
        self.parameters["W1"]=self.W1
        self.parameters["W2"]=self.W2
        self.parameters["W3"]=self.W3
        self.parameters["BW1"]=self.BW1
        self.parameters["BW2"]=self.BW2
        # self.B3+=alpha*self.dB3
        # print(self.BW2.shape)
        # print(self.dBW2.shape)
        

        # print("Weights After updates")
        # print(self.W1)
        # print(self.W2)
        # print(self.W3)
        

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
    
    # train=int(len(utility_dict)*0.8)
    layer_list=[2,2,3,1]
    alpha=0.001
    seed=1
    NN=NeuralNetwork(X, Y,alpha,seed,layer_list)
    # NN.print_state(X)
    # NN.print_state(Y)
    # a=np.zeros([2,3])
    # a[0][1]=-1
    # a[0][2]=3
    # print(NN.reLuPrime(a))
    NN.split_dataset()

    NN.initialize_weights()
    # NN.print_state(NN.W1)
    # NN.print_state(NN.BW1)
    # NN.print_state(NN.W2)
    # NN.print_state(NN.W3)

    NN.forward_propogation()
    # NN.back_propogation()
    # print(NN.dJ_dW1)
    # print(NN.dJ_dW2)
    # print(NN.dJ_dW3)
    # NN.forward_propogation()
    # NN.print_state(NN.W1)
    # NN.print_state(NN.BW1)
    # NN.print_state(NN.W2)
    # NN.print_state(NN.W3)

    loss_list=[]
    n_iterations=3000
    for i in range(n_iterations):

        NN.back_propogation()
        # print("\n====")
        # print(NN.dJ_dW1)
        # print(NN.dJ_dW2)
        # print(NN.dJ_dW3)
        NN.forward_propogation()
        loss=NN.mean_squared_error(NN.Y_train, NN.Y_hat)
        print(i,") RMSE == ",np.sqrt(loss))
        # print(i)
        loss_list.append(np.sqrt(loss))

    print("loss list = ",loss_list[-1])

    loss_list_x=range(1,len(loss_list)+1)
    NN.parameters["Loss_list"]=loss_list
    file = open("StoredWeights/weight_dict1.pkl", "wb")
    pickle.dump(NN.parameters, file)

    file.close()
    plt.plot(loss_list_x,loss_list)
    
    plt.show()
    timenow=datetime.now().strftime("%H-%M-%S")
    plt.savefig("StoredCharts/"+timenow+".png")
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




