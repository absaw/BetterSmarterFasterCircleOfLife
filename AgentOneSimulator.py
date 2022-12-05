#this file does the job of simulating the movement of agent prey and predator
#Variables needed
from Graph import *
from BFS import *
from Prey import *
from Predator import *
from AgentOne import *
import csv
from time import time
from datetime import datetime
def simulate_agent_one():
    start = time()
    
    #=========== Log file =======================
    filename_txt="Results/AgentOne.txt"
    filename_csv="Results/AgentOne.csv"
    file=open(filename_txt,"a")
    csvfile = open(filename_csv, "a")
    csv_writer=csv.writer(csvfile)
    fields=['Date Time','Simulation Number','Number of Graphs','Won','Died','Hanged','Comments']
    csv_writer.writerow(fields)
    text = "\n\n\n======  Start Time  =========->  " + \
        datetime.now().strftime("%m/%d/%y %H:%M:%S")
    file.write(text)
    file.write("\nNo. of Simulations = 30")
    file.write("\nNo. of trials for each simulation = 100")
    csv_writer.writerow(["Execution Started"])

    #============================================

    n_sim=30    # No. of simulations
    n_trials=100    # No. of Trials. Each trial has a random new graph. Final Metrics of one simulation will be calculated from these 100 trials
                    # We then average out the metrics, from the 30 simulations we have, to eventually get the final results.
    
    n_nodes=50
    win_list=[]
    lose_list=[]
    hang_list=[]
    step_list=[]
    for sim in range(1,n_sim+1):
        n_win=0     # When agent and prey are in same position, provided pred is not in that position
        n_lose=0    # When agent and predator are in same position
        n_hang=0    # When agent can't catch prey, even after walking a certain threshold distance
        hang_threshold=1000
        max_steps=1001
        n_steps=0

        for trial in range(1,n_trials+1):

            #generate graph
            # G=generate_graph(n_nodes)
            GraphClass=Graph(n_nodes)
            G=GraphClass.G

            #spawn prey, predator and agent at random locations

            prey=Prey(n_nodes,G)
            predator=Predator(n_nodes, G)
            agent_one=AgentOne(n_nodes, G, prey, predator)
            
            path=[]
            path.append(agent_one.position)
            steps=0
            # The three players move in rounds, starting with the Agent, followed by the Prey, and then the Predator.
            while(steps<=max_steps):
                steps+=1
                #========= Agent One Simulation  ========
                agent_one.simulate_step(prey, predator)
                # Now we have our agent's next position

                #========= Terminal Condition Check  ========
                if agent_one.position==predator.position:
                    n_lose+=1
                    break
                if agent_one.position==prey.position:
                    n_win+=1
                    n_steps+=steps
                    break
                # Threshold condition
                if steps>=hang_threshold:
                    n_hang+=1
                    break

                # ======== Prey Simulation   =========
                prey.simulate_step()

                #========= Terminal Condition Check  ========
                if agent_one.position==predator.position:
                    n_lose+=1
                    # print("Agent Dead")
                    break
                if agent_one.position==prey.position:
                    n_win+=1
                    n_steps+=steps

                    # print("Goal Reached")
                    break
                # ======== Predator Simulation   =========
                predator.simulate_step(agent_one.position)

                #========= Terminal Condition Check  ========
                if agent_one.position==predator.position:
                    n_lose+=1
                    break
                if agent_one.position==prey.position:
                    n_win+=1
                    n_steps+=steps

                    break

                # path.append(next_position)

        # print("Sim -> ", sim)
        # print("Alive ->",n_win)       
        # print("Dead ->",n_lose)       
        # print("Hang ->",n_hang)       
        # print()
        win_list.append(n_win)
        lose_list.append(n_lose)
        hang_list.append(n_hang)
        step_list.append(n_steps/n_win)
        time_now=datetime.now().strftime("%m/%d/%y %H:%M:%S")
        file.write("\nReport for Simulation Number %d" % sim)
        file.write("\nPlayer Survivability = %d" % n_win+" %")
        
        csv_writer.writerow([time_now,sim,100,str(n_win),str(n_lose),str(n_hang)])
    
    print("Win List : ",*win_list)
    print("Lose List : ",*lose_list)
    print("Average wins : ",(sum(win_list)/len(win_list)))
    print("Average losses : ",(sum(lose_list)/len(lose_list)))
    print("Average hangs : ",(sum(hang_list)/len(hang_list)))
    print("Average steps : ",(sum(step_list)/len(step_list)))
    print("Hang Threshold : ",hang_threshold)

    # Log file Start
    file.write("\n\nSummary : ")
    file.write("\nWin List : "+str(win_list))
    file.write("\nLose List : "+str(lose_list))
    file.write("\nAverage wins : %.2f" % (sum(win_list)/len(win_list)))
    file.write("\nAverage losses : %.2f" % (sum(lose_list)/len(lose_list)))
    file.write("\nAverage hangs : %.2f" % (sum(hang_list)/len(hang_list)))
    file.write("\nAverage steps : %.2f" % (sum(step_list)/len(step_list)))
    file.write("\nHang Threshold : %.2f" % hang_threshold)
    end=time()
    file.write("\n\nExecution Time = "+str(end-start)+" s")
    print("Execution time : "+str(end-start)+" s")
    file.close()
    # Log file End
    print("Done!")
# simulate_agent_one()


                            
                




                





                









