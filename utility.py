from collections import defaultdict
from Graph import *
from BFS import *
import math
from datetime import datetime
from time import time
import pickle
def print_dict(d):
    for key,value in d.items():
        print(key," : ",value)

if __name__=="__main__":
    start = time()

    #=========== Log file =======================
    # filename_txt="Results/Utility4.txt"
    filename_txt="/Users/abhishek.sawalkar/Library/Mobile Documents/com~apple~CloudDocs/AI Project/BetterSmarterFasterCircleOfLife/Results/Utility17.txt"
    # filename_csv="Results/AgentOne.csv"
    file=open(filename_txt,"w")
    # csvfile = open(filename_csv, "a")
    # csv_writer=csv.writer(csvfile)
    # fields=['Date Time','Simulation Number','Number of Graphs','Won','Died','Hanged','Comments']
    # csv_writer.writerow(fields)
    text = "\n\n\n======  Start Time  =========->  " + \
        datetime.now().strftime("%m/%d/%y %H:%M:%S")
    file.write(text)
    # file.write("\nNo. of Simulations = 30")
    # file.write("\nNo. of trials for each simulation = 100")
    # csv_writer.writerow(["Execution Started"])
    #============================================
    n_nodes=50

    state_dict=defaultdict()
    final_utility=defaultdict()

    for agent in range(1,n_nodes+1):
        for prey in range(1,n_nodes+1):
            for predator in range(1,n_nodes+1):
                state_dict[(agent,prey,predator)]=[0,0] #reward, utility
                final_utility[(agent,prey,predator)]=0

    #Reading the stored graph
    # G = nx.read_gpickle("StoredGraph/Graph1.gpickle")
    G = nx.read_gpickle("/Users/abhishek.sawalkar/Library/Mobile Documents/com~apple~CloudDocs/AI Project/BetterSmarterFasterCircleOfLife/StoredGraph/Graph1.gpickle")
    
    dist_dict=defaultdict()
    for start_node in range(1,n_nodes+1):
        for end_node in range(1,n_nodes+1):
            dist_dict[(start_node,end_node)]=len(get_bfs_path(G, start_node, end_node))-1

    #Setting initial rewards and utility
    for state in state_dict:
        if state[0]==state[1]: #agent and prey has same position
            state_dict[state]=[0,0] #minimum possible expected number of steps to prey is 0
        elif state[0]==state[2]:
            state_dict[state]=[math.inf,0] #reaching prey is impossible so a high value
        else:
            # distance_to_prey=len(get_bfs_path(G,state[0],state[1]))
            distance_to_prey=dist_dict[(state[0],state[1])]
            state_dict[state]=[1]+[distance_to_prey]
    
    #=============================================================
    #=========== Value Iteration Algorithm =======================
    #=============================================================
    beta=1
    n_iterations=50
    # error_list=[0]*len(state_dict)
    error_list=[]
    for k in range(n_iterations):
        #Running for all states
        error=0
        #For each particular state-We will calculate U* for all possible actions. Then take the min of these values to be the final U for this iteration
        for state in state_dict:
            #Generate action space by getting the neighbors of the agent,prey,predator
            # action_space=defaultdict()
            agent=state[0]
            prey=state[1]
            predator=state[2]

            if agent==prey:
                min_utility=0
                state_dict[state].append(min_utility)
                continue

            elif agent==predator:
                min_utility=math.inf
                state_dict[state].append(min_utility)
                continue
            
            
            agent_neighbors=list(G.neighbors(agent))
            prey_neighbors=list(G.neighbors(prey))+[prey] #Prey itself is also added since it can stay in same place
            predator_neighbors=list(G.neighbors(predator))
            agent_action_space=defaultdict()
            if prey in agent_neighbors:
                min_utility=1
                state_dict[state].append(min_utility)
                continue
            if agent in predator_neighbors:
                min_utility=math.inf
                state_dict[state].append(min_utility)
                continue

            for ag_neighbor in agent_neighbors:
                agent_action_space[ag_neighbor]=[]
                for prey_neighbor in prey_neighbors:
                    for predator_neighbor in predator_neighbors:
                        # action_space[(ag_neighbor,prey_neighbor,predator_neighbor)]=[0] #we will store the transition probability in here
                        #An agent can have 2 or 3 moves to make. We store all possible prey and predator states after the agent's move
                        #So there are 12 possible states for each agent's move. 4x3 i.e. 4 for prey, 3 for predator
                        agent_action_space[ag_neighbor].append((ag_neighbor,prey_neighbor,predator_neighbor))
            # Now we have all the actions possible for this particular state
            
            # p_agent=1/(G.degree(agent))
            p_agent=1 # Since agent's move is deterministic
            p_prey=1/(G.degree(prey)+1) #Prey can move to any of its neighbor or stay 
            p_pred_1 = 0.4/G.degree(predator) #Pred 1 is for distracted part of predator
            
            dist_list=[]
            for predator_neighbor in predator_neighbors:
                # dist=len(get_bfs_path(G, predator_neighbor, agent))
                dist=dist_dict[(predator_neighbor,agent)]
                dist_list.append(dist)
            min_dist=min(dist_list)
            min_dist_neighbor_count=dist_list.count(min_dist)
            prob_sum=0
            
            reward=state_dict[state][0]
            
            # We want the utility calculation done for the actions of the agent
            agent_utility_dict=defaultdict()
            
            for agent_action in agent_action_space: #2 or 3 agent actions possible
                #expected_utility=summation of product of individual probabilities and utilities of transition states
                action_possibilities=agent_action_space[agent_action]
                expected_utility=0
                
                prob_sum=0
                for possible_action in action_possibilities:
                    # isTerminated=False
                    agent_prime=possible_action[0] #Agent position after action
                    prey_prime=possible_action[1] #Prey position after action
                    predator_prime=possible_action[2] #Predator position after action
                    
                    if agent_prime==prey_prime:
                        expected_utility+=0
                        #This won't affect the expected utility
                        # isTerminated=True

                    elif agent_prime==predator_prime:
                        expected_utility+=math.inf
                        # isTerminated=True
                    else:
                        dist_pred_prime=dist_dict[(predator_prime,agent)]
                        if dist_pred_prime==min_dist:
                            p_pred_2=0.6/min_dist_neighbor_count #Pred 2 is for pred which moves directly towards agent
                        else:
                            p_pred_2=0
                        p_pred = p_pred_1+p_pred_2
                        prob_action=p_agent*p_prey*p_pred
                        # action_space[action][0] = prob_action
                        prob_sum+=prob_action
                        prev_utility=state_dict[possible_action][-1]
                        expected_utility+= prob_action*prev_utility
                # print(prob_sum)
                # if not isTerminated:
                expected_utility+=reward
                agent_utility_dict[agent_action]=expected_utility
            
            min_utility=min(agent_utility_dict.values())
            # min_possible_action=[key for key in agent_utility_dict if agent_utility_dict[key]==min_utility] # getting the minimum 
            state_dict[state].append(min_utility)

            if k>1 and (not math.isinf(state_dict[state][-1])) and (not math.isinf(state_dict[state][-2])):
                error+=state_dict[state][-1]-state_dict[state][-2]
        print("Iteration Done ->",k)
        iteration_error=error/len(state_dict)
        print("Iteration Error = ",iteration_error)
        if k>5 and iteration_error<0.001:
            break
        error_list.append(iteration_error)

    value_list=state_dict.values()
    m=-1
    for l in value_list:
        l2=l[2:]
        m_l=max(l)
        if m<m_l and not math.isinf(m_l):
            m=m_l
    
    #========= Constructing utility dictionary ==========
    for state in final_utility:
        final_utility[state]=state_dict[state][-1]
    #======== Dumping a dictionary as pickle and then reading it again using loads =====
    final_utility_file = open("StoredUtilities/Graph1_Utility7.pkl", "wb")
    pickle.dump(final_utility, final_utility_file)
    # final_utility_file.write(str(final_utility))
    final_utility_file.close()

    end=time()
    print("Max Utility = ",m)
    file.write('\n Max Utility =  %s'%str(m))
    file.write("\n\nExecution Time = "+str(end-start)+" s\n")

    file.write('\n Iteration Error->')
    for error in error_list:
        file.write('  %s, '%str(error))

    file.write('\n \nState Dictionary->')
    for key, value in state_dict.items(): 
        file.write('    %s  :       %s  \n' % (key, value[:15]))
    print("Done")
    print("Execution time : "+str(end-start)+" s")
    # print_dict(state_dict)






















