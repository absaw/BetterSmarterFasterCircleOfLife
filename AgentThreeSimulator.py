#this file does the job of simulating the movement of agent prey and predator
#Variables needed
from Graph import *
from BFS import *
from Prey import *
from Predator import *
from AgentThree import *
import csv
from time import time
from datetime import datetime
def simulate_agent_three():
    #=========== Log file =======================
    start = time()
    filename_txt="Results/AgentThree.txt"
    filename_csv="Results/AgentThree.csv"
    file=open(filename_txt,"a")
    csvfile = open(filename_csv, "a")
    csv_writer=csv.writer(csvfile)
    fields=['Date Time','Simulation Number','Number of Graphs','Won','Died','Hanged','No. of Steps','Frequency of Knowing Exact Location','Comments']
    csv_writer.writerow(fields)
    text = "\n\n\n======  Start Time  =========->  " + \
        datetime.now().strftime("%m/%d/%y %H:%M:%S")
    file.write(text)
    file.write("\nNo. of Simulations = 30")
    file.write("\nNo. of trials for each simulation = 100")
    csv_writer.writerow(["Execution Started"])

    #============================================
    n_sim=30      # No. of simulations
    n_trials=100    # No. of Trials. Each trial has a random new graph. Final Metrics of one simulation will be calculated from these 100 trials
                    # We then average out the metrics, from the 30 simulations we have, to eventually get the final results.
    
    n_nodes=50
    win_list=[]
    lose_list=[]
    hang_list=[]
    step_list=[]
    sure_list=[]
    for sim in range(1,n_sim+1):
        n_win=0     # When agent and prey are in same position, provided pred is not in that position
        n_lose=0    # When agent and predator are in same position
        n_hang=0    # When agent can't catch prey, even after walking a certain threshold distance
        hang_threshold=1000
        max_steps=1001
        n_steps=0
        n_sure=0
        for trial in range(1,n_trials+1):

            #generate graph
            GraphClass=Graph(n_nodes)
            G=GraphClass.G

            #spawn prey, predator and agent at random locations
            prey=Prey(n_nodes,G)
            predator=Predator(n_nodes, G)
            agent_three=AgentThree(n_nodes, G, prey, predator)
            
            steps=0
            survey_list=list(range(1,51))
            survey_list.remove(agent_three.position)
            survey_node=random.choice(survey_list)
            # The three players move in rounds, starting with the Agent, followed by the Prey, and then the Predator.
            while(steps<=max_steps):
                steps+=1
                # print("\n\nStep ->>>>> ",steps)
                # agent_three.print_state()
                # ========= Terminal Condition Check  ========
                if agent_three.position==predator.position:
                    n_lose+=1
                    break
                if agent_three.position==prey.position:
                    # print("Prey found")
                    n_win+=1
                    n_steps+=steps
                    break
                # Threshold condition
                if steps>=hang_threshold:
                    # print("hanged")
                    n_hang+=1
                    break
               
                #========= Agent Three Simulation  ========
                agent_three.simulate_step(survey_node,prey, predator)
                # Now we have our agent's next position
                # ========= Terminal Condition Check  ========
                if agent_three.position==predator.position:
                    n_lose+=1
                    break
                if agent_three.position==prey.position:
                    n_win+=1
                    n_steps+=steps
                    break

                # ======== Prey Simulation   =========
                prey.simulate_step()
                # New Info : Prey has moved. So update apply transition probability update to each node in graph
                agent_three.transition_update()
                agent_three.p_now=agent_three.p_next.copy()
                #agent_three.print_sum()

                #========= Terminal Condition Check  ========
                if agent_three.position==prey.position:
                    n_win+=1
                    n_steps+=steps
                    break
                # New Info : Prey is not in current agent's position. So update belief system
                # agent_three.update_belief(agent_three.position, prey.position)
                
                #agent_three.print_sum()
                
                # ======== Predator Simulation   =========
                predator.simulate_step(agent_three.position)

                # ========= Terminal Condition Check  ========
                if agent_three.position==predator.position:
                    n_lose+=1
                    break
                if agent_three.position==prey.position:
                    n_win+=1
                    n_steps+=steps
                    break

                m=max(agent_three.p_now) #finding value with highest prob
                survey_list=[node+1 for node in range(len(agent_three.p_now)) if agent_three.p_now[node]==m] # List of nodes with highest prob value
                survey_node=random.choice(survey_list) #Selecting a random element from highest prob value list
            
            n_sure+=agent_three.sure_of_prey


        win_list.append(n_win)
        lose_list.append(n_lose)
        hang_list.append(n_hang)
        step_list.append(n_steps/n_win)
        sure_list.append(n_sure/n_trials)
        
        time_now=datetime.now().strftime("%m/%d/%y %H:%M:%S")
        file.write("\nReport for Simulation Number %d" % sim)
        file.write("\nPlayer Survivability = %d" % n_win+" %")
        csv_writer.writerow([time_now,sim,100,str(n_win),str(n_lose),str(n_hang),str(n_steps/n_win),str(n_sure/n_trials)])
    
    print("Win List : ",*win_list)
    print("Lose List : ",*lose_list)
    print("Hang List : ",*hang_list)
    print("Sure List : ",*sure_list)
    # print("Step List : ",*step_list)
    print("Average wins : ",(sum(win_list)/len(win_list)))
    print("Average losses : ",(sum(lose_list)/len(lose_list)))
    print("Average hangs : ",(sum(hang_list)/len(hang_list)))
    print("Average steps : ",(sum(step_list)/len(step_list)))
    print("Average No. of times Agent was sure about Prey's Location : ",(sum(sure_list)/len(sure_list)))
    print("Hang Threshold : ",hang_threshold)
    
    # Log file Start
    file.write("\n\nSummary : ")
    file.write("\nWin List : "+str(win_list))
    file.write("\nLose List : "+str(lose_list))
    file.write("\nAverage wins : %.2f" % (sum(win_list)/len(win_list)))
    file.write("\nAverage losses : %.2f" % (sum(lose_list)/len(lose_list)))
    file.write("\nAverage hangs : %.2f" % (sum(hang_list)/len(hang_list)))
    file.write("\nAverage steps : %.2f" % (sum(step_list)/len(step_list)))
    file.write("\nAverage No. of times Agent was sure about Prey's Location : %.2f" % (sum(sure_list)/len(sure_list)))
    file.write("\nHang Threshold : %.2f" % hang_threshold)
    end=time()
    file.write("\n\nExecution Time = "+str(end-start)+" s")
    print("Execution time : "+str(end-start)+" s")
    file.close()
    # Log file End
# simulate_agent_three()


                            
                




                





                









