from collections import defaultdict
from Graph import *
from BFS import *
def print_dict(d):
    for key,value in d.items():
        print(key," : ",value)

if __name__=="__main__":
    # state_list=[]
    n_nodes=10
    # for agent in range(1,n_nodes):
    #     for prey in range(1,n_nodes):
    #         for predator in range(1,n_nodes):
    #             state_list.append([agent,prey,predator])
    
    # print(len(state_list))

    # #setting rewards

    # reward_list=[0]*len(state_list)

    # for i in range(len(state_list)):
    #     state=state_list[i]
    #     if state[0]==state[1]: #agent and prey has same position
    #         reward_list[i]=0 #minimum possible expected number of steps to prey is 0
    #     if state[0]==state[2]:
    #         reward_list[i]=10000 #reaching prey is impossible so a high value
    
    # utility_list=[0]*len(state_list)
    # n_iterations=10000
    # for k in range(1,n_iterations):

    state_dict=defaultdict()
    for agent in range(1,n_nodes):
        for prey in range(1,n_nodes):
            for predator in range(1,n_nodes):
                state_dict[(agent,prey,predator)]=[0,0] #reward, utility
    
    #Setting rewards

    for state in state_dict:
        # if state[0]==state[1]: #agent and prey has same position
        #     state_dict[state][0]=0 #minimum possible expected number of steps to prey is 0
        #     state_dict[state]
        if state[0]==state[2]:
            state_dict[state]=[10000,10000] #reaching prey is impossible so a high value
        else:
            state_dict[state]=[1,1]

    # print_dict(state_dict)

    GraphClass=Graph(10)
    G=GraphClass.G
    # GraphClass.visualize_graph()
    beta=0.9
    n_iterations=1
    for k in range(n_iterations):
        #Running for all states
        for state in state_dict:
            #Generate action space by getting the neighbors of the agent,prey,predator
            action_space=defaultdict()
            agent=state[0]
            prey=state[1]
            predator=state[2]

            agent_neighbors=list(G.neighbors(agent))
            prey_neighbors=list(G.neighbors(prey))+[prey]
            predator_neighbors=list(G.neighbors(predator))

            for ag_neighbor in agent_neighbors:
                for prey_neighbor in prey_neighbors:
                    for predator_neighbor in predator_neighbors:
                        action_space[(ag_neighbor,prey_neighbor,predator_neighbor)]=[0] #we will store the probability in here
            
            print_dict(action_space)
            #Prob of agent must be decided by the policy which is to take the next neighbor with 
            # the least utility value 
            p_agent=1/(G.degree(agent))
            # p_agent=1
            p_prey=1/(G.degree(prey)+1)

            p_pred_1 = 0.4/G.degree(predator)
            # pred_prime_neighbors=list(G.neighbors(predator))
            dist_list=[]
            for predator_neighbor in predator_neighbors:
                dist=len(get_bfs_path(G, predator_neighbor, agent))
                dist_list.append(dist)
            min_dist=min(dist_list)
            min_dist_neighbor_count=dist_list.count(min_dist)
            prob_sum=0
            
            for action in action_space:
                predator_prime=action[2]
                dist_pred_prime=len(get_bfs_path(G, predator_prime, agent))
                if dist_pred_prime==min_dist:
                    p_pred_2=0.6/min_dist_neighbor_count
                else:
                    p_pred_2=0
            
                p_pred = p_pred_1+p_pred_2

                prob_action=p_agent*p_prey*p_pred

                action_space[action][0] = prob_action
            
                prob_sum+=prob_action
            #Now we have the transition probability of all the possible action states from the current state s

            print(len(action_space))
            print_dict(action_space)
            print(prob_sum)

            #Calculating iterative U*
            reward=state_dict[state][0]
            prev_utility=state_dict[state][1]
            #We will calculate V for all possible actions. Then take the min of these values to be the final V for this iteration
            
            utility_space=defaultdict()
            # min_utility=-1
            for action in action_space:
                utility = reward + beta * action_space[action][0] * prev_utility
                utility_space[action]=utility
                # action_space[action].append(utility)
                # if utility>min_utility:
                    # min_utility=utility
            min_utility=min(utility_space.values())
            min_utility_list=[key for key in utility_space if utility_space[key]==min_utility]
            print_dict(utility_space)
            print(min_utility_list)


        break






















