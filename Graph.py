from math import degrees
from turtle import pos
import networkx as nx
import matplotlib.pyplot as plt
import random
from collections import deque


#Generate a graph with self.n_nodes. Max degree = 3. Nodes are numbered from 1 to self.n_nodes(i.e. 50)
class Graph:

    def __init__(self,n_nodes):
        self.n_nodes=n_nodes
        self.G=None
        self.generate_graph()
        
    def generate_graph(self):
        # self.n_nodes=50
        
        G=nx.Graph()
        
        #add nodes to the graph

        for node in range(1,self.n_nodes+1):
            G.add_node(node,P_now=0,P_next=0)
        
        node_list=list(G.nodes())
        # print("Node list : ",node_list)
        #adding initial edges

        for node in range(1,self.n_nodes+1):
            if node==self.n_nodes:
                G.add_edge(self.n_nodes,1)
            else:
                G.add_edge(node,node+1)
        # print("Initial No. of edges = ",G.number_of_edges())
        # visualize_graph(G)
        #adding edges randomly till degree is less than 3
        addEdge=True
        k=0
        while len(node_list)>0:
            # print(len(node_list))
            # if len(node_list)<=5:
                # print("here")
                # visualize_graph(G)
            # k+=1
        # for node_beg in range(0,self.n_nodes):
            # node_beg=random.randint(0,self.n_nodes)
            node_beg=random.choice(node_list)
            
            possible_node_list=list(range(node_beg-5,node_beg-1))+list(range(node_beg+2,node_beg+6))
            for i in range(len(possible_node_list)):
                if possible_node_list[i]==0:
                    possible_node_list[i]=self.n_nodes  #when node =0, then since the nodes are connected cirularly, the 0th node becomes 
                                                #last node. This separate 0 condition is used since mod function doesn't work with 0
                elif possible_node_list[i]<0 or possible_node_list[i]>self.n_nodes:
                    possible_node_list[i]=possible_node_list[i]%self.n_nodes

            # print(" Node  ",node_beg)
            # print("Possible Node List ",possible_node_list)
            
            if G.degree(node_beg)<3:
                possible_node_list_copy=possible_node_list.copy()
                for node in possible_node_list:
                    if G.degree(node)>=3:
                        possible_node_list_copy.remove(node)
                if not possible_node_list_copy:
                    node_list.remove(node_beg)
                    continue
                possible_node_list=possible_node_list_copy

                #if list is empty
                
                # if 5<node_beg<self.n_nodes-5:
                # endNodeNotFound=True
                # max_tries=10
                # while endNodeNotFound:
                    # max_tries-=1
                node_end=random.choice(possible_node_list)
                # node_end=abs(random.randint(node_beg-5,node_beg+5))%50
                if G.degree(node_end)<3 and node_end!=node_beg:
                    # endNodeNotFound=False
                    G.add_edge(node_beg,node_end)
                    node_list.remove(node_beg)
                    node_list.remove(node_end)
                # elif G.degree(node_end)>=3:
                #     node_list.remove(node_end)
                # if max_tries==0:
                #     break
                
                # else:
            # if k==20:
                # break
            else:
                node_list.remove(node_beg)
            

        # print("No. of edges = ",G.number_of_edges())
        # for node in range(1,self.n_nodes+1):
        #     nlist=list(G.neighbors(node))
        #     nlist.sort()
            # print("Node - ",node," Degree - ",G.degree(node),"- Neighbors - ",nlist)
            
        # visualize_graph(G)
        self.G=G
        # return G

    def visualize_graph(self):
        # plt.figure(figsize=(2,2))
        pos=nx.circular_layout(self.G)
        # nx.draw_networkx_nodes(self.G,pos=pos)
        # nx.draw_networkx_edges(self.G, pos,connectionstyle="arc2,rad=0.5")
        nx.draw_networkx(self.G,pos=pos,with_labels=True,edge_color="Green")
        # nx.draw_circular(G,with_labels=True)
        plt.show()
        # nx.draw(self.G,with_labels=True)
        # plt.show()

    # def get_shortest_path():
    # for i in range(0,100):
    #     generate_graph(50)
    # generate_graph(50)

if __name__=="__main__":
    
    # GraphClass=Graph(50)
    # G=GraphClass.G
    # cycles=list(nx.cycle_basis(G.to_undirected()))
    # # print("Cycle list ->",*cycles)
    # print("Cycles with length less than 5")
    # for i in cycles:
    #     if len(i)<5:
    #         print(*i)
            
    # print("Cycle list ->",list(nx.simple_cycles(G)))
    # GraphClass.visualize_graph()
    
    n_edges=[]
    #Finding the smallest no. of edges we are always able to add.
    for i in range(1000000):
        GraphClass=Graph(50)
        G=GraphClass.G
        edge_list=list(G.edges)
        # print(len(edge_list))
        n_edges.append(len(edge_list)-50)
    
    # print(*n_edges)
    print("Max =",max(n_edges))
    print("Min =",min(n_edges))