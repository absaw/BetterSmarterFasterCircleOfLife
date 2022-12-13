#this file does the job of simulating the movement of agent prey and predator
#Variables needed
from Graph import *
from BFS import *
from Prey import *
from Predator import *
from VModelAgent import *
import csv
from time import time
from datetime import datetime
def v_model_agent():
    start = time()
    
    #=========== Log file =======================
    filename_txt="/Users/abhishek.sawalkar/Library/Mobile Documents/com~apple~CloudDocs/AI Project/BetterSmarterFasterCircleOfLife/Results/VModelAgent.txt"
    # filename_csv="Results/VModelAgent.csv"
    file=open(filename_txt,"a")
    # csvfile = open(filename_csv, "a")
    # csv_writer=csv.writer(csvfile)
    # fields=['Date Time','Simulation Number','Number of Graphs','Won','Died','Hanged','Comments']
    # csv_writer.writerow(fields)
    text = "\n\n\n======  Start Time  =========->  " + \
        datetime.now().strftime("%m/%d/%y %H:%M:%S")
    file.write(text)
    file.write("\nNo. of Simulations = 30")
    file.write("\nNo. of trials for each simulation = 100")
    # csv_writer.writerow(["Execution Started"])

    #============================================

    n_sim=1    # No. of simulations
    n_trials=3000    # No. of Trials. Each trial has a random new graph. Final Metrics of one simulation will be calculated from these 100 trials
                    # We then average out the metrics, from the 30 simulations we have, to eventually get the final results.
    
    n_nodes=50
    win_list=[]
    lose_list=[]
    hang_list=[]
    step_list=[]

    #Loading data
    with open('/Users/abhishek.sawalkar/Library/Mobile Documents/com~apple~CloudDocs/AI Project/BetterSmarterFasterCircleOfLife/StoredUtilities/Graph1_Utility6.pkl', 'rb') as handle:
        data = handle.read()
    utility_dict = pickle.loads(data)
    
    with open('/Users/abhishek.sawalkar/Library/Mobile Documents/com~apple~CloudDocs/AI Project/BetterSmarterFasterCircleOfLife/StoredWeights/param_dict_14.pkl', 'rb') as handle:
        data = handle.read()
    param_dict = pickle.loads(data)
    
    with open('/Users/abhishek.sawalkar/Library/Mobile Documents/com~apple~CloudDocs/AI Project/BetterSmarterFasterCircleOfLife/StoredDistances/dist_dict1.pkl', 'rb') as handle:
        data = handle.read()
    dist_dict = pickle.loads(data)

    G = nx.read_gpickle("/Users/abhishek.sawalkar/Library/Mobile Documents/com~apple~CloudDocs/AI Project/BetterSmarterFasterCircleOfLife/StoredGraph/Graph1.gpickle")

    for sim in range(1,n_sim+1):
        n_win=0     # When agent and prey are in same position, provided pred is not in that position
        n_lose=0    # When agent and predator are in same positionp
        n_hang=0    # When agent can't catch prey, even after walking a certain threshold distance
        hang_threshold=1000
        max_steps=1001
        n_steps=0

        for trial in range(1,n_trials+1):
    
            #generate graph
            # G=generate_graph(n_nodes)
            # GraphClass=Graph(n_nodes)
            # G=GraphClass.G

            #spawn prey, predator and agent at random locations

            prey=Prey(n_nodes,G)
            predator=Predator(n_nodes, G)
            u_star_agent=VModelAgent(n_nodes, G, prey, predator,utility_dict,param_dict,dist_dict)
            
            path=[]
            path.append(u_star_agent.position)
            steps=0
            # print("\n\n New Trial Started \n\n")
            # The three players move in rounds, starting with the Agent, followed by the Prey, and then the Predator.
            while(steps<=max_steps):
                steps+=1
                # print("\n\n New Step Started \n\n")
                #========= Agent One Simulation  ========
                #======== Print State ========
                # print("\n")
                # d_prey=len(get_bfs_path(G, u_star_agent.position, prey.position))-1
                # d_pred=len(get_bfs_path(G, u_star_agent.position, predator.position))-1
                # print("Before Agent Sim step")
                # st=(u_star_agent.position,prey.position,predator.position)
                # print("Distance to Prey = ",d_prey)
                # print("Distance to Pred = ",d_pred)
                # print("State -> ",st)
                # n_l=list(G.neighbors(u_star_agent.position))
                # print("Neighbors of Agent ->",list(G.neighbors(u_star_agent.position)))
                # print("Utility of Neighbors->")
                # for n in n_l:
                #     st_n=(n,prey.position,predator.position)
                #     print("Utility of ",st_n," = ",utility_dict[st_n])
                # #=========================

                u_star_agent.simulate_step(prey, predator)

                #======== Print State ========
                # print("\n")
                # d_prey=len(get_bfs_path(G, u_star_agent.position, prey.position))-1
                # d_pred=len(get_bfs_path(G, u_star_agent.position, predator.position))-1
                # print("After Agent Sim step")
                # print("Step taken to - ",u_star_agent.position)
                # print("Distance to Prey = ",d_prey)
                # print("Distance to Pred = ",d_pred)
                # st=(u_star_agent.position,prey.position,predator.position)
                # print("State -> ",st)
                # n_l=list(G.neighbors(u_star_agent.position))
                # print("Neighbors of Agent ->",list(G.neighbors(u_star_agent.position)))
                # print("Utility of Neighbors->")
                # for n in n_l:
                #     st_n=(n,prey.position,predator.position)
                #     print("Utility of ",st_n," = ",utility_dict[st_n])
                #=========================

                # Now we have our agent's next position
                #========= Terminal Condition Check  ========
                if u_star_agent.position==prey.position:
                    n_win+=1
                    n_steps+=steps
                    break
                if u_star_agent.position==predator.position:
                    n_lose+=1
                    break
                # Threshold condition
                if steps>=hang_threshold:
                    n_hang+=1
                    break
                #======== Print State ========
                # print("\n")
                # d_prey=len(get_bfs_path(G, u_star_agent.position, prey.position))-1
                # d_pred=len(get_bfs_path(G, u_star_agent.position, predator.position))-1
                # print("Before Prey Sim step")
                # st=(u_star_agent.position,prey.position,predator.position)
                # print("Distance to Prey = ",d_prey)
                # print("Distance to Pred = ",d_pred)
                # print("State -> ",st)
                # n_l=list(G.neighbors(u_star_agent.position))
                # print("Neighbors of Agent ->",list(G.neighbors(u_star_agent.position)))
                # print("Utility of Neighbors->")
                # for n in n_l:
                #     st_n=(n,prey.position,predator.position)
                #     print("Utility of ",st_n," = ",utility_dict[st_n])
                # #=========================
                # ======== Prey Simulation   =========
                prey.simulate_step()
                #======== Print State ========
                # print("\n")
                # d_prey=len(get_bfs_path(G, u_star_agent.position, prey.position))-1
                # d_pred=len(get_bfs_path(G, u_star_agent.position, predator.position))-1
                # print("After Prey Sim step")
                # st=(u_star_agent.position,prey.position,predator.position)
                # print("Distance to Prey = ",d_prey)
                # print("Distance to Pred = ",d_pred)
                # print("State -> ",st)
                # n_l=list(G.neighbors(u_star_agent.position))
                # print("Neighbors of Agent ->",list(G.neighbors(u_star_agent.position)))
                # print("Utility of Neighbors->")
                # for n in n_l:
                #     st_n=(n,prey.position,predator.position)
                #     print("Utility of ",st_n," = ",utility_dict[st_n])
                # #=========================
                #========= Terminal Condition Check  ========
                if u_star_agent.position==prey.position:
                    n_win+=1
                    n_steps+=steps

                    # print("Goal Reached")
                    break
                if u_star_agent.position==predator.position:
                    n_lose+=1
                    # print("Agent Dead")
                    break

                #======== Print State ========
                # print("\n")
                # d_prey=len(get_bfs_path(G, u_star_agent.position, prey.position))-1
                # d_pred=len(get_bfs_path(G, u_star_agent.position, predator.position))-1
                # print("Before Pred Sim step")
                # st=(u_star_agent.position,prey.position,predator.position)
                # print("Distance to Prey = ",d_prey)
                # print("Distance to Pred = ",d_pred)
                # print("State -> ",st)
                # n_l=list(G.neighbors(u_star_agent.position))
                # print("Neighbors of Agent ->",list(G.neighbors(u_star_agent.position)))
                # print("Utility of Neighbors->")
                # for n in n_l:
                #     st_n=(n,prey.position,predator.position)
                #     print("Utility of ",st_n," = ",utility_dict[st_n])
                # #=========================
                # ======== Predator Simulation   =========
                predator.simulate_step_distracted(u_star_agent.position)
                #======== Print State ========
                # print("\n")
                # d_prey=len(get_bfs_path(G, u_star_agent.position, prey.position))-1
                # d_pred=len(get_bfs_path(G, u_star_agent.position, predator.position))-1
                # print("After pred Sim step")
                # st=(u_star_agent.position,prey.position,predator.position)
                # print("Distance to Prey = ",d_prey)
                # print("Distance to Pred = ",d_pred)
                # print("State -> ",st)
                # n_l=list(G.neighbors(u_star_agent.position))
                # print("Neighbors of Agent ->",list(G.neighbors(u_star_agent.position)))
                # print("Utility of Neighbors->")
                # for n in n_l:
                #     st_n=(n,prey.position,predator.position)
                #     print("Utility of ",st_n," = ",utility_dict[st_n])
                # #=========================
                #========= Terminal Condition Check  ========
                if u_star_agent.position==prey.position:
                    n_win+=1
                    n_steps+=steps
                    break
                if u_star_agent.position==predator.position:
                    n_lose+=1
                    break

                # path.append(next_position)

        print("Sim -> ", sim)
        print("Alive ->",n_win)       
        print("Dead ->",n_lose)       
        print("Hang ->",n_hang)       
        # print()
        win_list.append(n_win)
        lose_list.append(n_lose)
        hang_list.append(n_hang)
        step_list.append(n_steps/n_win)
        time_now=datetime.now().strftime("%m/%d/%y %H:%M:%S")
        file.write("\nReport for Simulation Number %d" % sim)
        file.write("\nPlayer Survivability = %d" % n_win+" %")
        
        # csv_writer.writerow([time_now,sim,100,str(n_win),str(n_lose),str(n_hang)])
    
    # print("Win List : ",*win_list)
    # print("Lose List : ",*lose_list)
    print("Average wins : ",(sum(win_list)/30))
    # print("Average losses : ",(sum(lose_list)/len(lose_list)))
    # print("Average hangs : ",(sum(hang_list)/len(hang_list)))
    print("Average steps : ",(sum(step_list)/len(step_list)))
    # print("Hang Threshold : ",hang_threshold)

    # Log file Start
    file.write("\n\nSummary : ")
    file.write("\nWin List : "+str(win_list))
    # file.write("\nLose List : "+str(lose_list))
    file.write("\nAverage wins : %.2f" % (sum(win_list)/30))
    # file.write("\nAverage losses : %.2f" % (sum(lose_list)/len(lose_list)))
    # file.write("\nAverage hangs : %.2f" % (sum(hang_list)/len(hang_list)))
    file.write("\nAverage steps : %.2f" % (sum(step_list)/len(step_list)))
    # file.write("\nHang Threshold : %.2f" % hang_threshold)
    end=time()
    file.write("\n\nExecution Time = "+str(end-start)+" s")
    print("Execution time : "+str(end-start)+" s")
    file.close()
    # Log file End
    print("Done!")
v_model_agent()


                            
                




                





                









